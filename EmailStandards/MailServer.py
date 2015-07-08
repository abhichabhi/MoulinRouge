class MailServer(object):
	msg = None
	def __init__(self, server_name='smtp.gmail.com', username='bazaarfunda@gmail.com', password='krish1436', port=0, require_starttls=True):
		self.server_name = server_name
		self.username = username
		self.password = password
		self.port = port
		self.require_starttls = require_starttls
