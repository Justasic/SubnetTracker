__author__ = 'justasic'

from django.db import models

class CIDR(models.Model):
	""" Basic CIDR model to keep track of all the CIDRs
		It's function is really to just manage the name=cidr
		association and store it in the database.
	"""
	name = models.CharField(max_length=255)
	cidr = models.CharField(max_length=20)

	def __unicode__(self):
		return str(self.name).encode('utf-8')