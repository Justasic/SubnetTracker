"""
    Copyright (C) 2014-2015  Justin Crawford <Justasic@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
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
		return unicode(self.name)

	def CIDROverlaps(self, addr):
		""" This function checks if the CIDR networks or addresses overlap.

			addr - takes a string (preferably Unicode) of the CIDR network mask or
					an ipaddress.IPv4Network object.
		"""
		if isinstance(addr, IPv4Network):
			return addr.overlaps(IPv4Network(unicode(self.cidr)))
		else:
			return IPv4Network(unicode(addr)).overlaps(IPv4Network(unicode(self.cidr)))
