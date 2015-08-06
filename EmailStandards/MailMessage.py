import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class MailMessage(object):
	html = True
	def __init__(self, from_email='', to_emails=[], cc_emails=[], subject='', body=''):
		self.from_email = from_email
		self.to_emails = to_emails
		self.cc_emails = cc_emails
		self.subject = subject
		self.body = body
	def get_message(self):
		if isinstance(self.to_emails, str):
			self.to_emails = [self.to_emails]
		if isinstance(self.cc_emails, str):
			self.cc_emails = [self.cc_emails]
		if len(self.to_emails) == 0 or self.from_email == '':
			raise Exception('Invalid From or To email address(es)')
		msg = MIMEMultipart('alternative')
		msg['To'] = ', '.join(self.to_emails)
		msg['Cc'] = ', '.join(self.cc_emails)
		msg['From'] = self.from_email
		msg['subject'] = self.subject
		self.body = self.body.encode('utf-8')
		HTML_BODY = MIMEText(self.body, 'html')
		msg.attach(HTML_BODY)
		return msg