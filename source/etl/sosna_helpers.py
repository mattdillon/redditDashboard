import datetime
import time
from datetime import date, timedelta, timezone, date


def log(log_file, msg):
	today = str(date.today())
	file_name = log_file + today
	
	log = open(file_name, 'a')
	ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
	
	log.write(ts + '\n')

	log.write(msg + '\n')
	log.write('\n')
	log.close()
