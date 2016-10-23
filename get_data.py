#!/usr/bin/env python3
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

def getData(url):
  print(url)
  html = urlopen(url)
  soup = BeautifulSoup(html, 'html5lib', from_encoding="GB18030")
  print(soup)
  return soup.find_all('a', class_='ulink')

def getPage(tag, listNum, tt):
  return urlArray[tag][1].rstrip('index.html') + 'list_' + listNum +'_' + str(tt)+'.html'
def getGoodData(tag, url):
  sourecType = urlArray[tag][0]
  kind = urlArray[tag][2]
  html = urlopen(url)
  soup = BeautifulSoup(html, 'html5lib', from_encoding="GB18030")
  cur.execute("INSERT INTO data(type, kind, url, title, content, magnetic) VALUES (%s, %s, %s, %s, %s, %s)",
    (
      sourecType,
      kind,
      url,
      soup.find('h1').find('font').get_text(),
      soup.find(class_='co_content8').find('p').get_text(),
      soup.find(class_='co_content8').find('a').get('href')
      ))
  conn.commit()
def spData(tag):
  sourecType = urlArray[tag][0]
  kind = urlArray[tag][2]
  listTag = urlArray[tag][3]
  pageCount = 1
  tt = 0
  while tt < 2:
    linkList = getData(getPage(tag, listTag, pageCount))
    if not linkList:
      tt = tt + 1
      pageCount = pageCount + 1
      continue
    for item in linkList:
      try:
        getGoodData(tag, kind[0:len(kind)-1]+item.get('href'))
      except:
        print('获取'+item.get('href')+"数据出错")
  if tag+1 < len(urlArray):
    spData(tag+1)

cur.execute("SELECT title, url, type, listTag  FROM title")
urlArray = cur.fetchall()
cur.execute("SELECT title, url, type, listTag FROM tag")

if cur.rowcount == 0:
  spData(0)
else:
  tagOne = cur.fetchone()
  if tagOne in urlArray:
    spData(urlArray.index(tagOne))
  else:
    print('错误:tag不再title里面')
print(urlArray)