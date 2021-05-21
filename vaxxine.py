import json
import time

import requests
import datetime

from telegram import get_client, send_message
from utils import print_with_date

districts = {'ERNAKULAM': 307, 'TRIVANDRUM': 296, 'MALAPPURAM': 302}

last_requested_datetime = datetime.datetime.now()


def get_api_response(url, headers):
    global last_requested_datetime
    print_with_date(f'Requesting API{url}')
    difference = (datetime.datetime.now() - last_requested_datetime).total_seconds()
    if difference < 4:
        time.sleep(int(4 - difference))
    r = requests.get(url, headers=headers)
    last_requested_datetime = datetime.datetime.now()
    print_with_date(f'Response for API {url} is {r.status_code}')
    return r


def get_subscriptions():
    subscriptions = {}
    with open('subscription.json', 'r') as f:
        subscriptions = json.load(f)
    return subscriptions


def get_next_date():
    return (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")


def get_url(district, date):
    return f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' \
           f'{districts.get(district)}&date={date}'


def notify_vaccine():
    client = get_client()
    notified_sessions = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'}
    while True:
        subscriptions = get_subscriptions()
        curr_date = get_next_date()
        for district_key in districts.keys():
            url = get_url(district_key, curr_date)
            district_subscriptions = subscriptions.get(district_key, [])
            if len(district_subscriptions) > 0:
                result = {}
                try:
                    result = get_api_response(url, headers)
                except Exception as e:
                    print_with_date('Failed to get data from ' + url)
                    continue
                if result.status_code == 200:
                    centers = result.json().get('centers')
                    # centers = [
                    #     {"center_id": 155472, "name": "Mazhuvannoor PHC", "address": "VadavucodeErnakulamKeralaIN",
                    #      "state_name": "Kerala", "district_name": "Ernakulam", "block_name": "Vadavucode CHC",
                    #      "pincode": 683541, "lat": 10, "long": 76, "from": "09:00:00", "to": "14:00:00",
                    #      "fee_type": "Free", "sessions": [
                    #         {"session_id": "e8f2f714-7609-4347-973b-644a91783348", "date": "21-05-2021",
                    #          "available_capacity": 10, "min_age_limit": 45, "vaccine": "COVISHIELD",
                    #          "slots": ["09:00AM-10:00AM", "10:00AM-11:00AM", "11:00AM-12:00PM", "12:00PM-02:00PM"],
                    #          "available_capacity_dose1": 0, "available_capacity_dose2": 15}]},
                    #     {"center_id": 155363, "name": "Fortkochi THQH",
                    #      "address": "Fortkochi THQH Cochi Ernakulam KeralaIN", "state_name": "Kerala",
                    #      "district_name": "Ernakulam", "block_name": "Kumbalangi CHC", "pincode": 682001, "lat": 9,
                    #      "long": 76, "from": "09:00:00", "to": "16:00:00", "fee_type": "Free", "sessions": [
                    #         {"session_id": "a787cc6e-1b9d-4a99-85d2-e68605c26d9b", "date": "21-05-2021",
                    #          "available_capacity": 10, "min_age_limit": 45, "vaccine": "COVISHIELD",
                    #          "slots": ["09:00AM-11:00AM", "11:00AM-01:00PM", "01:00PM-03:00PM", "03:00PM-04:00PM"],
                    #          "available_capacity_dose1": 0, "available_capacity_dose2": 25}]},
                    #     {"center_id": 155192, "name": "Alangad PHC", "address": "VarappuzhaErnakulamKeralaIN",
                    #      "state_name": "Kerala", "district_name": "Ernakulam", "block_name": "Varappuzha CHC",
                    #      "pincode": 683518, "lat": 10, "long": 76, "from": "09:00:00", "to": "14:00:00",
                    #      "fee_type": "Free", "sessions": [
                    #         {"session_id": "7f5133c2-4b22-42b4-879b-0c56e32f0fa6", "date": "21-05-2021",
                    #          "available_capacity": 10, "min_age_limit": 45, "vaccine": "COVISHIELD",
                    #          "slots": ["09:00AM-10:00AM", "10:00AM-11:00AM", "11:00AM-12:00PM", "12:00PM-02:00PM"],
                    #          "available_capacity_dose1": 0, "available_capacity_dose2": 29}]},
                    #     {"center_id": 155393, "name": "Kadayiruppu CHC", "address": "VadavucodeErnakulamKeralaIN",
                    #      "state_name": "Kerala", "district_name": "Ernakulam", "block_name": "Vadavucode CHC",
                    #      "pincode": 682311, "lat": 10, "long": 76, "from": "09:00:00", "to": "14:00:00",
                    #      "fee_type": "Free", "sessions": [
                    #         {"session_id": "6d63c3bc-329b-44b5-b1a1-4f0bb0aa28d7", "date": "21-05-2021",
                    #          "available_capacity": 10, "min_age_limit": 45, "vaccine": "COVISHIELD",
                    #          "slots": ["09:00AM-10:00AM", "10:00AM-11:00AM", "11:00AM-12:00PM", "12:00PM-02:00PM"],
                    #          "available_capacity_dose1": 0, "available_capacity_dose2": 56}]},
                    #     {"center_id": 561681, "name": "Aster Medcity Hospital",
                    #      "address": "Aster Dm Healthcare Ltd Kuttisahib Road Cheranelloor South Chittoor Kochi Kerala",
                    #      "state_name": "Kerala", "district_name": "Ernakulam", "block_name": "Cheranalloor PHC",
                    #      "pincode": 682027, "lat": 10, "long": 76, "from": "09:00:00", "to": "17:00:00",
                    #      "fee_type": "Paid", "sessions": [
                    #         {"session_id": "3328c6c0-6d6b-435e-a517-25fc9617c206", "date": "21-05-2021",
                    #          "available_capacity": 10, "min_age_limit": 18, "vaccine": "COVAXIN",
                    #          "slots": ["09:00AM-11:00AM", "11:00AM-01:00PM", "01:00PM-03:00PM", "03:00PM-05:00PM"],
                    #          "available_capacity_dose1": 0, "available_capacity_dose2": 69},
                    #         {"session_id": "1407ab6b-66cf-4171-892e-0cd74148d832", "date": "21-05-2021",
                    #          "available_capacity": 0, "min_age_limit": 45, "vaccine": "COVAXIN",
                    #          "slots": ["09:00AM-11:00AM", "11:00AM-01:00PM", "01:00PM-03:00PM", "03:00PM-05:00PM"],
                    #          "available_capacity_dose1": 0, "available_capacity_dose2": 89}],
                    #      "vaccine_fees": [{"vaccine": "COVAXIN", "fee": "1250"}]},
                    #     {"center_id": 569943, "name": "GMTH Karuvelipadi Hospital",
                    #      "address": "Moulana Azad Rd Karuvelipady Thoppumpady Kochi Kerala", "state_name": "Kerala",
                    #      "district_name": "Ernakulam", "block_name": "Kumbalangi CHC", "pincode": 682005, "lat": 9,
                    #      "long": 76, "from": "09:00:00", "to": "16:00:00", "fee_type": "Free", "sessions": [
                    #         {"session_id": "aee618e4-b082-4fd6-bd9d-77f0c4b7d7dd", "date": "21-05-2021",
                    #          "available_capacity": 0, "min_age_limit": 45, "vaccine": "COVAXIN",
                    #          "slots": ["09:00AM-11:00AM", "11:00AM-01:00PM", "01:00PM-03:00PM", "03:00PM-04:00PM"],
                    #          "available_capacity_dose1": 0, "available_capacity_dose2": 43}]}]
                    for center in centers:
                        center_name = center.get('name')
                        sessions = center.get('sessions')
                        for session in sessions:
                            min_age_limit = session.get('min_age_limit')
                            available_capacity = session.get('available_capacity')
                            if available_capacity <= 0:
                                failed_string = 'No Slots available in ' + center_name + ' on ' + session.get('date')
                                print_with_date(failed_string)
                            if min_age_limit == 18 and available_capacity > 0:
                                success_string = str(
                                    available_capacity) + ' slots available in ' + center_name + ' on ' + \
                                                 session.get('date') + ' for 18-45.'
                                success_string = success_string + '. Goto ' + 'https://selfregistration.cowin.gov.in/'
                                print_with_date(success_string)
                                for user in district_subscriptions:
                                    user_notified_sessions = notified_sessions.get(user.get('user_id'), [])
                                    if user.get('age_limit', 0) == 18 and \
                                            session.get('session_id') not in user_notified_sessions:
                                        user_notified_sessions.append(session.get('session_id'))
                                        notified_sessions.update({user.get('user_id'):
                                                                      user_notified_sessions})
                                        send_message(message=success_string, client=client, user_id=user.get('user_id'))

                            if min_age_limit == 45 and available_capacity > 0:
                                success_string = str(
                                    available_capacity) + ' slots available in ' + center_name + ' on ' + \
                                                 session.get('date') + ' for 45+'
                                success_string = success_string + '. Goto ' + 'https://selfregistration.cowin.gov.in/'
                                print_with_date(success_string)
                                for user in district_subscriptions:
                                    user_notified_sessions = notified_sessions.get(user.get('user_id'), [])
                                    if user.get('age_limit', 0) == 45 and \
                                            session.get('session_id') not in user_notified_sessions:
                                        user_notified_sessions.append(session.get('session_id'))
                                        notified_sessions.update({user.get('user_id'):
                                                                 user_notified_sessions})
                                        send_message(message=success_string, client=client, user_id=user.get('user_id'))
                else:
                    print_with_date(f'Unable to get data from api {result.status_code}')
