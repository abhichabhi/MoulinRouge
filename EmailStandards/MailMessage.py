import email
class MailMessage(object):
	html = False
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
		msg = email.Message.Message()
		msg['To'] = ', '.join(self.to_emails)
		msg['Cc'] = ', '.join(self.cc_emails)
		msg['From'] = self.from_email
		msg['subject'] = self.subject
		#TODO - Add HTML/TEXT support to the Body
		msg.set_payload(self.body)
		return msg