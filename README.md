# ping-sm
This is a script meant to be run periodically as a cron job. It checks if [Migros Sanalmarket](https://www.migros.com.tr/) is available for delivery to your neighborhood in the next 4 days.

### How it works
 * terminates if Sanalmarket isn't available
 * if it is available;
    - sends an email to you using the Mailgun API
    - creates a lock file
    - in the beginning of each execution, if there's a lock file, the script terminates immediately so as to avoid sending lots of emails

### Installing dependencies
```sh
pip3 install -r requirements.txt
```

### Configuraiton
 1. Copy `.env.example` and name the new file as `.env`
 2. Set each variable in `.env` with your own values

### Launching
```sh
# launch manually
python3 ./main.py

# example cron job
* * * * * /usr/bin/python3 /home/utku/git/ping-sm/main.py 2>&1 >> /home/utku/git/ping-sm/log.log
```