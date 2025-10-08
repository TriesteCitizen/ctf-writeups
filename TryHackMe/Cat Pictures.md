<h1 align="center">Challenge 038 - Cat Pictures </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/26c7885f-96c8-4966-9250-bb2942d28f61" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️  </p>

I want to see cat pictures to ease my mind. Don't judge. We deploy the machine and run the usual nmap scan.

```
root@ip-10-10-161-37:~# nmap -p- -sV -A 10.10.62.180
Starting Nmap 7.80 ( https://nmap.org ) at 2025-10-07 18:46 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.62.180
Host is up (0.00029s latency).
Not shown: 65530 closed ports
PORT     STATE    SERVICE      VERSION
21/tcp   filtered ftp
22/tcp   open     ssh          OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 37:43:64:80:d3:5a:74:62:81:b7:80:6b:1a:23:d8:4a (RSA)
|   256 53:c6:82:ef:d2:77:33:ef:c1:3d:9c:15:13:54:0e:b2 (ECDSA)
|_  256 ba:97:c3:23:d4:f2:cc:08:2c:e1:2b:30:06:18:95:41 (ED25519)
2375/tcp filtered docker
4420/tcp open     nvm-express?
| fingerprint-strings: 
|   DNSVersionBindReqTCP, GenericLines, GetRequest, HTTPOptions, RTSPRequest: 
|     INTERNAL SHELL SERVICE
|     please note: cd commands do not work at the moment, the developers are fixing it at the moment.
|     ctrl-c
|     Please enter password:
|     Invalid password...
|     Connection Closed
|   NULL, RPCCheck: 
|     INTERNAL SHELL SERVICE
|     please note: cd commands do not work at the moment, the developers are fixing it at the moment.
|     ctrl-c
|_    Please enter password:
8080/tcp open     http         Apache httpd 2.4.46 ((Unix) OpenSSL/1.1.1d PHP/7.3.27)
| http-open-proxy: Potentially OPEN proxy.
|_Methods supported:CONNECTION
|_http-server-header: Apache/2.4.46 (Unix) OpenSSL/1.1.1d PHP/7.3.27
|_http-title: Cat Pictures - Index page
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port4420-TCP:V=7.80%I=7%D=10/7%Time=68E5520A%P=x86_64-pc-linux-gnu%r(NU
SF:LL,A0,"INTERNAL\x20SHELL\x20SERVICE\nplease\x20note:\x20cd\x20commands\
SF:x20do\x20not\x20work\x20at\x20the\x20moment,\x20the\x20developers\x20ar
SF:e\x20fixing\x20it\x20at\x20the\x20moment\.\ndo\x20not\x20use\x20ctrl-c\
SF:nPlease\x20enter\x20password:\n")%r(GenericLines,C6,"INTERNAL\x20SHELL\
SF:x20SERVICE\nplease\x20note:\x20cd\x20commands\x20do\x20not\x20work\x20a
SF:t\x20the\x20moment,\x20the\x20developers\x20are\x20fixing\x20it\x20at\x
SF:20the\x20moment\.\ndo\x20not\x20use\x20ctrl-c\nPlease\x20enter\x20passw
SF:ord:\nInvalid\x20password\.\.\.\nConnection\x20Closed\n")%r(GetRequest,
SF:C6,"INTERNAL\x20SHELL\x20SERVICE\nplease\x20note:\x20cd\x20commands\x20
SF:do\x20not\x20work\x20at\x20the\x20moment,\x20the\x20developers\x20are\x
SF:20fixing\x20it\x20at\x20the\x20moment\.\ndo\x20not\x20use\x20ctrl-c\nPl
SF:ease\x20enter\x20password:\nInvalid\x20password\.\.\.\nConnection\x20Cl
SF:osed\n")%r(HTTPOptions,C6,"INTERNAL\x20SHELL\x20SERVICE\nplease\x20note
SF::\x20cd\x20commands\x20do\x20not\x20work\x20at\x20the\x20moment,\x20the
SF:\x20developers\x20are\x20fixing\x20it\x20at\x20the\x20moment\.\ndo\x20n
SF:ot\x20use\x20ctrl-c\nPlease\x20enter\x20password:\nInvalid\x20password\
SF:.\.\.\nConnection\x20Closed\n")%r(RTSPRequest,C6,"INTERNAL\x20SHELL\x20
SF:SERVICE\nplease\x20note:\x20cd\x20commands\x20do\x20not\x20work\x20at\x
SF:20the\x20moment,\x20the\x20developers\x20are\x20fixing\x20it\x20at\x20t
SF:he\x20moment\.\ndo\x20not\x20use\x20ctrl-c\nPlease\x20enter\x20password
SF::\nInvalid\x20password\.\.\.\nConnection\x20Closed\n")%r(RPCCheck,A0,"I
SF:NTERNAL\x20SHELL\x20SERVICE\nplease\x20note:\x20cd\x20commands\x20do\x2
SF:0not\x20work\x20at\x20the\x20moment,\x20the\x20developers\x20are\x20fix
SF:ing\x20it\x20at\x20the\x20moment\.\ndo\x20not\x20use\x20ctrl-c\nPlease\
SF:x20enter\x20password:\n")%r(DNSVersionBindReqTCP,C6,"INTERNAL\x20SHELL\
SF:x20SERVICE\nplease\x20note:\x20cd\x20commands\x20do\x20not\x20work\x20a
SF:t\x20the\x20moment,\x20the\x20developers\x20are\x20fixing\x20it\x20at\x
SF:20the\x20moment\.\ndo\x20not\x20use\x20ctrl-c\nPlease\x20enter\x20passw
SF:ord:\nInvalid\x20password\.\.\.\nConnection\x20Closed\n");
MAC Address: 02:6E:A4:3C:D5:D7 (Unknown)what does ssd do?
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.80%E=4%D=10/7%OT=22%CT=1%CU=37795%PV=Y%DS=1%DC=D%G=Y%M=026EA4%T
OS:M=68E55259%P=x86_64-pc-linux-gnu)SEQ(SP=108%GCD=1%ISR=109%TI=Z%CI=Z%II=I
OS:%TS=A)OPS(O1=M2301ST11NW7%O2=M2301ST11NW7%O3=M2301NNT11NW7%O4=M2301ST11N
OS:W7%O5=M2301ST11NW7%O6=M2301ST11)WIN(W1=F4B3%W2=F4B3%W3=F4B3%W4=F4B3%W5=F
OS:4B3%W6=F4B3)ECN(R=Y%DF=Y%T=40%W=F507%O=M2301NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T
OS:=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R
OS:%O=%RD=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=
OS:40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0
OS:%Q=)U1(R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R
OS:=Y%DFI=N%T=40%CD=S)

Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.29 ms 10.10.62.180

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 89.77 seconds
```

After that thorough scan we can see that the usual ports - port 80 for http, port 21 for ftp and port 22 for ssh are open. There also seems to be a port 4420, which is responsible for nvm-express. It is an open-standard interface and protocol designed for high-speed solid-state drives (SSD) using PCI Express (PCIe) to fully leverage their non-volatile memory (NVM) capabilities.

Another http port on 8080 serves an Apache site. We can't access the website that is serving on port 80, so we move on to the Apache site on port 8080 and can see the following

<img width="1148" height="709" alt="image" src="https://github.com/user-attachments/assets/35045ffa-88d7-4c1a-95c9-5a419ce8b6c0" />

I click on the post to get these information

<img width="942" height="358" alt="image" src="https://github.com/user-attachments/assets/e49eee05-2194-46d2-a28b-9d670273fb4b" />

As I was not really sure what do to with the hint of said message I just decided to check out the version of this PHPbb site. By googling I found out the version could be queried by checking out the directory styles/prosilver/style.cfg

<img width="974" height="617" alt="image" src="https://github.com/user-attachments/assets/b80c3fff-170a-4b7e-a4fc-d732f4912349" />


