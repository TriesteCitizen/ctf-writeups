# Challenge 007 - Jax sucks alot...........

Difficulty: 
Completed: 

Another day, another CTF. This time with a challenge that probably wants us to work with some sort of code injection.

<img width="758" height="369" alt="image" src="https://github.com/user-attachments/assets/112c5078-74bf-4851-a2c7-18ec2d95e298" />

When visiting the Target IP address we see a field, where the email has to be written. As the task already hints my presumption is that we have to write some JavaScript to abuse the vulnerability or maybe just use some command injection, so I first tried some more basic payloads to see what could happen. The result was disappointing as I didn’t see anything, which made sense, because this is a pretty common XSS situation. I still had to work out how we abuse those, so I put this room on pause and first finished the room that functions as the Into to Cross-site Scripting.
After having done that I returned and tried the basic call of an alert function

<img width="985" height="842" alt="image" src="https://github.com/user-attachments/assets/caa8d1e1-7556-48db-baf8-86d0fb0766a8" />

It didn’t quite work as intended but it gave a big hint. As we can see the script is not executed, but it’s also not being displayed completely. Maybe I could check the source code or the inspector to see what was going on with my POST Request.

If I use the input 
```
"><script>alert('THM');</script>
```
I get an output, where the output tells me that I’m being updated at: guest, which doesn’t make sense, but maybe we can use this to our advantage. 
I checked GitHub for an XSS Payload list and tried to play around with some commands, to see what else could be used to my advantage.

None of that seemed to work though. I was adviced to use nmap to check for ports, which just gave me the same results as I already anticipated. Not much to do there.
Also bruteforcing hidden directories also didn’t help as we were greeted with the following message:
```
root@ip-10-10-136-126:~# gobuster dir -u http://10.10.67.192 -w /root/script.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.67.192
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /root/script.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================

Error: the server returns a status code that matches the provided options for non existing urls. http://10.10.67.192/1139160d-fd91-4e20-b410-e5aa4760eb6a => 200 (Length: 3559). To continue please exclude the status code or the length
```

We clearly need to do some XSS 
The input is not being sanitized properly as we remember from writing that script alert prompt. We can try to use different payloads to see if we can achieve script execution, such as „onmouseover=“alert(‘XSS‘)“

Best way to find a vulnerability is to use the Burp Suite and check the parameters and maybe even modify them to my liking when using the alert command we intercept the following message:

<img width="956" height="468" alt="image" src="https://github.com/user-attachments/assets/fffcbd82-d1f3-4928-a409-84d24d2344d4" />

As we can see from the Request Body the web application is URL-encoding our input, which is common behavior to prevent direct injection attacks. The %3C and %3E represent < and >, respectively, while %27 represents the single quote ‘. This encoding is part of how the server processes data to maintain security

<img width="720" height="384" alt="image" src="https://github.com/user-attachments/assets/5219ff6e-bbce-4269-a8b7-f9568d87a9bd" />

As you can see when putting the session cookie into Cyberchef we realize that the value was Base64 encoded (which we can also recognize through the '==' at the end) and returns a JSON object. We are serializing data to fetch our session cookie. To abuse that vulnerability we can google for ways to abuse deserialization in node.js. An article was talking about the fact that insecure deserialization in node.js would have been in the OWASP top 10 in 2017. Attackers would be able to transfer payloads using serialized objects. This happens when integritiy checks are not in place, which totally is the case here.
