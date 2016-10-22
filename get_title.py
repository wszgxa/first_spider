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
  return soup.find(id="menu").find_all('a')[0:8]

def getPureData(data):
  pure = []
  for link in data:
    if re.match(r'^http', link.get('href')):
      pure.append([link.get('href'), link.get_text()])
    else:
      pure.append(['http://www.dytt8.net' + link.get('href'), link.get_text()])
  return pure

def insertData (data):
  for item in data:
    cur.execute("SELECT * FROM title WHERE title = %s", (item[1]))
    if cur.rowcount == 0:
      cur.execute("INSERT INTO title(title, url, type) VALUES (%s, %s, 'dytt8')",
        (item[1], item[0]))
      conn.commit()
  print('success!')

data = getRightData('http://www.dytt8.net/index.html')
pureData = getPureData(data)
insertData(pureData)

cur.close()
conn.close()
# print(pureData)
