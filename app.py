from flask import Flask, request, jsonify
import jwt
import requests
import json
from time import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from datetime import date 
import time
import urllib.request
import os


app = Flask(__name__)

@app.route('/api',methods=['GET'])

def hello_world():
    platform = str(request.args['platform'])
    if platform=="zoom":
        topic = str(request.args['topic'])
        duration = str(request.args['duration'])
        JWT_TOKEN = str(request.args['JWT_TOKEN'])

        temp = str(request.args['start_time'])
        temp = temp[:-4]
        start_time = temp.replace(" ","T")
        
        print("##############")
        print(temp)
        print("##############")
        
        d = {}
        meetingdetails = {"topic": topic,
                    "type": 2,
                    "start_time": start_time,
                    "duration": duration,
                    "timezone": "Asia/Calcutta",
                    "agenda": "test",
                    "recurrence": {"type": 1,
                                    "repeat_interval": 1
                                    },
                    "settings": {"host_video": "False",
                                "participant_video": "False",
                                "join_before_host": "true",
                                "mute_upon_entry": "False",
                                "watermark": "true",
                                "audio": "voip",
                                "auto_recording": "cloud"
                                }
                    }
        
        headers = {'authorization': 'Bearer {}'.format(JWT_TOKEN),'content-type': 'application/json'}
        r = requests.post(f'https://api.zoom.us/v2/users/me/meetings', headers=headers, data=json.dumps(meetingdetails))
        print("\n Creating Zoom Meeting.... \n")
        print(r.text)

        y = json.loads(r.text)
        try:
            join_URL = y["join_url"]
            meetingPassword = y["password"]
        
            d['status']="true"
            d['link']=join_URL
            d['password']=meetingPassword 
        except:
            d['status']="false"
            d['message']=y['message']

        response = jsonify(d)
        response.headers.add("Access-Control-Allow-Origin", "*") 
        return response

    elif platform=="gmeet":
        d = {}
        # try:
        #     d['status']="true"
        #     d['link']="meet.google.dummylink.com"
        # except:
        #     d['status']="false"

        


        try:
            opt = webdriver.ChromeOptions()
            opt.add_argument("user-data-dir=C:/Users/{}/AppData/Local/Google/Chrome/User Data".format(os.getlogin()))
            opt.add_argument("--start-maximized")

            gmeetUrl = "https://meet.google.com"
            driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=opt)
            driver.get(gmeetUrl)

            newMeetingButton = driver.find_element_by_css_selector("body#yDmH0d>c-wiz>div>div:nth-of-type(2)>div>div>div:nth-of-type(3)>div>div>div>div>button>div:nth-of-type(3)")
            driver.execute_script("arguments[0].click();", newMeetingButton)

            scheduleMeetingButton = driver.find_element_by_xpath("//span[@class='VfPpkd-BFbNVe-bF1uUb NZp2ef']/following-sibling::li[1]")
            driver.execute_script("arguments[0].click();", scheduleMeetingButton)

            time.sleep(10)
            copyButton = driver.find_element_by_xpath("//div[@class='acuQXc']//div")
            d['status']="true"
            d['link'] = copyButton.text
        except:
            d['status']="fail"
        
        
        response = jsonify(d)
        response.headers.add("Access-Control-Allow-Origin", "*") 
        return response

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
