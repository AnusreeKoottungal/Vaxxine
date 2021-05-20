import json
import time

import requests
import datetime

from telegram import get_client, send_message

districts = {'ERNAKULAM': 307, 'TRIVANDRUM': 295, 'MALAPPURAM': 310}


def get_subscriptions():
    subscriptions = {}
    with open('subscription.json', 'r') as f:
        subscriptions = json.load(f)
    return subscriptions


def get_next_date():
    return (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")


def get_url(district, date):
    return f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' \
           f'{districts.get(district)}307&date={date}'


def notify_vaccine():
    client = get_client()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'}
    # while True:
    subscriptions = get_subscriptions()
    print(subscriptions)
    curr_date = get_next_date()
    for district_key in districts.keys():
        print('Analyzing ' + district_key)
        url = get_url(district_key, curr_date)
        district_subscriptions = subscriptions.get(district_key, [])
        if len(district_subscriptions) > 0:
            print(district_subscriptions)
            result = {}
            try:
                result = requests.get(url, headers=headers)
            except Exception as e:
                print('Failed to get data from ' + url)
                continue
            if result.status_code == 200:
                centers = result.json().get('centers')
                for center in centers:
                    center_name = center.get('name')
                    sessions = center.get('sessions')
                    for session in sessions:
                        min_age_limit = session.get('min_age_limit')
                        available_capacity_dose1 = session.get('available_capacity_dose1')
                        if available_capacity_dose1 <= 0:
                            failed_string = 'No Slots available in ' + center_name + ' on ' + curr_date
                            print(failed_string)
                        if min_age_limit == 18 and available_capacity_dose1 > 0:
                            success_string = str(
                                available_capacity_dose1) + ' slots available in ' + center_name + ' on ' + \
                                             curr_date + ' for 18-45.'
                            success_string = success_string + '. Goto ' + 'https://selfregistration.cowin.gov.in/'
                            print(success_string)
                            for user in district_subscriptions:
                                if user.get('age_limit', 0) == 18:
                                    send_message(message=success_string, client=client, user_id=user.get('user_id'))

                        if min_age_limit == 45 and available_capacity_dose1 > 0:
                            success_string = str(
                                available_capacity_dose1) + ' slots available in ' + center_name + ' on ' + \
                                             curr_date + ' for 45+'
                            success_string = success_string + '. Goto ' + 'https://selfregistration.cowin.gov.in/'
                            print(success_string)
                            for user in district_subscriptions:
                                if user.get('age_limit', 0) == 45:
                                    send_message(message=success_string, client=client, user_id=user.get('user_id'))
            else:
                print('not found')

        # time.sleep(5)

# notify_vaccine()