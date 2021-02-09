import os, subprocess, select
import time, re
import smtplib
import logging

logging.basicConfig(filename="/var/log/sshudo_alert.log", level=logging.DEBUG, format='%(levelname)s:%(asctime)s:%(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
EMAIL_ADDRESS = os.environ.get("EMAIL")
EMAIL_PASSWORD = os.environ.get("PASS")

def poll_logfile(logfile):
  logline = subprocess.Popen(["tail", "-F", "-n", "0", logfile], encoding="utf8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  p = select.poll()
  p.register(logline.stdout)

  while True:
    if p.poll(1):
      prepare_data(logline.stdout.readline())
    time.sleep(1)

def prepare_data(logline):
	if ("ssh" and "Accepted" in logline):
	  	subject = "SSH Login Alert"
	  	send_email(subject, logline)
	elif ("sudo" and "COMMAND" in logline):
		subject = "Sudo Use Alert"
		send_email(subject, logline)

def send_email(subject, body):
	try:
		with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
			smtp.ehlo()
			smtp.starttls()
			smtp.ehlo()

			smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

			msg = f"Subject: {subject}\n\n{body}"

			smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
			logging.info(f" email successfully sent")
	except Exception as e:
		logging.error(f" failed to send email, exception raised: {e}")

if __name__ == "__main__":
	if (EMAIL_ADDRESS is not None and EMAIL_PASSWORD is not None):
		if (re.search("[a-z0-9\.]+@[a-z0-9]+\.com", EMAIL_ADDRESS)):
			poll_logfile("/var/log/auth.log")
		else:
			logging.error(f" login credentials are not valid")
			exit()
	else:
		logging.error(f" login credentials not found")
		exit()
