import requests
  
msg = 'LINE Notify from tyrcmp.tyc.edu.tw'
# 修改為你的權杖內容
token = 'W4elJYcjhNG6oNypWwMR2r4rS8APoHv8ih5jtcuV5P1'

headers = {
          "Authorization": "Bearer " + token, 
          "Content-Type" : "application/x-www-form-urlencoded"
      }
	
payload = {'message': msg}
r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)

