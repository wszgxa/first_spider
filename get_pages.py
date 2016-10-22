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
urlTag = ''
urlTitle = ''
urlType = ''
def getRightData(url):
  html = urlopen(url)
  soup = BeautifulSoup(html, 'html.parser', from_encoding="GB18030")
  tag = ()
  try:
    
  return soup.find(class_="co_content8").find(class_='x').find_all('a', text=re.compile(r'^\[(\d{1,5})\]'))

def insertData(data):
  print(data)
  for link in data:
    url = urlTag + link.get('href')
    cur.execute("SELECT * FROM pages WHERE url = %s", (url))
    if cur.rowcount == 0:
      num = re.match(r'^\[(\d{1,5})\]', link.get_text()).group(1)
      cur.execute("INSERT INTO pages(type, kind, pageNum, url) VALUES (%s, %s, %s, %s)", (urlType, urlTitle, num, url))
      conn.commit()
  return (int(re.match(r'^\[(\d{1,5})\]', data[-1].get_text()).group(1)), urlTag + data[-1].get('href'))

def spData(tag):
  cur.execute("INSERT INTO title(title, url, type) VALUES (%s, %s, %s)",
    (urlArray[tag][0], urlArray[tag][1], urlArray[tag][2]))
  conn.commit()
  prevPage = 1
  nextPage = 2
  nextUrl = urlArray[tag][1]
  global urlTag, urlTitle, urlType
  urlTag = urlArray[tag][1].rstrip('index.html')
  urlTitle = urlArray[tag][1][0]
  urlType = urlArray[tag][1][2]
  while nextPage > prevPage:
    prevPage = nextPage
    (nextPage, nextUrl) = insertData(getRightData(nextUrl))
    print('开始抓取' + nextUrl)
  if tag + 1 < len(urlArray):
    spData(tag + 1)
    print('开始抓取' + urlArray[tag + 1])
    tag = tag + 1

cur.execute("SELECT title, url, type FROM title")
urlArray = cur.fetchall()
cur.execute("SELECT title, url, type FROM tag")
if cur.rowcount == 0:
  spData(0)
else:
  tagOne = cur.fetchone()
  if tagOne in urlArray:
    spData(urlArray.index(tagOne))
  else:
    print('错误:tag不再title里面')
# print(hehe)

cur.close()
conn.close()