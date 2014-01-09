__author__ = 'justasic'

from django.db import models
from ipaddress import IPv4Network

class CIDR(models.Model):
	""" Basic CIDR model to keep track of all the CIDRs
		It's function is really to just manage the name=cidr
		association and store it in the database.

		The class also uses the 'ipaddress' library to compare
		CIDR masks to itself.
	"""
	name = models.CharField(max_length=255)
	cidr = models.CharField(max_length=20)

	def __unicode__(self):
		return str(self.name).encode('utf-8')

	def CIDROverlaps(self, addr):
		""" This function checks if the CIDR networks or addresses overlap.

			addr - takes a string (preferably Unicode) of the CIDR network mask or
					an ipaddress.IPv4Network object.
		"""
		if isinstance(addr, IPv4Network):
			return addr.overlaps(IPv4Network(self.cidr.encode('utf-8')))
		else:
			return IPv4Network(addr.encode('utf-8')).overlaps(IPv4Network(self.cidr.encode('utf-8')))