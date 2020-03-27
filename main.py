import os
import sys
import requests
from requests.exceptions import Timeout
from datetime import datetime
from dotenv import load_dotenv

timestamp = datetime.now()

# read environment variables
try:
    load_dotenv()
    URL = os.getenv('URL')
    SHOPPING_CART_URL = os.getenv('SHOPPING_CART_URL')
    KEYWORD = os.getenv('KEYWORD')
    SESSION = os.getenv('SESSION')
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
    MAILGUN_SECRET = os.getenv('MAILGUN_SECRET')
    EMAIL_FROM = os.getenv('EMAIL_FROM')
    EMAIL_TO = os.getenv('EMAIL_TO')
    LOCK_FILE = os.getenv('LOCK_FILE')
except:
    print(f"[{timestamp}]: Could not read environment variables.")
    sys.exit(1)

# abort if an opening was found previously
try:
    open(LOCK_FILE)
    print(f"[{timestamp}]: Lock file exists, aborting...")
    sys.exit(0)
except IOError:
    pass

# set session cookie
session = requests.Session()
jar = requests.cookies.RequestsCookieJar()
jar.set('SESSION', SESSION)
session.cookies = jar

# make GET request to see if there's an opening
try:
    r = session.get(URL, timeout=5)
except Timeout:
    print(f"[{timestamp}]: The request timed out.")
    sys.exit(1)

# terminate script if it's not available
if KEYWORD in r.text:
    print(f"[{timestamp}]: Sanalmarket is not available.")
    sys.exit(0)

# send a notification email if available
message = f"[{timestamp}]: Sanalmarket is now available yay! Go to: {SHOPPING_CART_URL}"
print(message)
requests.post(
    MAILGUN_DOMAIN,
    auth=("api", MAILGUN_SECRET),
    data={
        "from": EMAIL_FROM,
        "to": [EMAIL_TO],
        "subject": "Sanalmarket Available!",
        "text": message
    }
)

# create a lock file so that we don't spam ourselves with notification emails
f = open(LOCK_FILE, "w")
f.write("Found an opening!")
f.close()
