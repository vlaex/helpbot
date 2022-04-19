from datetime import datetime
import pytz

tz = pytz.timezone('Europe/Moscow')

def ts_to_date(timestamp: str) -> str:
  return datetime.fromtimestamp(float(timestamp), tz).strftime('%d.%m.%Y %H:%M:%S')
