<h1 align="center">Challenge 046 - CyberHeroes </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/ccb9f595-a6e8-4708-a056-aca3f2a78815" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 31.10.2025 </p>

This challenge emphasizes Authentication Bypass and thus expects us to find a way to log in to an elite club of CyberHeroes. Just out of habit I do an nmap scan

```
root@ip-10-10-114-25:~# nmap -sV -p- 10.10.15.100
Starting Nmap 7.80 ( https://nmap.org ) at 2025-10-31 11:27 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.15.100
Host is up (0.00017s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.48 ((Ubuntu))
MAC Address: 02:DF:AA:7C:92:A5 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.23 seconds
```

The usual suspects ssh and http are open. We visit the http website to see what we can gather from there

<img width="1153" height="758" alt="grafik" src="https://github.com/user-attachments/assets/88e3e049-e545-4630-827e-6123a9ce914e" />

The main page looks like this. At the top right corner we also have the option to check out the About and Login page. In the About page we can gather the following information.

<img width="1153" height="758" alt="grafik" src="https://github.com/user-attachments/assets/e294765d-49a0-49a1-a947-76bf06940dc8" />

It all leads to the login page at the end.

<img width="1136" height="733" alt="grafik" src="https://github.com/user-attachments/assets/324239de-e8d5-4a0e-ad73-399fc12fd453" />

I tried the usual contenders for authentification like admin:admin but instead get the following result

<img width="498" height="127" alt="grafik" src="https://github.com/user-attachments/assets/02c1b724-76b1-4a8a-8981-f85bc83e9535" />

For now I decided to check out the Page Source for some clues, and there indeed was a lot we could work with in form of JavaScript. Seems like there is a function called authenticate() that takes care of the whole login process, which is highly insecure, when - like in this instance - it happens on the client-side.

```
  <script>
    function authenticate() {
      a = document.getElementById('uname')
      b = document.getElementById('pass')
      const RevereString = str => [...str].reverse().join('');
      if (a.value=="h3ck3rBoi" & b.value==RevereString("54321@terceSrepuS")) { 
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            document.getElementById("flag").innerHTML = this.responseText ;
            document.getElementById("todel").innerHTML = "";
            document.getElementById("rm").remove() ;
          }
        };
        xhttp.open("GET", "RandomLo0o0o0o0o0o0o0o0o0o0gpath12345_Flag_"+a.value+"_"+b.value+".txt", true);
        xhttp.send();
      }
      else {
        alert("Incorrect Password, try again.. you got this hacker !")
      }
    }
  </script>
```

Even I can read that sort of source code. The username is pretty evident. The password itself was also just reversed and can easily be recovered. If we use these credentials as input we get the flag.

<img width="648" height="211" alt="Bildschirmfoto vom 2025-10-31 12-49-57" src="https://github.com/user-attachments/assets/b4d17066-da1d-4097-9714-5b725c271def" />

## Lesson Learned
It's highly inpractical and dangerous to write client-side login methods, as it's prone to expose vulnerabilities such as XSS. Server-side logins should always be the preferred choice in these instances, as they keep sensitive logic on the server where it can't be tampered with directly.   
