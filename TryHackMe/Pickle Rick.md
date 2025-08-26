# Challenge 013 - Pickle Rick

Difficulty: Very Easy (1/10)
Completed: ✔️ 25.08.2025

This is a Rick and Morty themed challenge. One of the few shows I actually watched. This probably would have to do with priviliedge escalation once again, so I hope that my prior knowledge will kind of path the way for me somehow.

<img width="774" height="697" alt="rick1" src="https://github.com/user-attachments/assets/fffa5684-3bee-4b39-8d75-1b59a5a619db" />

Oh geez! I guess I need to logon to his computer first. When checking the Page Source you quickly receive information regarding the username:

```
  <!--

    Note to self, remember username!

    Username: R1ckRul3s

  -->
```

Having seen that I quickly moved on to my shell to make an nmap scan and tried to connect via ssh. But as already established, without a password it would be difficult to get access to the remote machine. 
Trying ffuf didn't help much as the assets didn't really have anything interesting to look at. I could try steganography but something tells me, that this isn't what's supposed to be done. The robot.txt file contained a simple message, which may be the password(?)
Maybe we need to brute force SSH to gain access? I tried to research how we would be able to do that. but quickly realized that by the result we receive when trying to check a text file we are asked to input some public key instead.

```
root@ip-10-10-127-147:~# nmap 10.10.13.97 -p 22 --script ssh-brute --script-args userdb="R1ck Rul3s",passdb="passwords.txt"
Starting Nmap 7.80 ( https://nmap.org ) at 2025-08-25 12:12 BST
Nmap scan report for ip-10-10-13-97.eu-west-1.compute.internal (10.10.13.97)
Host is up (0.00016s latency).

PORT   STATE SERVICE
22/tcp open  ssh
|_ssh-brute: Password authentication not allowed
MAC Address: 02:23:EF:58:3C:7F (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.88 seconds
```

Maybe there are some hidden messages in the jpeg files. I already had a challenge yesterday, where that was the case. I wouldn't think that we would use Steganography again, but trying it would not hurt, so I attempted to use stegcracker.
As the bruteforcing took longer then my VM could handle I discarded all these ideas as I was probably thinking way too complicated once again. We probably are not even supposed to get access through ssh, but through http. For some reason I also tried using curl in hopes of seing html, which I would somehow not be able to see with 
I also discarded that and got some help. The problem was that I bruteforced with a namelist that was way too short. Today is the day I'm learning it's important to always consider which kind of textfile I want to bruteforce with. I used several with no avail, until I realized that I could have done with a login text file, as it was already very clear that we would be looking for something like that.

```
root@ip-10-10-254-210:~# gobuster dir -u http://10.10.1.19 -w /root/SecLists/Discovery/Web-Content/Logins.fuzz.txt 
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.1.19
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /root/SecLists/Discovery/Web-Content/Logins.fuzz.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/login.php            (Status: 200) [Size: 882]
/?page=admin.auth.inc (Status: 200) [Size: 1062]
/?page=auth.inc.php   (Status: 200) [Size: 1062]
/?page=auth.inc       (Status: 200) [Size: 1062]
Progress: 89 / 90 (98.89%)
===============================================================
Finished
===============================================================
```

Finally one problem was solved and I accessed the login.php. 

<img width="945" height="673" alt="rick2" src="https://github.com/user-attachments/assets/20b8416a-ec73-414a-969e-2dedba631bb6" />
 
The username is R1ckRul3s (as hinted from the Page Source) and the password COULD be Wubbalubbadubdub as hinted from the robots.txt. Let's try that out.

<img width="937" height="382" alt="rick3" src="https://github.com/user-attachments/assets/df0b7645-d466-49c7-b169-e8ec6b6465f3" />
 
And we were able to access the page. I almost started overthinking again and trying to use a reverse PHP shell, just because I saw an input prompt, but instead started executing commands through the panel. When using ls we got the following files as a result:

```
Sup3rS3cretPickl3Ingred.txt
assets
clue.txt
denied.php
index.html
login.php
portal.php
robots.txt
```

The first ingredient was very close. Now we only needed to use cat I thought, but instead we were greeted by a notification that the command was disabled.

 <img width="906" height="470" alt="rick4" src="https://github.com/user-attachments/assets/faa733fd-4424-4d48-a590-bb814c98cd77" />

Once again, my expectations were completely destroyed. I looked for a workaround and first tried using head, tail and cp. The last one was especially redundant, but through all this I found out about a command I never heard of before: tac. Apparently all the lines from a file would now be displayed in reverse. How fun. It also was able to bypass the command restriction and I was finally able to find out the first ingredient.

Now using tac I also checked out the clue.txt file, which hinted to look around the file system for the other ingredients. I did not even know which directory I was located in right now, so I used pwd, which gave me the output:

```
/var/www/html
```

Using this command confused me way more than it helped at the beginning. I still needed to understand that I was not in an actual SSH session and was executing commands in a web shell running as the web service account. Due to misconfigured permissions or sudo rights I was also able to read Ricks files though. The filesystem probably looked like this:

```
/
├── bin/        → system binaries (ls, cat, bash…)
├── etc/        → system configs (passwd, shadow, hosts, sudoers…)
├── home/
│   ├── rick/   → Rick’s personal files (2nd ingredient was here)
│   └── ubuntu/ → another user’s home
├── root/       → superuser’s home (3rd ingredient was here)
├── tmp/        → temporary files, often world-writable
└── var/
    └── www/
        └── html/ → web root (web app files, index.html, login.php, etc.)
```

As every directory has a /home I tried to check it out real quick with ls /home and got:

```
rick
ubuntu
```

Going further and using /home/rick revealed another directory that looked interesting:

```
second ingredients
```

With that clue I tried using the tac command again 

```
tac '/home/rick/second ingredients'
```

and simple as that I got the second ingredient.

For the last ingredient I assumed that we would need to do some sort of privilege escalation. I thought of maybe checking out the sudoers file /etc/, which exists, but is not accessible due to the command constraints of this challenge. I also needed to find out the path this sudoers file was located at and started usind realpath sudoers. The output was

```
/var/www/html/sudoers
```

Honestly even after having beat this challenge this output doesn't make a lot of sense to me. This file should be located in /etc/, but maybe our web panel is restricted in some ways I'm not aware of.

After some time I gave up on trying to modify that file, because I just don't have the file permissions for that. I forgot that in the last challenge we were only able to do that because of some specific edge case. 
I checked through all the file directories and thought I really would overlook some important directory in /etc/ that holds valuable information until I just tried the most simple command sudo ls /root:

```
3rd.txt
snap
```

I felt kind of offended that that worked as it felt a little bit too easy. Yet again this is a beginner CTF and is a good room to learn the basics, so I just accepted the third ingredient openly with the command
sudo tac '/root/3rd.txt'

The third ingredient was ours and marked the end of the challenge.
