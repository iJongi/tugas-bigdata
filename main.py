import os
import requests
import json
from google.cloud import storage
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

AQI_API_URL = "https://api.waqi.info/feed/@8294/?token=XXXXXXXXXXXXXXXXXXX"

STORAGE_BUCKET_NAME = "kualitas-udara-jakarta"
STORAGE_FOLDER = "raw_aqi_data"

@app.route("/", methods=['GET'])
def fetch_and_save_aqi_data():
    try:
        response = requests.get(AQI_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        timestamp = datetime.now().isoformat()
        
        if data.get('status') != 'ok':
            print(f"API Error: Status not 'ok'. Message: {data.get('data')}")
            return f"Error: API returned status '{data.get('status')}'", 500

        data_to_save = {
            "timestamp_gcp": timestamp,
            "aqi_data": data.get('data')
        }
        
        storage_client = storage.Client()
        bucket = storage_client.bucket(STORAGE_BUCKET_NAME)
        
        blob_name = f"{STORAGE_FOLDER}/{datetime.now().strftime('%Y-%m-%dT%H%M%S')}.json"
        blob = bucket.blob(blob_name)
        
        json_data_string = json.dumps(data_to_save)
        
        blob.upload_from_string(
            json_data_string,
            content_type='application/json'
        )
        
        print(f"Success! Data AQI saved to gs://{STORAGE_BUCKET_NAME}/{blob_name}")
        
        return 'Data AQI successfully fetched and stored.', 200

    except requests.exceptions.RequestException as e:
        print(f"Error calling external API: {e}")
        return f"Error calling external API: {e}", 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}", 500
