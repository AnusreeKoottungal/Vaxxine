import time

import requests
import datetime

from telegram import get_client, send_message

url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=307&date='
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
client = get_client()
while True:
    currDate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
    url = url + currDate
    result = requests.get(url, headers=headers)
    if result.status_code == 200:
        centers = result.json().get('centers')
        for center in centers:
            centerName = center.get('name')
            sessions = center.get('sessions')
            for session in sessions:
                min_age_limit = session.get('min_age_limit')
                available_capacity_dose1 = session.get('available_capacity_dose1')
                if available_capacity_dose1 <= 0:
                    failedString = 'No Slots available in ' + centerName + ' on ' + currDate
                    print(failedString)
                if min_age_limit == 18 and available_capacity_dose1 > 0:
                    successString = str(available_capacity_dose1) + ' slots available in ' + centerName + ' on ' + currDate + ' for 18-45.'
                    successString = successString + '. Goto ' + 'https://selfregistration.cowin.gov.in/'
                    print(successString)
                    send_message(message=successString, client=client, user_id='@johnsabujohn')

                if min_age_limit == 45 and available_capacity_dose1 > 0:
                    successString = str(available_capacity_dose1) + ' slots available in ' + centerName + ' on ' + currDate + ' for 45+'
                    successString = successString + '. Goto ' + 'https://selfregistration.cowin.gov.in/'
                    print(successString)
                    send_message(message=successString, client=client, user_id='@johnsabujohn')
    else:
        print('not found')

    time.sleep(5)
