import boto3
from datetime import date, timedelta
from sosna_helpers import log

LOG_FILE = 'logs/json_to_s3_log_'

def upload_to_bucket(key, bucket):
	log(LOG_FILE, 'Uploading {} to s3 {} bucket'.format(key, bucket))

	s3_resource = boto3.resource('s3')
	object = s3_resource.Object(bucket_name = bucket, key = key)
	object.upload_file('./'+key)

if __name__ == '__main__':
	
	s3_key  =  'output/r_hiking_output_' + str(date.today() - timedelta(days=1)) + '.txt'
	#print('Uploading {} to s3 {} bucket'.format(file_name, 'sosna-reddit-data'))
	upload_to_bucket(s3_key, 'sosna-reddit-data') 
