import requests
import sys
import time
import json
from py_console import console
from bs4 import BeautifulSoup


class BaseRequest:
    
   username = ''
   password = ''
   timeout = int
   visitUrl = 'http://httpbin.org/ip'
   loginUrl = 'http://172.16.10.20:1000'
   
   def __init__(self, username, password, timeout=1200):
        self.username = username
        self.password = password
        self.timeout = timeout
    
   def login(self, lUrl=loginUrl):
        '''
        perform the logout on the current session
        then login again
        '''
        username = self.username
        password = self.password
        visitUrl = self.visitUrl
        try:
            requests.get(lUrl+'/logout?0')
        except Exception as e:
            console.warn('no previous session')
        try:
            nextUrl = requests.get(visitUrl)
            nextUrl = nextUrl.text[59:108]
            loginData = requests.get(nextUrl)
            soup = BeautifulSoup(loginData.text, 'html.parser')
            magicToken = soup.find('input', {'name':'magic'})['value']  
            jsonData = {
                    'username':f'{username}',
                    'password':f'{password}',
                    'magic':f'{magicToken}'
                     }
            requests.post(nextUrl, data=jsonData)
            console.success("great success!")
            return
        except Exception as e:
            print(e)
            console.error('Login Failed!')

def checkCreds():
    config = open('./config.json', 'r')
    jsonConfig = json.load(config)
    config.close()
    if(jsonConfig['username'] == '' or jsonConfig['password'] == ''):
        console.error('Supply username and password in config.json')
        sys.exit(0)
    username = jsonConfig['username']
    password = jsonConfig['password']
    return username, password

def main():
    username, password = checkCreds()
    br = BaseRequest(username, password)
    while(1):
        br.login()
        time.sleep(br.timeout)

if(__name__ == "__main__"):
    main()
        
