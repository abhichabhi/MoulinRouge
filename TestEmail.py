from EmailStandards.EmailTemplate import EmailTemplate
from EmailStandards.MailServer import MailServer
from EmailStandards.MailMessage import MailMessage
from send import send
values = {}
values['username'] = 'Ludmal de silva!'
values['from'] = 'The Team'
values['url'] = 'http://www.bazaarfunda.com'
temp = EmailTemplate(template_name='TestTemplate.html', values=values)

server = MailServer(server_name='smtp.gmail.com', username='*********', password='*******', port=0,   require_starttls=True)
msg = MailMessage(from_email='dude.abhi.chat@gmail.com', to_emails=['dude.abhi.chat@gmail.com'], subject='Welcome')
send(mail_msg=msg, mail_server=server, template=temp)