<h1 align="center">Challenge 048 - JPGChat </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/0d244a71-f810-4843-8a67-328556ab5fa4" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

This challenge will be all about exploiting a poorly made custom chatting service written in Python. 

I thought I would see a classic http site, but apparently the service is running on a completely different port. Let's scan them to see which ones are open.

```
root@ip-10-10-53-99:~# nmap -sV -p- 10.10.18.87
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-04 11:41 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.18.87
Host is up (0.00024s latency).
Not shown: 65533 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
3000/tcp open  ppp?
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port3000-TCP:V=7.80%I=7%D=11/4%Time=6909E680%P=x86_64-pc-linux-gnu%r(NU
SF:LL,E2,"Welcome\x20to\x20JPChat\nthe\x20source\x20code\x20of\x20this\x20
SF:service\x20can\x20be\x20found\x20at\x20our\x20admin's\x20github\nMESSAG
SF:E\x20USAGE:\x20use\x20\[MESSAGE\]\x20to\x20message\x20the\x20\(currentl
SF:y\)\x20only\x20channel\nREPORT\x20USAGE:\x20use\x20\[REPORT\]\x20to\x20
SF:report\x20someone\x20to\x20the\x20admins\x20\(with\x20proof\)\n")%r(Gen
SF:ericLines,E2,"Welcome\x20to\x20JPChat\nthe\x20source\x20code\x20of\x20t
SF:his\x20service\x20can\x20be\x20found\x20at\x20our\x20admin's\x20github\
SF:nMESSAGE\x20USAGE:\x20use\x20\[MESSAGE\]\x20to\x20message\x20the\x20\(c
SF:urrently\)\x20only\x20channel\nREPORT\x20USAGE:\x20use\x20\[REPORT\]\x2
SF:0to\x20report\x20someone\x20to\x20the\x20admins\x20\(with\x20proof\)\n"
SF:);
MAC Address: 02:CC:1C:DF:9E:D5 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.22 seconds
```

We have the ssh port open and a user defined port 3000 that is running a service not even nmap seems to know anything about. To communicate with the service I tried running netcat. curl probably wouldn't work as it doesn't seem to be a regular web service.

```
root@ip-10-10-53-99:~# nc 10.10.18.87 3000
Welcome to JPChat
the source code of this service can be found at our admin's github
MESSAGE USAGE: use [MESSAGE] to message the (currently) only channel
REPORT USAGE: use [REPORT] to report someone to the admins (with proof)
```

As I connected to the chatroom service the output made clear what our next task would have to be: look for the source code of the service in github. So we just query "JPChat admin github" and immediately saw some interesting results

<img width="960" height="459" alt="Bildschirmfoto vom 2025-11-04 13-28-05" src="https://github.com/user-attachments/assets/a3274d80-59f5-4609-af06-04549bee6f09" />

Clicking on the link tells us we are on the right track.

<img width="970" height="711" alt="Bildschirmfoto vom 2025-11-04 13-32-09" src="https://github.com/user-attachments/assets/841da662-82fd-4846-97e2-adfe49ad11c8" />

We check out the source code and can gather the following from the jpchat.py 

```
#!/usr/bin/env python3

import os

print ('Welcome to JPChat')
print ('the source code of this service can be found at our admin\'s github')

def report_form():

	print ('this report will be read by Mozzie-jpg')
	your_name = input('your name:\n')
	report_text = input('your report:\n')
	os.system("bash -c 'echo %s > /opt/jpchat/logs/report.txt'" % your_name)
	os.system("bash -c 'echo %s >> /opt/jpchat/logs/report.txt'" % report_text)

def chatting_service():

	print ('MESSAGE USAGE: use [MESSAGE] to message the (currently) only channel')
	print ('REPORT USAGE: use [REPORT] to report someone to the admins (with proof)')
	message = input('')

	if message == '[REPORT]':
		report_form()
	if message == '[MESSAGE]':
		print ('There are currently 0 other users logged in')
		while True:
			message2 = input('[MESSAGE]: ')
			if message2 == '[REPORT]':
				report_form()

chatting_service()
```

This is where the service finally made sense to me. It also revealed where a possible vulnerability would be as two lines in particular are writing data to a file called *report.txt*. The first line writes the value of *your_name* to the file, and the second appends the content of *report.text*. This can be exploited if we can control the values somehow.

Maybe we can inject shell commands into these variables, you could execute arbitrary commands on the server. For example, if we manage to set *your_name* to something like $(whoami) or *; [my_command]*, it could allow us to run commands with the privileges of the user running the script. I thought that, but the application seems to sanitize the output. The next idea was to run a reverse shell..

I set up the netcat listener 

```
nc -lvnp 1337
```

and tried to run the reverse shell, but it didn't seem to work.
