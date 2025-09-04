# Challenge 018 - Fowsniff CTF

This one was considered an easy challenge, with many hints along the way, so I decided to go for it. In this boot2root machine we will enumerate to find open ports, decode hashes, brute force hashes and much more. I'm already very curious on what will await me. At the beginnign we just need to deploy the machine. Easy.

<img width="820" height="933" alt="Bildschirmfoto vom 2025-09-05 00-54-01" src="https://github.com/user-attachments/assets/a0431a3c-d2ac-419e-be49-1eef3e1e2207" />

After having done that, we have to use nmao to check for open ports again. As i felt lazy I just used the -p- flag.

<img width="735" height="320" alt="image" src="https://github.com/user-attachments/assets/be42ff7c-135b-49a0-b830-a695096ba276" />

As we can see there are exactly 4 ports open. The one for http (80), used for unencrypted web traffic, the ssh (22), which is the port used by the secure shell protocol to faciliate secure connections, the one for pop3 (110), which is used for unencrypted connection and the imap port (143), which is the default IMAP port for unencrypted (plain text) connections.

<img width="973" height="873" alt="image" src="https://github.com/user-attachments/assets/ec4919ca-2d42-435f-86ad-af456d14c196" />

When we check out the http website, we get the notification that it would temporarily be out of service as there was a data breach. A hacker apparently hijacked the website and got a hold of all usernames and passwords, which could very well be leaked at Twitter in a future date.

```
root@ip-10-10-43-10:~# gobuster dir -u http://10.10.22.125 -w big.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.22.125
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/images               (Status: 301) [Size: 313] [--> http://10.10.22.125/images/]
/assets               (Status: 301) [Size: 313] [--> http://10.10.22.125/assets/]
/server-status        (Status: 403) [Size: 300]
Progress: 1273834 / 1273835 (100.00%)
===============================================================
Finished
===============================================================
```

Thats
