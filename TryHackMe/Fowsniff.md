# Challenge 018 - Fowsniff CTF 

<img width="92" height="93" alt="Bildschirmfoto vom 2025-09-05 16-43-24" src="https://github.com/user-attachments/assets/3fd01736-3a20-4890-81f3-7a9920460620" />

Difficulty: Easy (2/10) Completed: ✔️ 05.09.2025

This one was considered an easy challenge, with many hints along the way, so I decided to go for it. In this boot2root machine we will enumerate to find open ports, decode hashes, brute force hashes and much more. I'm already very curious on what will await me. At the beginnign we just need to deploy the machine. Easy.
After having done that, we have to use nmao to check for open ports again. As i felt lazy I just used the -p- flag.

<img width="735" height="320" alt="image" src="https://github.com/user-attachments/assets/be42ff7c-135b-49a0-b830-a695096ba276" />

As we can see there are exactly 4 ports open. The one for http (80), used for unencrypted web traffic, the ssh (22), which is the port used by the secure shell protocol to faciliate secure connections, the one for pop3 (110), which is used for unencrypted connection and the imap port (143), which is the default IMAP port for unencrypted (plain text) connections.

<img width="973" height="873" alt="image" src="https://github.com/user-attachments/assets/ec4919ca-2d42-435f-86ad-af456d14c196" />

When we check out the http website, we get the notification that it would temporarily be out of service as there was a data breach. A hacker apparently hijacked the website and got a hold of all usernames and passwords, which could very well be leaked somewhere. Maybe GitHub or some other website. I just did a directory check to see if there maybe was another directory, where the data was leaked.

```
root@ip-10-10-43-10:~# gobuster dir -u http://10.10.22.125 -w big.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.22.125
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/images               (Status: 301) [Size: 313] [--> http://10.10.22.125/images/]
/assets               (Status: 301) [Size: 313] [--> http://10.10.22.125/assets/]
/server-status        (Status: 403) [Size: 300]
Progress: 1273834 / 1273835 (100.00%)
===============================================================
Finished
===============================================================
```

Unfortunately this didn't really reveal anything new or worthwhile. I also researched what the Dovecot service was all about. Apparently it's a highly secure and performant IMAP and POP3 mail server for Linux/UNIX-like systems, handling email retrieval from mail servers to email clients. So nothing we can use to our advantage.

I tried to use the WaybackMachine to maybe find some lost resources but that didn't really help either, which is weird. Maybe I wrote the wrong URL. For now I just checked GitHub and at least found an interesting repo with a text file there.

```
FOWSNIFF CORP PASSWORD LEAK
            ''~``
           ( o o )
+-----.oooO--(_)--Oooo.------+
|                            |
|          FOWSNIFF          |
|            got             |
|           PWN3D!!!         |
|                            |         
|       .oooO                |         
|        (   )   Oooo.       |         
+---------\ (----(   )-------+
           \_)    ) /
                 (_/
FowSniff Corp got pwn3d by B1gN1nj4!
No one is safe from my 1337 skillz!
 
 
mauer@fowsniff:8a28a94a588a95b80163709ab4313aa4
mustikka@fowsniff:ae1644dac5b77c0cf51e0d26ad6d7e56
tegel@fowsniff:1dc352435fecca338acfd4be10984009
baksteen@fowsniff:19f5af754c31f1e2651edde9250d69bb
seina@fowsniff:90dc16d47114aa13671c697fd506cf26
stone@fowsniff:a92b8a29ef1183192e3d35187e0cfabd
mursten@fowsniff:0e9588cb62f4b6f27e33d449e2ba0b3b
parede@fowsniff:4d6e42f56e127803285a0a7649b5ab11
sciana@fowsniff:f7fd98d380735e859f8b2ffbbede5a7e
 
Fowsniff Corporation Passwords LEAKED!
FOWSNIFF CORP PASSWORD DUMP!
 
Here are their email passwords dumped from their databases.
They left their pop3 server WIDE OPEN, too!
 
MD5 is insecure, so you shouldn't have trouble cracking them but I was too lazy haha =P
 
l8r n00bz!
 
B1gN1nj4

-------------------------------------------------------------------------------------------------
This list is entirely fictional and is part of a Capture the Flag educational challenge.

--- THIS IS NOT A REAL PASSWORD LEAK ---
 
All information contained within is invented solely for this purpose and does not correspond
to any real persons or organizations.
 
Any similarities to actual people or entities is purely coincidental and occurred accidentally.

-------------------------------------------------------------------------------------------------
```

This probably is the pastebin the challenge was hinting at. It contains leaked passwords from the Fowsniff Corporation. The values were MD5 encrypted, which - like the author of this text file hinted - isn't really difficult to crack. Using the site md5hashing I inserted the hash of mauer to got the md5 value:

<img width="934" height="255" alt="Bildschirmfoto vom 2025-09-05 11-49-19" src="https://github.com/user-attachments/assets/c9bbc359-3a62-42ba-929f-9f98f5a48116" />

Now it was time to use Metasploit to brute force the pop3 login. For that I looked up possible packages security weaknesses that could be abused.

```
msf6 > grep scanner search pop3
   2   auxiliary/scanner/pop3/pop3_version                    .                normal   No     POP3 Banner Grabber
   3   auxiliary/scanner/pop3/pop3_login                      .                normal   No     POP3 Login Utility
```

I was able to find a package pretty quickly called auxiliary/scanner/pop3/pop3_login where all usernames and passwords can be used to brute force the machines pop3 service. 

I was also asked about the seina's password for the email service. Using the md5hashing website again I found out pretty quickly, that her password was scoobydoo2. Funny.
With that we would also be able to solve the next task, which asks us to use seinas credentials to login to the pop3 service

<img width="551" height="351" alt="Bildschirmfoto vom 2025-09-05 12-23-22" src="https://github.com/user-attachments/assets/767cbb89-b124-4241-b4bc-237a3ffc5a9a" />

So far so good. The telnet command is the only command we can use to connect to the pop3 remote server using the Telnet protocol. With a given cheat sheet for POP3 commands (https://routezero.security/2025/04/20/pop3-cheat-sheet-for-penetration-testers/) I was able to get an overview of the current mails seina got.

<img width="737" height="187" alt="image" src="https://github.com/user-attachments/assets/a4f15842-88c3-4ed0-b027-998ef7a33cfa" />

I took advantage of these commands in particular. 

```
RETR 1
+OK 1622 octets
Return-Path: <stone@fowsniff>
X-Original-To: seina@fowsniff
Delivered-To: seina@fowsniff
Received: by fowsniff (Postfix, from userid 1000)
	id 0FA3916A; Tue, 13 Mar 2018 14:51:07 -0400 (EDT)
To: baksteen@fowsniff, mauer@fowsniff, mursten@fowsniff,
    mustikka@fowsniff, parede@fowsniff, sciana@fowsniff, seina@fowsniff,
    tegel@fowsniff
Subject: URGENT! Security EVENT!
Message-Id: <20180313185107.0FA3916A@fowsniff>
Date: Tue, 13 Mar 2018 14:51:07 -0400 (EDT)
From: stone@fowsniff (stone)

Dear All,

A few days ago, a malicious actor was able to gain entry to
our internal email systems. The attacker was able to exploit
incorrectly filtered escape characters within our SQL database
to access our login credentials. Both the SQL and authentication
system used legacy methods that had not been updated in some time.

We have been instructed to perform a complete internal system
overhaul. While the main systems are "in the shop," we have
moved to this isolated, temporary server that has minimal
functionality.

This server is capable of sending and receiving emails, but only
locally. That means you can only send emails to other users, not
to the world wide web. You can, however, access this system via 
the SSH protocol.

The temporary password for SSH is "S1ck3nBluff+secureshell"

You MUST change this password as soon as possible, and you will do so under my
guidance. I saw the leak the attacker posted online, and I must say that your
passwords were not very secure.

Come see me in my office at your earliest convenience and we'll set it up.

Thanks,
A.J Stone



.
```
Haha, what a mess. This is funny. Anyways. We got the temporaty SSH password through that, which gives us another attack vector. Before that I used RETR 2 to also look at the other mail

```
RETR 2
+OK 1280 octets
Return-Path: <baksteen@fowsniff>
X-Original-To: seina@fowsniff
Delivered-To: seina@fowsniff
Received: by fowsniff (Postfix, from userid 1004)
	id 101CA1AC2; Tue, 13 Mar 2018 14:54:05 -0400 (EDT)
To: seina@fowsniff
Subject: You missed out!
Message-Id: <20180313185405.101CA1AC2@fowsniff>
Date: Tue, 13 Mar 2018 14:54:05 -0400 (EDT)
From: baksteen@fowsniff

Devin,

You should have seen the brass lay into AJ today!
We are going to be talking about this one for a looooong time hahaha.
Who knew the regional manager had been in the navy? She was swearing like a sailor!

I don't know what kind of pneumonia or something you brought back with
you from your camping trip, but I think I'm coming down with it myself.
How long have you been gone - a week?
Next time you're going to get sick and miss the managerial blowout of the century,
at least keep it to yourself!

I'm going to head home early and eat some chicken soup. 
I think I just got an email from Stone, too, but it's probably just some
"Let me explain the tone of my meeting with management" face-saving mail.
I'll read it when I get back.

Feel better,

Skyler

PS: Make sure you change your email password. 
AJ had been telling us to do that right before Captain Profanity showed up.

.
```

Valid crashout honestly. There was not much info to retrieve so I exited the service and moved on to the Secure Shell, using the credentials I found out just now. It didn't work at first, because I did not clearly read the task. They were asking me to use the credentials of the SENDER, which in this case would be stone or baksteen. My bad. For that I needed to make sure to crack their md5 passwords as well to then check their pop3 mailbox. It was very evident after a while, that stones password at least could not be cracked. Impressive. The same can't be said about baksteens who just used his first name as a password (skyler22). I was not able to enter through his pop3 login credentials though, seems like that was already changed. Probably because Devin was still on vacation. I WAS able to get access through his secure shell though. 

```
root@ip-10-10-52-216:~# ssh baksteen@10.10.203.64
baksteen@10.10.203.64's password: 

                            _____                       _  __  __  
      :sdddddddddddddddy+  |  ___|____      _____ _ __ (_)/ _|/ _|  
   :yNMMMMMMMMMMMMMNmhsso  | |_ / _ \ \ /\ / / __| '_ \| | |_| |_   
.sdmmmmmNmmmmmmmNdyssssso  |  _| (_) \ V  V /\__ \ | | | |  _|  _|  
-:      y.      dssssssso  |_|  \___/ \_/\_/ |___/_| |_|_|_| |_|   
-:      y.      dssssssso                ____                      
-:      y.      dssssssso               / ___|___  _ __ _ __        
-:      y.      dssssssso              | |   / _ \| '__| '_ \     
-:      o.      dssssssso              | |__| (_) | |  | |_) |  _  
-:      o.      yssssssso               \____\___/|_|  | .__/  (_) 
-:    .+mdddddddmyyyyyhy:                              |_|        
-: -odMMMMMMMMMMmhhdy/.    
.ohdddddddddddddho:                  Delivering Solutions


   ****  Welcome to the Fowsniff Corporate Server! **** 

              ---------- NOTICE: ----------

 * Due to the recent security breach, we are running on a very minimal system.
 * Contact AJ Stone -IMMEDIATELY- about changing your email and SSH passwords.


Last login: Tue Mar 13 16:55:40 2018 from 192.168.7.36
```

We are in. Now we needed to figure out, which group the user belonged to, which can be done with id.

```
baksteen@fowsniff:/home$ id
uid=1004(baksteen) gid=100(users) groups=100(users),1001(baksteen)
```

By using the command we can see that backsteen is just a regular user with no root privileges. We are also asked to find out if there are any interesting files that can be run by that group. For that we use

```
find / -group users -type f 2>/dev/null
```

With -type f we are able to specify that the command only looks for regular files. One of the first results is 

```
/opt/cube/cube.sh
...
```
which outputs the box that we saw above. Amazing! With this we are able to run a reverse shell. Luckily the challenge itself already supplies a reverse shell we can insert. After using nano I do exactly that

<img width="777" height="381" alt="image" src="https://github.com/user-attachments/assets/b61f7140-8403-49f5-ad43-fac34336546b" />

Succesfully appended! When running the shell it notifies us that there is no route to host, which would be our listener. We will get back to that in a second. This file is run as root now though. When a user connects to the machine using SSH. The update-mot-d directory, where all the script and template files reside will execute a dynamic "Message of the Day" (MOTD) upon user login, the 00-header file 

```
baksteen@fowsniff:/etc/update-motd.d$ cat 00-header
#!/bin/sh
#
#    00-header - create the header of the MOTD
#    Copyright (C) 2009-2010 Canonical Ltd.
#
#    Authors: Dustin Kirkland <kirkland@canonical.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

#[ -r /etc/lsb-release ] && . /etc/lsb-release

#if [ -z "$DISTRIB_DESCRIPTION" ] && [ -x /usr/bin/lsb_release ]; then
#	# Fall back to using the very slow lsb_release utility
#	DISTRIB_DESCRIPTION=$(lsb_release -s -d)
#fi

#printf "Welcome to %s (%s %s %s)\n" "$DISTRIB_DESCRIPTION" "$(uname -o)" "$(uname -r)" "$(uname -m)"

sh /opt/cube/cube.sh
```

As we can see the shell gets executed at the very end. Everything should work accordingly. This is the moment where we can run the netcat listener and ssh login with the credentials... or so I thought. This was the moment where I realized I made a BIG mistake, which was inserting the IP Address of the target machine instead of my own. Yeah... we don't talk about it. I tried restarting the machine and retracing my steps while inserting the right IP Address this time! After doing that I thankfully made it

<img width="484" height="96" alt="image" src="https://github.com/user-attachments/assets/7996b997-1ec1-41a2-9d88-cf4866788a59" />

We moved to the root directory and cat'ed the flag.txt

<img width="688" height="520" alt="image" src="https://github.com/user-attachments/assets/13573079-135f-4cc3-9369-5acafd921ceb" />

Great. This was a fun little CTF, but I had a lot issues regarding the VM that kept on disconnecting at the very end, when I just wanted to take a final screenshot, which was very frustrating. Maybe I should start deploying my own machine. It would probably make a lot of stuff easier. Next time I will also try to figure out Metaspoit, as this was my very first use of that tool, and I'm not sure if I was really able to use all of it's functionalities well enough. 
