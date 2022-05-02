import requests
from connectDB import getSubnet
'''
ip='127.0.0.1'
data, to_mail, to_line, mail_no, line_no = getSubnet(ip)
print(data)
to_chat=[]
to_line=''.join(to_line.split())
to_line = to_line.split(',')
for chat in to_line:
    to_chat.append(chat)
print(to_chat)
'''
msg = 'LINE Notify from tyrcmp.tyc.edu.tw'
# 修改為你的權杖內容
token = 'W4elJYcjhNG6oNypWwMR2r4rS8APoHv8ih5jtcuV5P1'

headers = {
          "Authorization": "Bearer " + token, 
          "Content-Type" : "application/x-www-form-urlencoded"
      }
	
payload = {'message': msg}

r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)

