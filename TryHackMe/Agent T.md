<h1 align="center">Challenge 036 - Agent T </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/19cef16c-98f0-46b4-926c-1419ec98c7b4" alt="AgentT" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 07.10.2025  </p>

This is a small challenge, which apparently can be solved in about 10 minutes. Perfect for a little warm-up. 

Agent T uncovered this website, which looks innocent enough, but apparently something seems off about how the server responds. Let's find out what it is. But before we visit the site I do a quick nmap scan

```
root@ip-10-10-94-93:~# nmap -p- -sV 10.10.78.125
Starting Nmap 7.80 ( https://nmap.org ) at 2025-10-07 14:16 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.78.125
Host is up (0.00022s latency).
Not shown: 65534 closed ports
PORT   STATE SERVICE VERSION
80/tcp open  http    PHP cli server 5.5 or later (PHP 8.1.0-dev)
MAC Address: 02:9A:01:92:E4:FB (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.73 seconds
```

Seems like this is one of the cases where we really just have to focus on what's going on on the website. But the hint that this website is using a specific PHP version could be a vulnerability, which we can keep in mind for later.

When the site is accessed we see this Dashboard

<img width="1151" height="852" alt="image" src="https://github.com/user-attachments/assets/9df9bd5f-05eb-4ea7-bfa6-58a9baf52e04" />

Except that we are already logged in as the admin - which is quite concerning by itself - we can also Generate a Report by clicking on a button. Might be a way to exploit via SSRF. Looking at the sidebar we aren't able to really click on any of these options. There also are some open notifications and messages, which we unfortunately aren't to check out. Not even the Admin profile is viewable.

The Page Source also doesn't really reveal anythign worthwhile, so we move on to the Network Inspector and refresh the page to see if we are able to deduce something through that.

<img width="977" height="250" alt="image" src="https://github.com/user-attachments/assets/56126892-3899-4456-9b89-b8c0f9988c1c" />

Seems like some sort of image is requested through GET when we access the site, but is blocked. As the domain name and IP address are given we might as well check it out.

<img width="472" height="255" alt="image" src="https://github.com/user-attachments/assets/8fa433b9-ec8d-4065-ae7c-5bac0dc1ba4a" />

That didn't really help anything. As I didn't really know what to do I just googled for some exploit for the *PHP 8.1.0-dev* version and found a website which was really helpful for this situation. (https://www.exploit-db.com/exploits/49933)

It showcases how we are able to access a backdoor in this version and how an attacker can execute arbitrary code by sending the User-Agent header.

After downloading the exploit file we were ready to execute it through our bash terminal 

```
root@ip-10-10-94-93:~# ls
49933.py    Desktop       Pictures  Scripts            Tools
burp.json   Downloads     Postman   snap
CTFBuilder  Instructions  Rooms     thinclient_drives
root@ip-10-10-94-93:~# python3 49933.py
Enter the full host url:
http://10.10.78.125/

Interactive shell is opened on http://10.10.78.125/ 
Can't acces tty; job crontol turned off.
$ whoami
root
```

And just like that we compromised the server and had root privileges. Now we only had to find the text file and cat it

<img width="353" height="102" alt="Bildschirmfoto vom 2025-10-07 16-32-58" src="https://github.com/user-attachments/assets/7c39f21c-1c56-46a2-8285-6ae185b837bc" />

It's funny. When starting this challenge I really thought using nmap would be an unnecessary step as the task itself was already given away that we would mostly analyze a web page, but this CTF really showed me that the version of an application can give additional clues as to how we can exploit a specific site and to always keep an overview of what attack vectors we can have. This was fun and even if it costed me more time then the expected 10 minutes, it was still a valuable experience.
