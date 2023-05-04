#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3

"""
This script demonstrates how to use the Venmo API to obtain an access token
using your Venmo email and password.

To use this script, you must first create a config.ini file with your Venmo
email and password. Never commit your credentials or token to a git repository.
"""

from venmo_api import Client
import configparser
import datetime

# Read your config file
config = configparser.ConfigParser()
config.read('config.ini')

user_email = config.get('Venmo', 'Email')
user_password = config.get('Venmo', 'Password')

# Get your access token. You will need to complete the 2FA process
access_token = Client.get_access_token(
    username=user_email, password=user_password)

# Initialize your client
client = Client(access_token=access_token)
user = client.user.get_my_profile()

# Define the start and end times for the time frame you want to retrieve payment requests for
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=7)

# Get the first page of the user's transaction history
transactions = client.user.get_user_transactions(
    user_id=user.id)

while transactions:
    for transaction in transactions:
        date_completed = datetime.datetime.fromtimestamp(
            transaction.date_completed)
        if date_completed >= start_time:
            print(f"Transaction: {transaction}")
        else:
            transactions = None
            exit

    print("\n" + "=" * 15 + "\n\tNEXT PAGE\n" + "=" * 15 + "\n")
