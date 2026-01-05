function transform(line) {
  var row;
  try {
    row = JSON.parse(line);
  } catch (e) {
    return null;
  }

  if (!row || !row.aqi_data) return null;

  var aqiData = row.aqi_data;
  var iaqi = aqiData.iaqi || {};
  var city = aqiData.city || {};
  var time = aqiData.time || {};

  function getVal(obj) {
    return (obj && obj.v !== undefined) ? obj.v : null;
  }

  function safeDate(dateStr) {
    if (!dateStr) return null;
    try {
        var dt = new Date(dateStr);
        if (isNaN(dt.getTime())) return null; 
        return dt.toISOString();
    } catch (e) {
        return null;
    }
  }

  var timestampGcpStr = safeDate(row.timestamp_gcp);
  
  if (!timestampGcpStr) {
      timestampGcpStr = new Date().toISOString(); 
  }

  var timeStr = safeDate(time.s);

  return JSON.stringify({
    timestamp_gcp: timestampGcpStr,
    aqi: (aqiData.aqi !== undefined) ? aqiData.aqi : null,
    idx: (aqiData.idx !== undefined) ? aqiData.idx : null,
    city: city.name || null,
    pm25: getVal(iaqi.pm25),
    o3: getVal(iaqi.o3),
    so2: getVal(iaqi.so2),
    time_s: timeStr,
    aqi_data: JSON.stringify(aqiData) 
  });
}
