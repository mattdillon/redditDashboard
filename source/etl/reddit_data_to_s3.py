import requests
import requests.auth
import r_credentials
import datetime
import time
from datetime import datetime, timedelta, timezone

ROOT_URL = "https://www.reddit.com"


#get access token
def get_r_token(username, password, appClientId, appSecret):
	url = 'https://www.reddit.com/api/v1/access_token'
	clientAuth = requests.auth.HTTPBasicAuth(appClientId, appSecret)
	postData = {'grant_type': 'password', 'username': username, 'password': password}
	headers = {'User-Agent': 'ChangeMeClient/0.1 by YourUserName'}
	
	print(('Retrieving access_token for user: {}').format(username))

	try:
		res = requests.post(url, auth=clientAuth,data=postData, headers=headers)
		#print(res.json())
		token = res.json()['access_token']
		print(('Retrieved token: {}').format(token))
		return token
	except:
		print('Could not retrive token')
		raise
		return 1
	

def get_time_limits():
	yesterday = datetime.now(timezone.utc).date() - timedelta(days=1)
	today = datetime.now(timezone.utc).date()	

	yesterday_linux = time.mktime(yesterday.timetuple())
	today_linux = time.mktime(today.timetuple())

	return yesterday_linux, today_linux


if __name__ == '__main__':
	username = r_credentials.reddit_credentials['username']
	password = r_credentials.reddit_credentials['password']
	appClientId = r_credentials.reddit_credentials['appClientId']
	appSecret = r_credentials.reddit_credentials['appSecret']
	
	token = get_r_token(username, password, appClientId, appSecret)
