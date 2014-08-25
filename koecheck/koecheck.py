"""
Script to check planned electricity disconnections in Kiyv area
Copyright (C) 2014 ado-ua

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

# This Python file uses the following encoding: utf-8

import urllib2
import urllib
from BeautifulSoup import BeautifulSoup

opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'cookiename=cookievalue'))
d_end = '2014/08/29'
d_f = '2014/08/20'
rp = 'Бориспільський РП'
data = {'d_end' : d_end, 'd_f' : d_f, 'rp' : rp.decode('utf8').encode('cp1251')}
#opener.add_data(data)
data_encoded = urllib.urlencode(data)
f = opener.open("http://www.koe.vsei.ua/koe/index.php?page=76&ok=1",data_encoded)

content = f.read()
soup = BeautifulSoup(content.decode('cp1251').encode('utf8'))

for turnoff in soup('td','colspan=7'):
    print turnoff.contents[:3]
print soup
