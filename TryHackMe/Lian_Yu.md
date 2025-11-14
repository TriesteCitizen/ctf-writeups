<h1 align="center">Challenge 051 - Lian_Yu </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/ef39fa90-0710-4e7b-b19d-4f13385b2a4d" width="250" height="250" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 3/10 (Fairly Easy) <b>Completed</b>: ✔️ 14.11.2025 </p>

## Reconnaissance
This is a beginner level security challenge, which probably expects us to do some basic enumeration and exploitation. We go ahead and deploy the machine, starting with port scanning through nmap.

```
root@ip-10-10-233-75:~# nmap -sV -p- -A 10.10.132.37
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-13 12:38 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.132.37
Host is up (0.00043s latency).
Not shown: 65530 closed ports
PORT      STATE SERVICE VERSION
21/tcp    open  ftp     vsftpd 3.0.2
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)
| ssh-hostkey: 
|   1024 56:50:bd:11:ef:d4:ac:56:32:c3:ee:73:3e:de:87:f4 (DSA)
|   2048 39:6f:3a:9c:b6:2d:ad:0c:d8:6d:be:77:13:07:25:d6 (RSA)
|   256 a6:69:96:d7:6d:61:27:96:7e:bb:9f:83:60:1b:52:12 (ECDSA)
|_  256 3f:43:76:75:a8:5a:a6:cd:33:b0:66:42:04:91:fe:a0 (ED25519)
80/tcp    open  http    Apache httpd
|_http-server-header: Apache
|_http-title: Purgatory
111/tcp   open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          39797/udp6  status
|   100024  1          45977/tcp   status
|   100024  1          50401/tcp6  status
|_  100024  1          60138/udp   status
45977/tcp open  status  1 (RPC #100024)
MAC Address: 02:96:00:AF:7C:39 (Unknown)
Device type: general purpose
Running: Linux 3.X
OS CPE: cpe:/o:linux:linux_kernel:3
OS details: Linux 3.10 - 3.13
Network Distance: 1 hop
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.43 ms 10.10.132.37

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.98 seconds
```

Seems like we have an existing web page. There are a lot of other services that seem to be open too. When checking out the website we see the following page.

<img width="1154" height="762" alt="grafik" src="https://github.com/user-attachments/assets/9a499dbf-a762-454e-a6ad-eb89fca16b97" />

## Vulnerability Analysis

This is also the moment, where I realize that this challenge is based on the Arrow TV-Show. Unfortunately there was not much else to gather from the site, so I just continued with directory enumeration through gobuster. I had to try out multiple wordlists to get a satisfying result.

```
root@ip-10-10-233-75:~# gobuster dir -u 10.10.132.37 -w /usr/share/wordlists/dirb/big.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.132.37
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 199]
/.htpasswd            (Status: 403) [Size: 199]
/island               (Status: 301) [Size: 235] [--> http://10.10.132.37/island/]
/server-status        (Status: 403) [Size: 199]
Progress: 20469 / 20470 (100.00%)
===============================================================
Finished
===============================================================
```

Let's check out the site.

<img width="588" height="195" alt="Bildschirmfoto vom 2025-11-13 14-02-01" src="https://github.com/user-attachments/assets/2cd7f243-2ba8-4fbc-96f4-bef6d25db171" />

That's one code word we can note down for ourselves. Clearly we can also keep enumerating from this directory to see, if the /island directory holds some other secrets. I had to try out a lot of different wordlists for this one. Note to myself: for easy enumerating refer to the lists in the Web-Content directory.

```
root@ip-10-10-233-75:~# gobuster dir -u 10.10.132.37/island -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.132.37/island
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/2100                 (Status: 301) [Size: 240] [--> http://10.10.132.37/island/2100/]
Progress: 220560 / 220561 (100.00%)
===============================================================
Finished
===============================================================
```

This answers the question of what numeric Web Directory we found. Let's check it out now.

<img width="903" height="604" alt="grafik" src="https://github.com/user-attachments/assets/263d0bfe-bf46-4c50-a2e7-e8a45b49ee1f" />

What in the...? Is this challenge that old, or am I missing something? I checked out the Page Source too

```
<!DOCTYPE html>
<html>
<body>

<h1 align=center>How Oliver Queen finds his way to Lian_Yu?</h1>


<p align=center >
<iframe width="640" height="480" src="https://www.youtube.com/embed/X8ZiFuW41yY">
</iframe> <p>
<!-- you can avail your .ticket here but how?   -->

</header>
</body>
</html>
```

This at least gave me some new hint. We need to navigate through further directories by using the -x flag on gobuster to specify the extension to append to each word in the wordlist during the directory enumeration process. It allows us to search for specific file types while scanning for hidden directories and files on a web server. Now in this instance we append *.ticket*

```
root@ip-10-10-43-71:~# gobuster dir -u 10.10.183.241/island/2100 -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -x .ticket
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.183.241/island/2100
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              ticket
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/green_arrow.ticket   (Status: 200) [Size: 71]
Progress: 441120 / 441122 (100.00%)
==================================To base=============================
Finished
===============================================================
```

Seems like I had the right hunch. Let's check out that directory now.

<img width="398" height="101" alt="grafik" src="https://github.com/user-attachments/assets/cbde29eb-9075-47cd-95e4-e05aa5542251" />

We could very well be close to receiving the FTP password

<img width="668" height="551" alt="Bildschirmfoto vom 2025-11-14 12-13-00" src="https://github.com/user-attachments/assets/0ac4495e-5581-4aa3-81a9-ebabe23f3c26" />

I went through all the different base decodings to see what output could be logical in Cyberchef. Base58 seemed to be the right option. With that we can finally login to port 21 to see what we can retrieve.

```
root@ip-10-10-43-71:~# ftp 10.10.183.241
Connected to 10.10.183.241.
220 (vsFTPd 3.0.2)
Name (10.10.183.241:root): vigilante
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0          511720 May 01  2020 Leave_me_alone.png
-rw-r--r--    1 0        0          549924 May 05  2020 Queen's_Gambit.png
-rw-r--r--    1 0        0          191026 May 01  2020 aa.jpg
226 Directory send OK. 
```

We can try to retrieve those files now.

```
ftp> type binary
200 Switching to Binary mode.
ftp> get Leave_me_alone.png
local: Leave_me_alone.png remote: Leave_me_alone.png
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for Leave_me_alone.png (511720 bytes).
226 Transfer complete.
511720 bytes received in 0.01 secs (80.3316 MB/s)
ftp> get Queen's_Gambit.png
local: Queen's_Gambit.png remote: Queen's_Gambit.png
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for Queen's_Gambit.png (549924 bytes).
226 Transfer complete.
549924 bytes received in 0.00 secs (136.3620 MB/s)
ftp> get aa.jpg
local: aa.jpg remote: aa.jpg
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for aa.jpg (191026 bytes).
226 Transfer complete.
191026 bytes received in 0.00 secs (89.6980 MB/s)
ftp> quit
221 Goodbye.
```

After fetching the png's we can see the two following prictures

<p align="center">
  <img width="400" height="600"
       src="https://github.com/user-attachments/assets/433da41a-a83e-462a-94a3-e9852d51e317" />
</p>

<p align="center">
  <img width="400" height="400"
       src="https://github.com/user-attachments/assets/46f8b6de-0c7e-4eed-804d-185418cc0c96" />
</p>

There also was a third picture, which I was unable to load as it lead to a fatal error. Maybe something is wrong with the file header. PNG files always start with a specific signature: the first eight bytes should be *89 50 4E 47 0D 0A 1A 0A*. If these are altered we may not be able to load it anymore. I used the xxd command in the terminal to create a hexdump.

```
root@ip-10-10-7-251:~# xxd -p Leave_me_alone.png > new.png
root@ip-10-10-7-251:~# vim new.png
```

I altered these in the hopes we could render the image and indeed after using Cyberchef we received a password

<img width="877" height="731" alt="Bildschirmfoto vom 2025-11-14 16-53-41" src="https://github.com/user-attachments/assets/e904f8cb-e05b-47c1-8aec-1cef5bd03694" />

Maybe we can use that password to extract some secret message from one of the two pictures.

```
root@ip-10-10-7-251:~# steghide --extract -sf aa.jpg
Enter passphrase: 
wrote extracted data to "ss.zip".
```

Checking out the zip we got two passwords.

<img width="916" height="206" alt="grafik" src="https://github.com/user-attachments/assets/b499915a-4a87-4f4b-b455-784398de7561" />

Now we succesfully recovered the password for ssh. Not really sure what the username is supposed to be though. I tried vigilante but that didn't seem to work. After a long thinking process I tried to login to the ftp service again to see if there were some other users, which credentials I could make use of.

```
root@ip-10-10-7-251:~# ftp 10.10.208.244
Connected to 10.10.208.244.
220 (vsFTPd 3.0.2)
Name (10.10.208.244:root): vigilante
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> cd ..
250 Directory successfully changed.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwx------    2 1000     1000         4096 May 01  2020 slade
drwxr-xr-x    2 1001     1001         4096 May 05  2020 vigilante
226 Directory send OK.
```

Maybe it's good practice to always traverse through all directories if I already have the chance to explore a service. I will keep that in mind for the next time, as this really stole a lot of my time. Anyway I tried logging in now with the slade username.

## Exploitation

<img width="729" height="517" alt="Bildschirmfoto vom 2025-11-14 17-26-09" src="https://github.com/user-attachments/assets/cbafb1f7-a18b-4698-a918-d9f7f27cc824" />

We got the first flag. For the second one I checked out the commands I could run as sudo.

```
slade@LianYu:~$ sudo -l
[sudo] password for slade: 
Matching Defaults entries for slade on LianYu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User slade may run the following commands on LianYu:
    (root) PASSWD: /usr/bin/pkexec
```

Gtfobins is our friend in these situations.

<img width="848" height="302" alt="grafik" src="https://github.com/user-attachments/assets/b18170d3-528f-4326-862e-9bf102024a8d" />

Got 'em!

<img width="724" height="383" alt="Bildschirmfoto vom 2025-11-14 17-32-49" src="https://github.com/user-attachments/assets/abfb1537-8725-49ff-ae9a-9ae4d842798a" />

And that takes care of the privilege escalation. We got the root.txt!

## Lesson Learned
I realized that we needed to do a lot of directory enumeration and not every wordlist would be valuable for that. We always need to consider the context we are in. Enumerating further in the context of an *island* should have sounded logical, but I did not really get that. I also didn't know that we could use gobuster to append strings into the wordlist. Last but not least always make use of exploring the necessary services that are available to you. Just because you successfully exfiltrated the files you were searching for doesn't mean you shouldn't be curious to explore more. All in all this is still a good challenge. Maybe watch the Arrow show and some clues might be more clear to you. I don't know. 
