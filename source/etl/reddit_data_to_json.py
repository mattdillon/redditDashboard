import requests
import requests.auth
import r_credentials
import datetime
import time
from datetime import datetime, timedelta, timezone, date
import praw
import json
from sosna_helpers import log
import argparse

ROOT_URL = "https://www.reddit.com"
LOG_FILE = "logs/reddit_etl_log_"


#get access token
def get_r_token(username, password, appClientId, appSecret):
	url = 'https://www.reddit.com/api/v1/access_token'
	clientAuth = requests.auth.HTTPBasicAuth(appClientId, appSecret)
	postData = {'grant_type': 'password', 'username': username, 'password': password}
	headers = {'User-Agent': 'sosnaDash/0.1 by mattdillon'}
	
	log(LOG_FILE, ('Retrieving access_token for user: {}').format(username))

	try:
		res = requests.post(url, auth=clientAuth,data=postData, headers=headers)
		#print(res.json())
		token = res.json()['access_token']
		log(LOG_FILE, ('Retrieved token: {}').format(token))
		return token
	except:
		log(LOG_FILE, 'Could not retrive token')
		raise
		return 1
	

def get_time_limits(date):
	
	log(LOG_FILE, 'Getting time limits...')
	#yesterday = datetime.now(timezone.utc).date() - timedelta(days=1)
	#today = datetime.now(timezone.utc).date()	

	yesterday = date - timedelta(days=1)

	yesterday_linux = time.mktime(yesterday.timetuple())
	today_linux = time.mktime(date.timetuple())

	log(LOG_FILE, 'Start: {}\nEnd: {}'.format(yesterday_linux, today_linux))

	return yesterday_linux, today_linux


def fetch_r_posts(subreddit, num):
	log(LOG_FILE, 'Fetching last {} posts for r/{}'.format(str(num), subreddit))
	
	reddit = praw.Reddit(client_id='oOfnrLqNV-nurw', client_secret='PN96hsK1oFu0HrtkjJh6J4XSSMc',user_agent='sosnaDash/0.1 by mattdillon')
	sub_reddit = reddit.subreddit(subreddit)
		
	return sub_reddit.new(limit = num)
	


if __name__ == '__main__':
	username = r_credentials.reddit_credentials['username']
	password = r_credentials.reddit_credentials['password']
	appClientId = r_credentials.reddit_credentials['appClientId']
	appSecret = r_credentials.reddit_credentials['appSecret']

	parser = argparse.ArgumentParser()
	parser.add_argument('-s', action='store', dest='subreddit', help='Subreddit to collect posts from')
	parser.add_argument('-n', action='store', dest='post_count', help='Number of posts to collect') 

	args = parser.parse_args()
	subreddit = args.subreddit
	post_count = int(args.post_count)
	
	for arg in vars(args):
		log(LOG_FILE, arg + ' : ' + getattr(args, arg))
	
		
	
		
	token = get_r_token(username, password, appClientId, appSecret)

	start, end = get_time_limits(datetime.now(timezone.utc).date()-timedelta(days=1))

	posts = fetch_r_posts(subreddit, post_count)
	output_file = './output/r_' + subreddit + '_output_' + str(date.today()) + '.txt'
	f = open(output_file, 'w', encoding='utf-8')
	data = []
	for p in posts:
		if (start <= p.created_utc and p.created_utc < end):
			p_obj = {}
			p_obj['created_utc'] = p.created_utc
			p_obj['title'] = p.title
			p_obj['content'] = p.selftext
			data.append(p_obj)
	log(LOG_FILE, 'Writing {} objects to: {}'.format(len(data), output_file))
	json.dump(data, f)
	f.close()  

	
	
	spacer = '#'*50+'\n'
	log(LOG_FILE, 'reddit_to_s3 sript completed\n\n' + spacer*3)
