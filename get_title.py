#!/usr/bin/env python 
#coding=utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pymysql
from config import dbUser, dbPassword, db
conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',user=
                      dbUser, passwd=dbPassword, db=db, charset='utf8')
cur = conn.cursor()
cur.execute("USE "+ db)

def getRightData(url):
  html = urlopen(url)
  soup = BeautifulSoup(html, 'html.parser', from_encoding="GB18030")
  return soup.find(id="menu").find_all('a')[0:10]

def getPureData(data):
  pure = []
  for link in data:
    if re.match(r'^http', link.get('href')):
      pure.append([link.get('href'), link.get_text(), 'http://www.ygdy8.net/'])
    else:
      pure.append(['http://www.dytt8.net' + link.get('href'), link.get_text(), 'http://www.dytt8.net/'])
  return pure
def getListTag(url):
  print(url)
  html = urlopen(url)
  soup = BeautifulSoup(html, 'html.parser', from_encoding="GB18030")
  try:
    tag = soup.find(class_="co_content8").find(class_='x').find('a', text=re.compile(r'^\[(\d{1,5})\]')).get('href')
  except:
    return 0
  tt = re.match(r'^list_(\d{1,4})_\d.html', tag)
  return tt.group(1)

def insertData (data):
  for item in data:
    cur.execute("SELECT * FROM title WHERE title = %s", (item[1]))
    if cur.rowcount == 0:
      listTag = getListTag(item[0])
      if listTag == 0:
        continue
      cur.execute("INSERT INTO title(title, url, type, listTag) VALUES (%s, %s, %s, %s)",
        (item[1], item[0], item[2], listTag))
      conn.commit()
  print('success!')

data = getRightData('http://www.dytt8.net/index.html')
pureData = getPureData(data)
insertData(pureData)

cur.close()
conn.close()
