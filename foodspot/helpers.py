from django.utils.deconstruct import deconstructible
import os
from uuid import uuid4


@deconstructible
def PathAndRenameFile(object):
	def __init__(self, path):
		self.path = path
	def __call__(self, instance, filename):
		extension = filename.split('.')[-1]
		filename = '{}.{}'.format(uuid4().hex, extension)
		print self.path
		print "Hello"
		return os.path.join('foodspots', filename)

	
