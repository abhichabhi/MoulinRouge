import os, email, smtplib
from EmailStandards.MailServer import MailServer
def send(mail_msg, mail_server=MailServer(), template=None):
	server = smtplib.SMTP(mail_server.server_name, 587)
	if mail_server.require_starttls:
		server.starttls()
	server.login(mail_server.username, mail_server.password)
	# if template:
	# 	mail_msg.body = template.render()
	# 	mail_msg.html = template.html
	server.sendmail(mail_msg.from_email, ', '.join(mail_msg.to_emails), mail_msg.get_message().as_string())
	server.close()
