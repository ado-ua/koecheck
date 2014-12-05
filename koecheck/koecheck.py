# This Python file uses the following encoding: utf-8

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

import urllib2
import urllib
import time
from datetime import date

'''
 Options for script
'''
location = 'Вишеньки'  # Location in which we are interested in.
rp = 'Бориспільський РП'  # Our centre
date_to = default = '' + str(
    date.fromtimestamp(time.time()).strftime('%Y/%m/%d'))  # Till which date to search, currently till today
date_from = '' + str(
    date.fromtimestamp(time.time() - 4320000).strftime('%Y/%m/%d'))  # From which date, currently today - 20 days


def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif (c == '"' or c == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + c

    return out


def check_blackout(end_date, from_date, centre_name, name):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'cookiename=cookievalue'))
    url = 'http://www.koe.vsei.ua/koe/index.php?page=76&ok=1'
    data = {'d_end': end_date, 'd_f': from_date, 'rp': centre_name.decode('utf8').encode('cp1251')}
    data_encoded = urllib.urlencode(data)
    f = opener.open(url, data_encoded)
    result = []
    event_date = ''

    content = f.read().decode('cp1251').encode('utf8')
    content = content.splitlines()
    for line in content:
        if 'background:#efefde' in line:
            sub_line = ' '.join(line.split()).split('</tr>')
            for part in sub_line:
                if part.startswith('<tr><td '):
                    event_date = part.replace('<tr><td colspan=7 style=\'background:#efefde\'><center><b>', '').replace(
                        '</b></center></td>', '')
                else:
                    if name in part:
                        data = part.replace('<tr><td>', '').split('</td><td>')
                        out = {'Date': event_date, 'Районний підрозділ': data[0], 'Населенний пункт': data[1],
                               'Вулиця': data[2], 'Відкл.уст.': data[3], 'Роботи': data[4],
                               'Час': data[5].replace('</td>', '')}
                        result.append(out)

    return result


if __name__ == '__main__':
    output = check_blackout(date_to, date_from, rp, location)

    for date in output:
        print '\n'
        print 'Дата: ', date.get('Date')
        print 'Районний підрозділ: ', date.get('Районний підрозділ')
        print 'Населенний пункт:', date.get('Населенний пункт')
        print 'Вулиця: ', date.get('Вулиця')
        print 'Відкл.уст.: ', date.get('Відкл.уст.')
        print 'Роботи: ', date.get('Роботи')
        print 'Час: ', date.get('Час')