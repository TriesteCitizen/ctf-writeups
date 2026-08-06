<h1 align="center">Grep </h1>

<p align="center">
  <img src="assets/grep.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

This is a challenge I have to do for my certification. I don't know what this OSINT challenge has to do with blue teaming but whatever. In this task, we will be an ethical hacker aiming to exploit a newly developed web application.

SuperSecure Corp, a fast-paced startup, is currently creating a blogging platform inviting security professionals to assess its security. The challenge involves using OSINT techniques to gather information from publicly accessible sources and exploit potential vulnerabilities in the web application.

Our goal is to identify and exploit vulnerabilities in the application using a combination of recon and skills. As we progress, we’ll look for weak points in the app, find sensitive data, and attempt to gain unauthorized access. We will leverage the skills and knowledge acquired through the Red Team Pathway to devise and execute our attack strategies.

For Reconnaissance we do a classic nmap scan

```
root@ip-10-112-65-134:~# nmap -sV -sC -p- 10.112.144.72
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-08-06 13:31 UTC
Nmap scan report for ip-10-112-144-72.eu-central-1.compute.internal (10.112.144.72)
Host is up (0.00057s latency).
Not shown: 65531 closed tcp ports (reset)
PORT      STATE SERVICE  VERSION
22/tcp    open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 6a:cd:96:d4:ad:12:be:8e:13:41:94:46:2c:74:c1:44 (RSA)
|   256 b1:26:2b:68:8d:d6:83:3b:ad:22:6c:1e:be:3a:d9:81 (ECDSA)
|_  256 9f:72:c3:97:7c:65:ed:22:db:e1:fe:24:6c:5d:e9:6e (ED25519)
80/tcp    open  http     Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.41 (Ubuntu)
443/tcp   open  ssl/http Apache httpd 2.4.41
|_http-title: 403 Forbidden
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
| ssl-cert: Subject: commonName=grep.thm/organizationName=SearchME/stateOrProvinceName=Some-State/countryName=US
| Not valid before: 2023-06-14T13:03:09
|_Not valid after:  2024-06-13T13:03:09
51337/tcp open  http     Apache httpd 2.4.41
|_http-title: 400 Bad Request
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.67 seconds
```

## What is the API key that allows a user to register
An API key is a unique identifier used to authenticate requests associated with a project or application. It acts as a secret token that allows us to securely interact with an API, enabling actions such as user registration or data retrieval.
Accessing the webpage we see a Ubuntu Default Page. None of what you see is really interesting so I moved in with directory brute forcing.

```
root@ip-10-112-65-134:~# gobuster dir -u http://10.112.144.72/ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.112.144.72/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/javascript           (Status: 301) [Size: 319] [--> http://10.112.144.72/javascript/]
/phpmyadmin           (Status: 403) [Size: 278]
/server-status        (Status: 403) [Size: 278]
Progress: 220560 / 220561 (100.00%)
===============================================================
Finished
===============================================================
```

Since directory brute forcing hasn't yielded results, I opted on actually looking for some kind of repository. The exercise even talked about the SuperSecure Corp. Let's query for it. That lead to results in form of a GitHub repository.

<img width="869" height="816" alt="image" src="https://github.com/user-attachments/assets/8fb38303-9c4a-4c3a-aed5-27e7f918a88b" />

First let's clone this.

```
root@ip-10-112-65-134:~# git clone https://github.com/HighlySecureOrganization/SuperSecureWebApp.git
Cloning into 'SuperSecureWebApp'...
remote: Enumerating objects: 74, done.
remote: Counting objects: 100% (74/74), done.
remote: Compressing objects: 100% (52/52), done.
remote: Total 74 (delta 25), reused 61 (delta 12), pack-reused 0 (from 0)
Receiving objects: 100% (74/74), 14.09 KiB | 2.01 MiB/s, done.
Resolving deltas: 100% (25/25), done.
```

We can try extracting the API key from the source code. For that we use the following command to search for API key references in the dumped repository:

<img width="816" height="48" alt="Bildschirmfoto vom 2026-08-06 15-16-55" src="https://github.com/user-attachments/assets/b3a5de82-5481-4d49-8c53-c6b384d3bc99" />

I thought that would be the solution. But it wasn't.
