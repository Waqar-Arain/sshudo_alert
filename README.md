# sshudo_alert

Systemd service that send gmail alerts when someone ssh into or use sudo on the machine.

Note: I have used same email to send and recieve email, you can change that if you want.

## How to install

### Step 1 (Credentials)

- Store your gmail credentials into `vars.env` file
- Make sure to enable 'Less secure app access' on your gmail account so that this python script can use your credentials to send email

### Step 2 (Files)

- Service file
	- make sure that you update path (full home path) with yours on line 9 and 10 in `sshudo.service` file
	- `chmod 644 ~/.sshudo/sshudo.service` and `chown root:root ~/.sshudo/sshudo.service`
	- move sshudo.service to `/etc/systemd/system/`
- Permissions on remaining directory and files
	- `chmod 700 ~/.sshudo` (I put vars.env and sshudo_alert.py files in this directory, you can put wherever you want but make sure that you add those changes to `/etc/systemd/system/sshudo.service` file)
	- `chmod 600 ~/.sshudo/vars.env`
	- `chmod 700 ~/.sshudo/sshudo_alert.py`

### Step 3 (Service)

1. `sudo systemctl daemon-reload`
2. `sudo systemctl start sshudo`
3. `sudo systemctl enable sshudo`

## Features to add

- IP lookup (sending detailed information about who and from where someone did SSH login)
