The task was the following exercise:

<img width="982" height="297" alt="Bildschirmfoto vom 2025-08-13 17-04-06" src="https://github.com/user-attachments/assets/945df1d7-9f78-4345-abfb-66c717f42122" />

At the very beginning I tried to acces the website under the URL
https://futurevera.thm , which already didn’t work for some reason. I also tried to take the hint in account, but didn’t really know what to make out of the fact that we had to add 10.10.152.174 in /etc/hosts as I already was not able to access the main page.

After reconsidering the hint that this task is about Enumeration I researched on the web and came to the conclusion of using nmap first to see what could happen.

root@ip-10-10-161-86:~# nmap 10.10.152.174

Which gave the following results

Starting Nmap 7.80 ( https://nmap.org ) at 2025-08-13 16:21 BST
Nmap scan report for ip-10-10-152-174.eu-west-1.compute.internal (10.10.152.174)
Host is up (0.00049s latency).
Not shown: 997 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp open  https
MAC Address: 02:89:6F:18:13:45 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 0.29 seconds

I couldn’t do much with these informations so I resumed with running standard nmap scripts (-sC)

root@ip-10-10-161-86:~# nmap -sC 10.10.152.174
Starting Nmap 7.80 ( https://nmap.org ) at 2025-08-13 16:34 BST
Nmap scan report for ip-10-10-152-174.eu-west-1.compute.internal (10.10.152.174)
Host is up (0.0045s latency).
Not shown: 997 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
|_http-title: Did not follow redirect to https://futurevera.thm/
443/tcp open  https
|_http-title: FutureVera
| ssl-cert: Subject: commonName=futurevera.thm/organizationName=Futurevera/stateOrProvinceName=Oregon/countryName=US
| Not valid before: 2022-03-13T10:05:19
|_Not valid after:  2023-03-13T10:05:19
| tls-alpn: 
|_  http/1.1
MAC Address: 02:89:6F:18:13:45 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 2.22 seconds

I copied this output to ChatGPT and he recommended to add futurevera.thm to my /etc/hosts so my machine knows where to send requests, which is probably what was meant with the hint at the very beginning of the challenge. 

sudo nano /etc/hosts

I had to add the following information:

10.10.152.174 futurevera.thm

and save with Ctrl + O!

It then recommeded me to visit the website, which obviously wasn’t possible as I was already not able to enter it at the very beginning, but it also said I could try the http way, which made me curious, as I really tried to enter the URL the way it was requested from me, but not the secure way. I wasn’t even aware we could do that. Look I’m still a full fleshed amateur in Pentesting. I will look into why we have two different Hyptertext Protocols. For some reason I just thought you could only either have one or the other, but not both.

Anyways after looking up the page with http I looked at its source code.
Unfortunately nothing of interest was found. After that I tried to use dirb to see if there may were some pages that I could get access to.

root@ip-10-10-161-86:/# dirb https://futurevera.thm/

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Wed Aug 13 17:07:16 2025
URL_BASE: https://futurevera.thm/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: https://futurevera.thm/ ----
==> DIRECTORY: https://futurevera.thm/assets/                                  
==> DIRECTORY: https://futurevera.thm/css/                                     
+ https://futurevera.thm/index.html (CODE:200|SIZE:4605)                       
==> DIRECTORY: https://futurevera.thm/js/                                      
+ https://futurevera.thm/server-status (CODE:403|SIZE:280)                     
                                                                               
---- Entering directory: https://futurevera.thm/assets/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                               
---- Entering directory: https://futurevera.thm/css/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                               
---- Entering directory: https://futurevera.thm/js/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
                                                                               
-----------------
END_TIME: Wed Aug 13 17:07:21 2025
DOWNLOADED: 4612 - FOUND: 2

As we can see there were two pages that I could enter: /assets and /css. So I tried to abuse that to see if maybe I could use this to my advantage. Unfortunately or probably fortunately those sites were pretty clean. As clean as css can look. ChatGPT kept on pestering me how valuable it would be for me to use GoBuster, which I didn’t even know. He said it’s a tool with which we could brute-force possible URL’s based on a wordlist we give it. An example would be:

gobuster dir -u https://futurevera.thm -w /usr/share/wordlists/dirb/common.txt -k

The options would mean

    • dir → directory/file brute force mode.
    • -u → target URL.
    • -w → wordlist (common.txt is a popular one).
    • -k → ignore SSL errors (your cert is expired).
root@ip-10-10-161-86:/# gobuster dir -u https://futurevera.thm -w /usr/share/wordlists/dirb/common.txt -k
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     https://futurevera.thm
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 280]
/.htpasswd            (Status: 403) [Size: 280]
/.htaccess            (Status: 403) [Size: 280]
/assets               (Status: 301) [Size: 319] [--> https://futurevera.thm/assets/]
/css                  (Status: 301) [Size: 316] [--> https://futurevera.thm/css/]
/index.html           (Status: 200) [Size: 4605]
/js                   (Status: 301) [Size: 315] [--> https://futurevera.thm/js/]
/server-status        (Status: 403) [Size: 280]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================

I was also advised to maybe use a bigger dir wordlist as the default common.txt is only around ~4600 which is nothing compared to other text files like the directory-list-2.3-medium.txt, which contains ~220k entries instead. Still even after all that it returned about the same results with a much longer execution time. We were thorough with no real benefit. 
The last thing, which was also hinted by the tryhackme room itself was to try checking for subdomains. For that I checked the internet to see what kind of tools could be helpful in those kind of situations and remembered the ffuf tool. Suddenly I felt very dense and tried the following output:

root@ip-10-10-106-66:/etc# ffuf -w /usr/share/wordlists/SecLists/Discovery/DNS/namelist.txt -H "Host: FUZZ.futurevera.thm" -u http://10.10.57.13 -fs 0

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.57.13
 :: Wordlist         : FUZZ: /usr/share/wordlists/SecLists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.futurevera.thm
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response size: 0
________________________________________________

payroll                 [Status: 200, Size: 70, Words: 9, Lines: 2]
portal                  [Status: 200, Size: 69, Words: 9, Lines: 2]
:: Progress: [1907/1907] :: Job [1/1] :: 29642 req/sec :: Duration: [0:00:04] :: Errors: 0 ::

Obviously I only incoorperated the size flag after first running the command without it to see the most frequent size, which would be spit out. Now finally we had something we could really work with.

<img width="836" height="291" alt="grafik" src="https://github.com/user-attachments/assets/ae738ba4-bfd1-4e89-98bc-8def95a0442a" />

I proceeded to add these lines into /etc/hosts and was able to access these URLS in my browser.

I really thought I would have solved this task, but au contraire. I still seemed to miss something. I didn’t quite know what though, which is crazy as this task is only supposed to take four minutes. The Page Source didn’t have mentionable comments and even using ffuf again to enumerate paths or directories didn’t lead to anything 

root@ip-10-10-106-66:/etc# ffuf -u http://payroll.futurevera.thm/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1
________________________________________________

 :: Method           : GET
 :: URL              : http://payroll.futurevera.thm/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
________________________________________________

.htpasswd               [Status: 403, Size: 287, Words: 20, Lines: 10]
.htaccess               [Status: 403, Size: 287, Words: 20, Lines: 10]
.hta                    [Status: 403, Size: 287, Words: 20, Lines: 10]
index.html              [Status: 200, Size: 70, Words: 9, Lines: 2]
server-status           [Status: 403, Size: 287, Words: 20, Lines: 10]
:: Progress: [4655/4655] :: Job [1/1] :: 24412 req/sec :: Duration: [0:00:01] :: Errors: 0:: Progress: [4655/4655] :: Job [1/1] :: 134 req/sec :: Duration: [0:00:04] :: Errors: 0 ::
root@ip-10-10-106-66:/etc# ffuf -u http://portal.futurevera.thm/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1
________________________________________________

 :: Method           : GET
 :: URL              : http://portal.futurevera.thm/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
________________________________________________

.htpasswd               [Status: 403, Size: 286, Words: 20, Lines: 10]
.hta                    [Status: 403, Size: 286, Words: 20, Lines: 10]
.htaccess               [Status: 403, Size: 286, Words: 20, Lines: 10]
index.html              [Status: 200, Size: 69, Words: 9, Lines: 2]
server-status           [Status: 403, Size: 286, Words: 20, Lines: 10]
:: Progress: [4655/4655] :: Job [1/1] :: 22847 req/sec :: Duration: [0:00:04] :: Errors: 0 ::

Now I started checking assets, js, css – everything that could be some sort of hint. I still didn’t find any valuable information and decided to take a break here and think about what I could possibly have overlooked.

------------------------------------------------------------------------------------------------------------------------

After returning from my break I needed to restart the AttackBox so the new Target IP Address is called 10.10.215.76 just so that there is no confusion. The rest is still the same.
Still, having said that, I was still not able to figure out what I was overlooking. I tried to check for other subdomains in the subdomain, some brute-forcing in the directories and looking for API endpoints, but none of that helped out.

After watching a video I realised that everyone was finding subdomains like blog and support due to the HTTPS domain name. Yet again the duality of HTTP and HTTPS was my detriment and I tried to move on from there

root@ip-10-10-76-59:~# ffuf -w /usr/share/wordlists/SecLists/Discovery/DNS/namelist.txt -H "Host: FUZZ.futurevera.thm" -u https://10.10.215.76 -fs 4605

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1
________________________________________________

 :: Method           : GET
 :: URL              : https://10.10.215.76
 :: Wordlist         : FUZZ: /usr/share/wordlists/SecLists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.futurevera.thm
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response size: 4605
________________________________________________

:: Progress: [40/1907] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errorsblog                    [Status: 200, Size: 3838, Words: 1326, Lines: 81]
:: Progress: [204/1907] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [207/1907] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [357/1907] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [496/1907] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [751/1907] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [983/1907] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [1192/1907] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erro:: Progress: [1455/1907] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errosupport                 [Status: 200, Size: 1522, Words: 367, Lines: 34]
:: Progress: [1625/1907] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erro:: Progress: [1665/1907] :: Job [1/1] :: 2052 req/sec :: Duration: [0:00:01] :: E:: Progress: [1907/1907] :: Job [1/1] :: 2064 req/sec :: Duration: [0:00:01] :: E:: Progress: [1907/1907] :: Job [1/1] :: 2318 req/sec :: Duration: [0:00:01] :: Errors: 0 ::

After having done this command we now could also check out the subdomain of blog and support, which reminded me of the exercise task that clearly stated. 

„We do a lot of space research and write blogs about it. We used to help students with space questions, but we are rebuilding our support.“

That was a hint and I checked out the support site…

Unfortunately I still had to look up YouTube videos after this. I did not realize that I had to look up the certificate of said site. How should I have known? I will make notes of it though. There we got information of another DNS Name called secrethelpdesk934752.support.futurevera.thm 
that I immediately saved as such in the editor and accessed after that. Once again I had difficulties because I used the HTTPS protocol instead of HTTP :)
After having figured that out I finally got the flag that I desperately was looking for:

<img width="836" height="829" alt="grafik" src="https://github.com/user-attachments/assets/b45e3a6d-a244-4631-9466-0640d4449fc1" />

For the very first challenge, that was only supposed to take around 4 minutes I really took my time. I can only hope that I will learn from this and can make some notes on what to do better next time. If I start doing a daily activity out of this I can only hope to improve more and more. We will see, how my skills will evolve. For now I will rest and celebrate this (small) victory, even with all the tools and helper videos I had to take.
