# ping-sm
Run this script periodically as a cron job. It checks if [Migros Sanalmarket](https://www.migros.com.tr/) is available for delivery to your neighborhood in the next 4 days.


## How it works
 * terminates sends you a warning email if session is invalid
 * terminates if a delivery isn't available
 * sends you a notification email if a delivery is available

#### Email Notifications
You need a Mailgun domain to enable notification emails. You'll have to rely on logs otherwise.

## Installing dependencies
```sh
pip3 install -r requirements.txt
```

## Configuraiton
 1. Copy `.env.example` and name the new file as `.env`
 2. Set each variable in `.env` with your own values. Find out your `SESSION` & `remember-me` cookies using the developer tools of your favorite browser

## Launching
```sh
# launch manually
python3 ./__main__.py

# launch manually with notification emails enabled
python3 ./__main__.py --email

# example cron job
* * * * * /usr/bin/python3 /home/utku/git/ping-sm/__main__.py --email 2>&1 >> /home/utku/git/ping-sm/log.log
```