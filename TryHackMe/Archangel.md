<h1 align="center">Challenge 032 - Archangel </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/e4bcb6fe-3553-412a-a8ab-9a7133c22f41" alt="Archangel" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️  </p>

This CTF focuses on the usual boot2root, Web exploitation, but also Local File Inclusion, which I never did any practical examples for. I'm excited what I will learn from this and deployed the machine.

For now I just scanned the ports to make sure I knew what kind of services I'm dealing with

```
root@ip-10-10-229-242:~# nmap -p- -sV 10.10.211.113
Starting Nmap 7.80 ( https://nmap.org ) at 2025-10-02 13:48 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.211.113
Host is up (0.000094s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
MAC Address: 02:BF:D7:B1:83:CB (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.90 seconds
```

It's the usual ports. When accessing the website, we see the following  

<img width="1158" height="766" alt="Bildschirmfoto vom 2025-10-02 14-50-12" src="https://github.com/user-attachments/assets/2bc8cd82-2f7c-47c0-adca-24e9495dccda" />

By further scrolling down the website we see a lot of blind text that doesn't really mean anything. We are able to answer the first question by just analyzing the given webpage and seeing at which hostname an email needs to be sent. It's the only hostname I saw at the website, and it was the right one too.

Now we have to find the first flag. This is where I tried to check the Page Source or any suspicious links, but I didn't have any luck. Gobuster was next.

```
root@ip-10-10-229-242:~# gobuster dir -u http://10.10.211.113 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.211.113
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 278]
/.hta                 (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/flags                (Status: 301) [Size: 314] [--> http://10.10.211.113/flags/]
/images               (Status: 301) [Size: 315] [--> http://10.10.211.113/images/]
/index.html           (Status: 200) [Size: 19188]
/layout               (Status: 301) [Size: 315] [--> http://10.10.211.113/layout/]
/pages                (Status: 301) [Size: 314] [--> http://10.10.211.113/pages/]
/server-status        (Status: 403) [Size: 278]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

There is a flag directory waving at us. Let's check it out.

<img width="479" height="228" alt="image" src="https://github.com/user-attachments/assets/eb55955e-3104-4ab6-9aba-42c568dfa8ef" />

Can you even imagine how I felt when seeing that? But when we click on the link

<img width="966" height="705" alt="image" src="https://github.com/user-attachments/assets/bd690533-0c03-42d8-85dc-881f926cf3de" />

Very funny. 😒 I was rickrolled in 2025. I can't believe it.

Not even further enumerating the directory led to anything and the other directories didn't really show any interesting results, if any.

This is where it hit me. The webserver is hosting multiple websites. That's why we were asked to find another domain name. To then be able to call it by host. For that we first need to open the etc/hosts file and add that domain name, which allows our system to resolve that hostname to a specific IP address without needing to query a DNS server. It's particularly useful for accessing local servers or services that may not be publicly available, so we map the domain to an IP in the hosts file

<img width="645" height="524" alt="image" src="https://github.com/user-attachments/assets/912b9750-fb27-4e1e-8f86-32eaef0b6d29" />

Now our Operating System can directly connect to the specified service. And indeed, when entering the domain name

<img width="969" height="203" alt="Bildschirmfoto vom 2025-10-02 15-41-05" src="https://github.com/user-attachments/assets/f70bd4ac-e193-41c2-ab6f-aa8c333d36d5" />

After having done that we had the possibility to look for a page under development now. As the domain name was not bruteforced with gobuster yet, I did that

```
root@ip-10-10-229-242:~# gobuster dir -u http://mafialive.thm/ -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://mafialive.thm/
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
/.htpasswd            (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/index.html           (Status: 200) [Size: 59]
/robots.txt           (Status: 200) [Size: 34]
/server-status        (Status: 403) [Size: 278]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

Which worked out. Let's check out the sites that web crawlers are disallowed from visiting, as that could very well be a page under development

<img width="969" height="164" alt="Bildschirmfoto vom 2025-10-02 15-45-32" src="https://github.com/user-attachments/assets/829e0ab9-7c1e-457d-b1ad-da1d716289d4" />

Right again. Now a second flag needs to be found. As there is no other directory I can think of where to look except the one that's disallowed I decide to check it out.

<img width="969" height="232" alt="image" src="https://github.com/user-attachments/assets/8be109d6-b599-4558-ad19-105b80fab318" />

Now on this test page we have a button that begs to be clicked. Probably wouldn't be a good idea in any other context, but let's just go for it.

<img width="969" height="217" alt="image" src="https://github.com/user-attachments/assets/403496c6-11ce-4981-80b9-74da7fc18a04" />

Now we see some text and the URL seems to have changed to 

http://mafialive.thm/test.php?view=/var/www/html/development_testing/mrrobot.php

Don't know what to do now though. This seems to have to do with LFI though, as we are redirecting this page to a Local File of the Server. We could maybe try manipulating the view parameter to include different files or paths on the server like  http://mafialive.thm/test.php?view=/etc/passwd

That didn't work though, so I tried traversing directories by using ../ to move up to the directory structure like http://mafialive.thm/test.php?view=../../etc/passwd, but that also didn't lead to any successes, as the output was repeatedly telling me

<img width="969" height="217" alt="image" src="https://github.com/user-attachments/assets/95c62e52-75c4-4359-bbe8-a448fb93c82d" />

I tried other approaches like PHP wrappers where we use php://filter to read files. For example http://mafialive.thm/test.php?view=php://filter/read=convert.base64-encode/resource=/var/www/html/development_testing/test.php, which worked successfully because it accessed a valid file that the web server can read

<img width="969" height="217" alt="Bildschirmfoto vom 2025-10-02 17-05-50" src="https://github.com/user-attachments/assets/b149271a-bb46-4186-9f73-3a7f1ca76441" />

The content of that file was base64 encoded and allowed us to view the contents in a readable format. When using Cyberchef we get the following output

<img width="725" height="737" alt="Bildschirmfoto vom 2025-10-02 17-08-45" src="https://github.com/user-attachments/assets/e478678d-8815-4cf7-af1f-c643f2ed505d" />

By looking clearly at the php source code we can also see how the other approaches didn't work and how the input was sanitized

```	
<!DOCTYPE HTML>
<html>

<head>
    <title>INCLUDE</title>
    <h1>Test Page. Not to be Deployed</h1>
 
    </button></a> <a href="/test.php?view=/var/www/html/development_testing/mrrobot.php"><button id="secret">Here is a button</button></a><br>
        <?php

	    //FLAG: thm{xxx}

            function containsStr($str, $substr) {
                return strpos($str, $substr) !== false;
            }
	    if(isset($_GET["view"])){
	    if(!containsStr($_GET['view'], '../..') && containsStr($_GET['view'], '/var/www/html/development_testing')) {
            	include $_GET['view'];
            }else{

		echo 'Sorry, Thats not allowed';
            }
	}
        ?>
    </div>
</body>

</html>
```

There were two if-conditions that were making sure that the usual LFI approaches wouldn't work. The first one being the one that checks for "../.." strings, but also another that was clearly stating that the "/var/www/html/development_testing" path needs to be included. This is how the website sanitizes the input. But we can work with that. We need to get a shell and find the user flag now, which will happen through Log Poisoning.
