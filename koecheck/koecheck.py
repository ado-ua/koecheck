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
