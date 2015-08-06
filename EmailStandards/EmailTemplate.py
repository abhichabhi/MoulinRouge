import os
import traceback
import sys

class EmailTemplate():
	dirname = os.path.dirname
	path = dirname(dirname(__file__))
	#modify this to change the Template Directory
	TEMPLATE_DIR = '/templates/'

	def __init__(self, template_name='', values={}, html=True):
		self.template_name = template_name
		self.values = values
		self.html = html
	def render(self):
		content = open(self.path + self.TEMPLATE_DIR + self.template_name).read()
		content = content.decode('utf-8')
		for k,v in self.values.iteritems():
			try:
				content = content.replace('[%s]' % k,str(v))
			except Exception, err:
				print k,v
				print(traceback.format_exc())
		# content = content.encode("ascii")
		return content