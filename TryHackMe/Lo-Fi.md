<h1 align="center">Challenge 033 - Lo-Fi </h1>
<div align="center">
  <img width="90" height="90" alt="5de96d9ca744773ea7ef8c00-1737110160739" src="https://github.com/user-attachments/assets/9070b314-b310-47a4-84b4-63331fd78381" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 2.10.2025  </p>

Life gets hard and I really wanted something small, so I decided to go with this challenge, which probably will scratch the surface of what LFI is about. Before that I tried tackling a challenge, which was far more challenging when it came to Local File Inclusion, so I hope that this room will be a little more forgiving with me. It also promises some Lo-Fi beats, which I'm totally down for.

To start with I just instinctively used nmap, which on hinsight wasn't really necessary, since LFI would always be a web exploit but oh well

```
root@ip-10-10-200-151:~# nmap -p- -sV 10.10.3.234
Starting Nmap 7.80 ( https://nmap.org ) at 2025-10-02 17:10 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.3.234
Host is up (0.00011s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.2.22 ((Ubuntu))
MAC Address: 02:22:AF:01:02:21 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.41 seconds
```

We access the website and see the following

<img width="1127" height="758" alt="Bildschirmfoto vom 2025-10-02 18-12-13" src="https://github.com/user-attachments/assets/e7006f07-ac27-477b-98db-830ac2a3169f" />

Cute. I'm already listening to Lo-Fi, so this is redundant, but the idea is still lovely. There is a Box labelled Discography which gives us the option to choose between different music options. Once you click on one of the options the URL promptly changes to http://10.10.3.234/?page=relax.php. Vulnerability spotted.

We try appending

<img width="661" height="267" alt="image" src="https://github.com/user-attachments/assets/5c00f2f3-6976-4baa-b740-2c6e31266178" />

This seems to work. We just have to traverse long enough to find the right path.

<img width="668" height="478" alt="image" src="https://github.com/user-attachments/assets/7fd25662-6d11-4f18-b51a-04ab23f102e5" />

And it worked with http://10.10.3.234/?page=../../../etc/passwd

Now keeping that path logic in the back of our mind we can try to find the flag.txt now.

<img width="968" height="337" alt="Bildschirmfoto vom 2025-10-02 18-28-22" src="https://github.com/user-attachments/assets/b91b1ae3-a138-4333-85e5-13bd3dba2563" />

That was easy. That takes care of that.

This was some very easy Local File Inclusion challenge. If you can even call it that. As something to get you acquainted with it, it surely is a manageable thing.
