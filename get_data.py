#!/usr/bin/env python3
#coding=utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pymysql
from config import dbUser, dbPassword, db
conn = pymysql.connect(host='127.0.0.1', unix_socket='/var/run/mysqld/mysqld.sock',user=
                      dbUser, passwd=dbPassword, db=db, charset='utf8')
cur = conn.cursor()
cur.execute("USE "+ db)

def getData(url):
  print(url)
  html = urlopen(url)
  soup = BeautifulSoup(html, 'html5lib', from_encoding="GB18030")
  return soup.find_all('a', class_='ulink',href=re.compile(r'[0-9]+.html$'))

def getPage(tag, listNum, tt):
  return urlArray[tag][1].rstrip('index.html') + 'list_' + listNum +'_' + str(tt)+'.html'
def getGoodData(tag, url):
  print(url)
  cur.execute("SELECT * FROM data WHERE url = %s", (url))
  if cur.rowcount == 0:
    sourecType = urlArray[tag][0]
    kind = urlArray[tag][2]
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html5lib', from_encoding="GB18030")
    content = ''
    try:
    	content = soup.find(class_='co_content8').find('p').prettify()
    except :
    	content = 'not found'
    cur.execute("INSERT INTO data(type, kind, url, title, content, magnetic) VALUES (%s, %s, %s, %s, %s, %s)",
      (
        sourecType,
        kind,
        url,
        soup.find('h1').find('font').get_text(),
        content,
        soup.find(class_='co_content8').find('a', href=re.compile(r'^ftp://[/s/S]*')).get('href')
        ))
    print(soup.find(class_='co_content8').find('a', href=re.compile(r'^ftp://[/s/S]*')).get('href'))
    conn.commit()
def spData(tag, pageCount):
  sourecType = urlArray[tag][0]
  kind = urlArray[tag][2]
  listTag = urlArray[tag][3]
  tt = 0
  while tt < 2:
    linkList = getData(getPage(tag, listTag, pageCount))
    if not linkList:
      tt = tt + 1
      pageCount = pageCount + 1
      cur.execute("UPDATE tagNum SET pageCount = %s WHERE id = 1", (pageCount))
      conn.commit()
      continue
    pageCount = pageCount + 1
    cur.execute("UPDATE tagNum SET pageCount = %s WHERE id = 1", (pageCount))
    conn.commit()
    for item in linkList:
      try:
        getGoodData(tag, kind[0:len(kind)-1]+item.get('href'))
      except:
        print('获取'+item.get('href')+"数据出错")
  if tag+1 < len(urlArray):
    print('爬取下个类型')
    cur.execute("UPDATE tagNum SET tag = %s WHERE id = 1", (tag+1))
    conn.commit()
    spData(tag+1, 0)

cur.execute("SELECT title, url, type, listTag  FROM title")
urlArray = cur.fetchall()
cur.execute("SELECT tag, pageCount FROM tagNum")
hiTag = cur.fetchall()[0]
spData(int(hiTag[0]), int(hiTag[1]))

cur.close()
conn.close()
print(urlArray)