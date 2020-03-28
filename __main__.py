import os
import sys
import requests
import argparse
from requests.exceptions import Timeout
from datetime import datetime
from dotenv import load_dotenv


def sendEmail(subject, message):
    try:
        requests.post(
            os.getenv('MAILGUN_DOMAIN'),
            auth=("api", os.getenv('MAILGUN_SECRET')),
            data={
                "from": os.getenv('EMAIL_FROM'),
                "to": [os.getenv('EMAIL_TO')],
                "subject": subject,
                "text": message
            }
        )
    except:
        print(f"[{datetime.now()}]: Could not send email with subject: {subject}")

    # create a lock file so that we don't spam ourselves with notification emails
    f = open(os.getenv('LOCK_FILE'), "w")
    f.write("")
    f.close()


def main():
    # read program arguments and environment variables
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--email', type=bool, nargs='?', const=True, default=False,
                        help='Enable notification emails')
    args = parser.parse_args()

    # abort if an opening was found previously
    if args.email:
        try:
            open(os.getenv('LOCK_FILE'))
            print(f"[{datetime.now()}]: Lock file exists, aborting...")
            sys.exit(0)
        except IOError:
            pass

    # set session & "remember-me" cookies
    session = requests.Session()
    jar = requests.cookies.RequestsCookieJar()
    jar.set('SESSION', os.getenv('SESSION'))
    jar.set('remember-me', os.getenv('REMEMBER_ME'))
    session.cookies = jar

    # make GET request to see if a delivery is available
    try:
        r = session.get(os.getenv('URL'), timeout=5)
    except Timeout:
        print(f"[{datetime.now()}]: The request timed out.")
        sys.exit(1)

    # send warning email & terminate if cookies didn't work
    if os.getenv('NOT_LOGGED_IN_KEYWORD') in r.text:
        message = f"[{datetime.now()}]: Invalid session, could not check availability."
        print(message)
        if args.email:
            sendEmail("Invalid Session!", message)
            sys.exit(1)

    # terminate script if it's not available
    if os.getenv('NOT_AVAILABLE_KEYWORD') in r.text:
        print(f"[{datetime.now()}]: Sanalmarket is not available.")
        sys.exit(0)

    # send a notification email if a delivery is available
    message = f'''[{datetime.now()}]: Sanalmarket is now available:\n
        {r.text}\nShopping cart: {os.getenv('SHOPPING_CART_URL')}'''
    print(message)
    if args.email:
        sendEmail("Sanalmarket Available!", message)


if __name__ == '__main__':
    main()
