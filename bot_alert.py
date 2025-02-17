import requests
import json
import psycopg2
import datetime

def sendmessage(m,u):
    headers = {
                'content-type':
                'application/json',
                'Authorization':'Bearer '+token
               }
    formData = {
        "to": u,
        "messages":[
            {
                "type":"text",
                "text":m
            }
        ]
      }

    r = requests.post(url, headers=headers , data = json.dumps(formData, indent=4))
    print(r.text)

h = "165.232.164.140"
db = "postgres"
us = "postgres"
pw = "your password"
conn = psycopg2.connect(host = h,database  = db ,user =us ,password =pw ,port=5432)
cur = conn.cursor()


url = 'https://api.line.me/v2/bot/message/push'
token = 'TOKEN LINE' 

now = datetime.datetime.now()
tomorrow = datetime.datetime(now.year,now.month,now.day+1)
cur.execute("SELECT * FROM HOMEWORKS WHERE DEADLINE = '"+tomorrow.strftime("%Y-%m-%d")+"'")
rows = cur.fetchall()
print(tomorrow.strftime("%Y-%m-%d"))
if len(rows) > 0 :
    for row in rows:
        if row[2] != None:
            m = "Subject : "+row[1]+"\nNote : "+row[2]+"\nDeadline : "+str(row[3])
        else:
            m = "Subject : "+row[1]+"\nDeadline : "+str(row[3])
        sendmessage(m,row[0])
        cur.execute("DELETE FROM HOMEWORKS WHERE DEADLINE = '"+tomorrow.strftime("%Y-%m-%d")+"'")

conn.commit()
conn.close()
