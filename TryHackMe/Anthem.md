<h1 align="center">Challenge 031 - Anthem </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/2b1bf64b-e488-4a64-9e95-a2a4769d6234" alt="Sakura Room" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 2/10 (Easy) <b>Completed</b>: ✔️ 01.10.2025  </p>

This challenge is all about exploting a Windows machine. It once again is very beginner friendly so I should be able to beat it. Let's see how I will manage it.

## Website Analysis

We begin with the usual which is the scanning of the ports to see how many of them are open.

```
root@ip-10-10-39-7:~# nmap -p- -sV 10.10.177.180
Starting Nmap 7.80 ( https://nmap.org ) at 2025-10-01 16:14 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.177.180
Host is up (0.028s latency).
Not shown: 65532 filtered ports
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
3389/tcp open  ms-wbt-server Microsoft Terminal Services
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
MAC Address: 02:CB:EB:8E:40:97 (Unknown)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 155.32 seconds
```

We have the common ports like port 80 resposible for the web server, but also port 3389, which is a remote desktop service (RDP), developed by Microsoft to enable users to control a remote computer from another device over a network.

When visiting the http site we see the following site.

<img width="1133" height="763" alt="Bildschirmfoto vom 2025-10-01 17-21-08" src="https://github.com/user-attachments/assets/b5cc835b-a7a1-4105-ac75-3dc56a4ed5ba" />

It seems to be a blog of someone.

### robots.txt

Anyways. Our next task is finding out what is a possible password one of the pages web crawlers would check for? I assumed that we could check the robots.txt file of the web server for that and I also got some insight through that.

<img width="451" height="281" alt="Bildschirmfoto vom 2025-10-01 17-29-38" src="https://github.com/user-attachments/assets/761ae911-6585-4d56-a5f8-4f77c36d0f51" />

Jackpot. We were successful.

Moving on we have to find out what kind of CMS the website is using. A Content Management System that continuously gets mentioned - even in the robots.txt file - is Umbraco.

<div align="center">
  <img width="150" height="150" alt="image" src="https://github.com/user-attachments/assets/deb4353a-6306-4164-8760-986561ee066d" />
</div>

Right again. Never heard of it. The more you know.

The next question was still fairly easy. What is the domain of the website? I mean. We already checked the blog, where the name was displayed clear as day. I will refrain from further talking about this and keep on going with the next task.

### OSINT

Now we get to a little riddle which promises to be very fun. It's about finding out the name of the Administrator. When checking out the blog posts of the homepage we also see one post that is dedicated to the admin himself.

<img width="732" height="699" alt="image" src="https://github.com/user-attachments/assets/e0ab5d3b-603f-4830-96f3-dba66132f13d" />

I don't recognize this poem, but maybe our beloved search engine will.

<img width="1057" height="324" alt="Bildschirmfoto vom 2025-10-01 19-05-29" src="https://github.com/user-attachments/assets/5494a08e-3053-4d74-8bba-d4bc1c9a1125" />

It very much did. Beautiful.

Now the last task for this section was to find the email address of the administrator. Might seem difficult at first, but it really isn't. We get a huge hint at what it could be by just checking the first blog post

<img width="691" height="528" alt="image" src="https://github.com/user-attachments/assets/58872d5e-9d47-413c-a2d7-336cddd6d08e" />

If the email addresses on this website all follow the same pattern, it should be very evident what the email of the Administrator should be.

## Spot the flags

Now with this out of the way it's time to spot some flags. For that I tried the usual and just inspecting the Page Source. I immediately found 2 (!) flags.

To further enumerate we checked out all the links and pages we could click on this website including the page of Jane Doe.

<img width="689" height="488" alt="Bildschirmfoto vom 2025-10-01 19-24-16" src="https://github.com/user-attachments/assets/59b2e651-3c2d-40a1-a8af-b4a2e14df496" />

For this last flag I searched and searched and finally had luck when inspecting the second blog post again through the Page Source. Those were some very easily hidden flags. Almost too easy. But I won't complain as this reminded me of the fact how important it sometimes can be to check the Page Source of EVERY post.

## Final Stage

Now we will probably have to get into the box. For that it would pronbably be for the best to check for hidden directories like login pages with gobuster. Note: The performance of this VM was very poor, so the results might look a little weird, but it still led to results

```
root@ip-10-10-39-7:~# gobuster dir -u 10.10.177.180 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.177.180
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/archive              (Status: 301) [Size: 118] [--> /]
/Archive              (Status: 301) [Size: 118] [--> /]
/authors              (Status: 200) [Size: 4075]
Progress: 593 / 4615 (12.85%)[ERROR] Get "http://10.10.177.180/aux": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
/blog                 (Status: 200) [Size: 5399]
/Blog                 (Status: 200) [Size: 5399]
/categories           (Status: 200) [Size: 3546]
Progress: 995 / 4615 (21.56%)[ERROR] Get "http://10.10.177.180/com1": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
[ERROR] Get "http://10.10.177.180/com2": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
[ERROR] Get "http://10.10.177.180/com3": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
Progress: 1042 / 4615 (22.58%)[ERROR] Get "http://10.10.177.180/con": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
/install              (Status: 302) [Size: 126] [--> /umbraco/]
Progress: 2417 / 4615 (52.37%)[ERROR] Get "http://10.10.177.180/lpt1": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
Progress: 2419 / 4615 (52.42%)[ERROR] Get "http://10.10.177.180/lpt2": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
Progress: 2760 / 4615 (59.80%)[ERROR] Get "http://10.10.177.180/nul": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
Progress: 2894 / 4615 (62.71%)[ERROR] Get "http://10.10.177.180/pbcsad": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
Progress: 3178 / 4615 (68.86%)[ERROR] Get "http://10.10.177.180/prn": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
/robots.txt           (Status: 200) [Size: 192]
/RSS                  (Status: 200) [Size: 1877]
/rss                  (Status: 200) [Size: 1877]
/search               (Status: 200) [Size: 3472]
/Search               (Status: 200) [Size: 3472]
/sitemap              (Status: 200) [Size: 1047]
/SiteMap              (Status: 200) [Size: 1047]
/tags                 (Status: 200) [Size: 3599]
/umbraco              (Status: 200) [Size: 4078]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

Checking the install directory might be the best option for now and indeed, we see a login page now.

<img width="908" height="619" alt="image" src="https://github.com/user-attachments/assets/07e9a6ec-2330-4f05-b3b5-8930ad6d8e89" />

Ain't that pretty? I tried to use basic SQL injection to get in, but that didn't really work. After a quick second I remembered that we already got a hold of usernames and password. Silly me! ⭐

<img width="1154" height="768" alt="Bildschirmfoto vom 2025-10-01 20-10-04" src="https://github.com/user-attachments/assets/d7e052ca-936b-42e4-ac29-0a18c8f5d67b" />

We are in. Now the task is to gain initial access to the machine and find out the contents of user.txt. I remember there was a place in Umbraco where we could upload a file. Maybe even a Reverse Shell?

### rdesktop

It's only after a while that I understood that the Windows machine I was trying to access is not part of a corporate or organization domain (THE BOX IS NOT A DOMAIN). We were supposed to get remote acces through our terminal. I searched for some useful commands, which we could make use of and found rdesktop to be the perfect fit for this task


```
root@ip-10-10-39-7:~# rdesktop 10.10.177.180
Autoselecting keyboard map 'en-gb' from locale

ATTENTION! The server uses and invalid security certificate which can not be trusted for
the following identified reasons(s);

 1. Certificate issuer is not trusted by this system.

     Issuer: CN=WIN-LU09299160F


Review the following certificate info before you trust it to be added as an exception.
If you do not trust the certificate the connection atempt will be aborted:

    Subject: CN=WIN-LU09299160F
     Issuer: CN=WIN-LU09299160F
 Valid From: Tue Sep 30 15:49:24 2025
         To: Wed Apr  1 15:49:24 2026

  Certificate fingerprints:

       sha1: a35a81ce62932ab4d11d1d2a61fc163735bd9c7a
     sha256: 5ecbe15e2da94ef624c1692cb6a127a4dab13a078df2ac2bf3d569acd96ac837


Do you trust this certificate (yes/no)? yes
```

After confirming we now enabled a graphical desktop environment on Windows machines from Linux. We can perform tasks on remote Windows systems as if we were physically present at the machine.

<img width="974" height="792" alt="image" src="https://github.com/user-attachments/assets/6cbef0e6-4570-41dd-b606-1dd563137381" />

Booyah. After the succesful login the user.txt file is displayed on plain sight.

<img width="974" height="792" alt="image" src="https://github.com/user-attachments/assets/57ec7185-bcee-4954-8e3c-cd4285ef03ad" />

### Modification of Permissions

For our penultimate task we are asked to spot some admin password. After enumerating through a lot of directories I needed a hint, so I asked for a one, which was that the file would be hidden. So we click the option "View" and check the checkbox for "Hidden Items". Immediately after that I found a backup directory in the Local Disk (C:). We couldn't open the restore.txt though as we didn't have the permissions for it. Yet. I right clicked on Properties and changed permission by clicking on the "Edit" button of the Security option.

<img width="974" height="792" alt="Bildschirmfoto vom 2025-10-01 21-11-32" src="https://github.com/user-attachments/assets/14658c2e-2a80-4629-a94e-6d6efae8b266" />

By adding "everyone" and applying said modifications all groups and usernames should now be able to open said file.

<img width="355" height="449" alt="image" src="https://github.com/user-attachments/assets/fbb27f13-fcfc-4977-9770-388529223dce" />

And indeed. After trying to open said file again I was immediately welcomed by the admin password.

<img width="239" height="80" alt="Bildschirmfoto vom 2025-10-01 21-14-07" src="https://github.com/user-attachments/assets/397fc5f8-1a2e-4d73-8608-2a19d905ecc8" />

### Privilege Escalation

Now the very last thing to do is escalating our privileges to root. I just decided to end the session with this terminal and login again with the credentials of the Administrator

<img width="784" height="592" alt="image" src="https://github.com/user-attachments/assets/897530c1-2064-4eab-8a95-2fcf84f278a5" />

That seemed to have worked out just fine.

<img width="975" height="793" alt="image" src="https://github.com/user-attachments/assets/1a7d33f2-d383-468a-9b5f-69b286697cc1" />

And the root.txt is in plain sight once again. Maybe I could have done this through the Power Shell as well, but I was too lazy and everything seemed to have worked just fine for this challenge so it doesn't matter much.

I learned to make use of some commands which could give us remote access to a Windows Operating System through Linux and how to escalate priviliges in a Windows environment. This really gave me the motivation to check on the Power Shell once again and try to get acquainted with it. It might also seem silly but a secret fascination was piqued over time with all these different ports holding different kinds of application and me always interacting with them in some kind of way. It motivates me to create some sort of checklist for all the ports and services I succesfully analyzed over my history of CTFs. It's silly but there is a real fascination there.
