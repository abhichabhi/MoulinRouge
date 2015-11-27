from EmailStandards.EmailTemplate import EmailTemplate
from EmailStandards.MailServer import MailServer
from EmailStandards.MailMessage import MailMessage
from send import send
from pymongo import MongoClient
from celery import Celery
from celery import current_app
import time
from celery import signature
import ConfigParser
import requests
BROKER_URL = 'mongodb://localhost:27017/jobs'
 
celery = Celery('EOD_TASKS',broker=BROKER_URL)
 
#Loads settings for Backend to store results of jobs
celery.config_from_object('celeryconfig')

def ConfigSectionMap(section):
	Config = ConfigParser.ConfigParser()
	Config.read('./configuration/DBConfig.ini')
        configDict = {}
        options = Config.options(section)
        for option in options:
            try:
                configDict[option] = Config.get(section, option)
                if configDict[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                configDict[option] = None
        return configDict

def getMongoClient(section):
	configSectionMap = ConfigSectionMap(section)
	mongo = MongoClient(configSectionMap['host'], int(configSectionMap['port']))[configSectionMap['name']]
	return mongo

@celery.task
def sendEmail(values, server):
	print "in send email"
	values['from'] = 'BazaarFunda Team'
	values['url'] = 'http://www.bazaarfunda.com'
	template = EmailTemplate(template_name='PriceMovement.html', values=values)	
	msg = MailMessage(from_email='bazaarfunda@gmail.com', to_emails=[values['email']], subject='BazaarFunda Price Alert For You', body=template.render())
	send(mail_msg=msg, mail_server = server)

@celery.task
def priceMovement():	
	server = MailServer(server_name='smtp.gmail.com', username='dude.abhi.chat@gmail.com', password='malesbian', port=0,   require_starttls=True)
	client = getMongoClient('PriceSubscribers')
	priceSubscribers = client.priceSubscribers
	client = getMongoClient('compareDB')
	prices = client.prices
	allUsers = priceSubscribers.find({'status':'A'})
	for user in allUsers:
		user['status'] = 'D'
		values = {}
		productName = user['productName']
		ProductPriceCursor = prices.find({'Model Name':productName})
		productPrice = 100000
		for price in ProductPriceCursor:
			if productPrice > price['ECommercePrice']:
				productPrice = price['ECommercePrice']
		values['ProductName'] = user['productName']
		values['ProductURL'] = 'http://www.bazaarfunda.com/pdp/' + user['productId']
		values['ProductImage'] = 'http://www.bazaarfunda.com/static/img/ImageScrappers/' + user['productName'].replace(' ', '%20') + '.jpg'
		values['ProductPrice'] = productPrice
		values['email'] = user['email']
		print "preparing to sendmail"
		if int(productPrice) < int(user['priceCutOff']):
			print productPrice, user['priceCutOff']
			success = sendEmail.apply_async(args=[values, server])
			print success
			if success:
				priceSubscribers.save(user)
				#current_app.send_task('PriceMovement.sendEmail', args=[values])
				print "sent mail"
priceMovement()
