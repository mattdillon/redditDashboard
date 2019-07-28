import boto3
from datetime import date, timedelta
from sosna_helpers import log
import r_credentials

LOG_FILE = 'logs/json_to_s3_log_'

aws_secret_access_key = r_credentials.s3_credentials['aws_secret_access_key']
aws_access_key_id = r_credentials.s3_credentials['aws_access_key_id']

def upload_to_bucket(key, bucket):
	log(LOG_FILE, 'Uploading {} to s3 {} bucket'.format(key, bucket))

	s3_resource = boto3.resource('s3', aws_secret_access_key=aws_secret_access_key, aws_access_key_id=aws_access_key_id)
	object = s3_resource.Object(bucket_name = bucket, key = key)
	object.upload_file('./'+key)

if __name__ == '__main__':
	
	s3_key  =  'output/r_hiking_output_' + str(date.today()) + '.txt'
	#print('Uploading {} to s3 {} bucket'.format(file_name, 'sosna-reddit-data'))
	upload_to_bucket(s3_key, 'sosna-reddit-data') 
