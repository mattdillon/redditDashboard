import smtplib
from email.mime.text import MIMEText
from r_credentials import audit_dist_list



FROM = 'etl@sosna.us'

TO = ['dillonmc26@gmail.com']

#for contact in audit_dist_list.recipients:
#	TO.append(contact['email']

SUBJECT = 'ETL Job Completed'

def send_audit_email(msg):

	msg = MIMEText(msg)

	#message = """\
	#From:{} 
	#To: {}
	#Subject: {}

	#{}
	#""".format(FROM, ", ".join(TO), SUBJECT, TEXT)

	msg['Subject'] = SUBJECT
	msg['From'] = FROM
	msg['To'] = TO[0] 

	server = smtplib.SMTP('mail.sosna.us')
	server.send_message(msg)
	server.quit()

def read_message_template(filename, var_dict):
	f = open(filename, 'r', encoding='utf-8')
	content = f.read()
	
	formatted = content.format(**var_dict)
	return formatted	

if __name__ == '__main__':
	print('sending test email...')
	send_audit_email('this is only a test :)')
		


