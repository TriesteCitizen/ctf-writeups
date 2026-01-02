<h1 align="center">Challenge 061 - Chill Hack </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/ae193853-9a40-4536-a6b3-d1d6741c7e86" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

I just wanted to have some fun with a box this time around. This challenge promises an easy challenge, which sounds just right.

## User Flag
We begin with the usual port scanning.

```
root@ip-10-64-102-12:~# nmap -sV -sV -p- 10.64.134.226
Starting Nmap 7.80 ( https://nmap.org ) at 2026-01-02 17:35 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.64.134.226
Host is up (0.0073s latency).
Not shown: 65532 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.5
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.67 seconds
```

The open ports are for ftp (port 21), ssh (port 22) and http (port 80). Pretty straightforward. Let's see what information the web page holds for us.

<img width="1123" height="766" alt="image" src="https://github.com/user-attachments/assets/e066b306-e055-492d-bd1a-bb2ba9a912e6" />

This is a pretty cool looking soccer website that contains information about upcoming matches, headline stories and information about team members. Browsing through the different pages of the website doesn't really reveal any real vulnerabilities yet. The page source also doesn't seem to hide something, so I just moved on to the brute forcing.

```
root@ip-10-64-102-12:~# gobuster dir -u 10.64.134.226 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.64.134.226
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration modeaddress bar
===============================================================
/.hta                 (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/css                  (Status: 301) [Size: 312] [--> http://10.64.134.226/css/]
/fonts                (Status: 301) [Size: 314] [--> http://10.64.134.226/fonts/]
/images               (Status: 301) [Size: 315] [--> http://10.64.134.226/images/]
/index.html           (Status: 200) [Size: 35184]
/js                   (Status: 301) [Size: 311] [--> http://10.64.134.226/js/]
/secret               (Status: 301) [Size: 315] [--> http://10.64.134.226/secret/]
/server-status        (Status: 403) [Size: 278]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

This already gives us a lot of clues. Let's check out the secret directory. By querying said url in the browser we are greeted with the following searchbar. 

<img width="261" height="37" alt="image" src="https://github.com/user-attachments/assets/73ec955b-d2ee-432b-b625-f7b4e4ea859e" />

Tempting. This makes me want to execute some Linux commands. Should I?

<img width="1123" height="763" alt="image" src="https://github.com/user-attachments/assets/ea16659e-d932-4e9a-a239-d26357fd431f" />

That's the stuff. Seems like we are on the right track. We could try finding some user.txt file now, so I used the *cat /user.txt* command.

<img width="1123" height="738" alt="image" src="https://github.com/user-attachments/assets/c77b91dc-90b4-4d1b-aee7-96e0cf732f0f" />

Well... that certainly was not the right idea. I tried using tac to make sure, we couldn't bypass this screen, which we COULD with tac, but there just doesn't seem to be a user.txt file hidden anywhere. Using ls also seems to be a  no-no, which gave me the occasion to get acquainted with some new linux commands I never used before

- find /home -maxdepth 1 -type d

With this, I was at least able to gather what kind of users existed.

<img width="946" height="83" alt="image" src="https://github.com/user-attachments/assets/08bb4174-5352-4bb2-af15-8dd7a4a76b6b" />

Next we would use a slightly abbreviated form of the same command to check for files in those user directories. It was

- find /home/apaar -maxdepth 1 -type f

Aurick didn't have anything of interest. Apaar on the other hand may be our ticket for gaining infos on the user.txt file.

<img width="945" height="137" alt="image" src="https://github.com/user-attachments/assets/a946a1ee-36e1-4250-bc10-935cde6a5daa" />

The local.txt file in particular looked very interesting.
