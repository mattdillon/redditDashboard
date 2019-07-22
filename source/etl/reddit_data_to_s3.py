import requests
import requests.auth
import r_credentials
import datetime
import time
from datetime import datetime, timedelta, timezone, date

ROOT_URL = "https://www.reddit.com"
LOG_FILE = "logs/reddit_etl_log_"

def log(msg):
	today = str(date.today())
	file_name = LOG_FILE + today
	
	log = open(file_name, 'a')
	ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
	
	log.write(ts + '\n')

	log.write(msg + '\n')
	log.write('\n')
	log.close()

#get access token
def get_r_token(username, password, appClientId, appSecret):
	url = 'https://www.reddit.com/api/v1/access_token'
	clientAuth = requests.auth.HTTPBasicAuth(appClientId, appSecret)
	postData = {'grant_type': 'password', 'username': username, 'password': password}
	headers = {'User-Agent': 'ChangeMeClient/0.1 by YourUserName'}
	
	log(('Retrieving access_token for user: {}').format(username))

	try:
		res = requests.post(url, auth=clientAuth,data=postData, headers=headers)
		#print(res.json())
		token = res.json()['access_token']
		log(('Retrieved token: {}').format(token))
		return token
	except:
		log('Could not retrive token')
		raise
		return 1
	

def get_time_limits():
	
	log('Getting time limits...')
	yesterday = datetime.now(timezone.utc).date() - timedelta(days=1)
	today = datetime.now(timezone.utc).date()	

	yesterday_linux = time.mktime(yesterday.timetuple())
	today_linux = time.mktime(today.timetuple())

	log('Start: {}\nEnd: {}'.format(yesterday_linux, today_linux))

	return yesterday_linux, today_linux


if __name__ == '__main__':
	username = r_credentials.reddit_credentials['username']
	password = r_credentials.reddit_credentials['password']
	appClientId = r_credentials.reddit_credentials['appClientId']
	appSecret = r_credentials.reddit_credentials['appSecret']
	
	token = get_r_token(username, password, appClientId, appSecret)

	start, end = get_time_limits()
	
	spacer = '#'*50+'\n'
	log('reddit_to_s3 sript completed\n\n' + spacer*3)
