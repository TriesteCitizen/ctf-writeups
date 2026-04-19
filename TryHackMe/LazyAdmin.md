<h1 align="center">Challenge 062 - Hide and Seek </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/514f5fff-fa9d-40eb-976d-d89daa735c7b" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ ??? </p>

It's been a long time since I last did some proper red teaming. In this machine we will probably do the usual directory enumeration and privilege escalation, which might be good for me to get back into the grind. 
We begin with some basic nmapping

```
root@ip-10-129-93-61:~# nmap -p- -sV 10.129.144.4
Starting Nmap 7.80 ( https://nmap.org ) at 2026-04-19 17:07 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.129.144.4
Host is up (0.00093s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.97 seconds
```

As expected we have two existing ports. Let's access the http service.

Right when accessing the target IP address in the web we see the usual Apache Ubuntu Default Page.

## Directory Brute Forcing

No other hints that could help us in the Page Source, so I move on with some directory brute forcing

```
root@ip-10-128-72-209:~# gobuster dir -u 10.128.184.213 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.128.184.213
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 279]
/.htpasswd            (Status: 403) [Size: 279]
/.htaccess            (Status: 403) [Size: 279]
/content              (Status: 301) [Size: 318] [--> http://10.128.184.213/content/]
/index.html           (Status: 200) [Size: 11321]
/server-status        (Status: 403) [Size: 279]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

The content directory might be the next big clue for us. We see the following page:

<img width="1119" height="788" alt="Bildschirmfoto vom 2026-04-18 15-33-11" src="https://github.com/user-attachments/assets/aa5415fb-2604-4c5b-b581-baaff6ffd405" />

on the bottom left of the site we can read the information that the site is "Powered by Basic-CMS.ORG SweetRice." A big clue, which should be further used for exploitation.
