# importing all required libraries
from telethon import TelegramClient, sync, events
from telethon import utils
# get your api_id, api_hash, token
# from telegram as described above
api_id = '5367299'
api_hash = '8ff2358ef3c20de3bca2bf5ffbcb9dfd'
token = '1732626920:AAH9ar3USEHyHsVApvx4f5NJnx8QFJdfqoo'

# your phone number
phone = '+919790986756'


# creating a telegram session and assigning
# it to a variable client
def get_client():
    client = TelegramClient('session', api_id, api_hash)

    # connecting and building the session
    client.connect()

    # in case of script ran first time it will
    # ask either to input token or otp sent to
    # number or sent or your telegram id
    if not client.is_user_authorized():
        client.send_code_request(phone)

        # signing in the client
        client.sign_in(phone, input('Enter the code: '))
    print('Telegram connected successfully')
    return client


def send_message(user_id, client, message):
    try:
        # receiver user_id and access_hash, use
        # my user_id and access_hash for reference
        entity = client.get_input_entity(user_id)
        # receiver = InputPeerUser('user_id', 'user_hash')
        receiver = utils.get_input_user(entity)
        # sending message using telegram client
        client.send_message(receiver, message, parse_mode='html')
    except Exception as e:

        # there may be many error coming in while like peer
        # error, wwrong access_hash, flood_error, etc
        print(e)

# disconnecting the telegram session
# client.disconnect()
