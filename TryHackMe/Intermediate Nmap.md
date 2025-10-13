<h1 align="center">Challenge 042 - Intermediate Nmap </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/1de8ff3b-ae68-430a-b185-1e7316866470" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 13.10.2025  </p>

This CTF is supposed to be an easy riddle, which expects us to combine our nmap skills with other commands like netcat to login to a machine and find the flag. Furthermore we are also given the hint that this VM 10.10.111.86 is listening on a high port and might reveal some information we can use to connect to a lower port commonly used for remote access.

Honestly this can't even be called a hint anymore. It's clear as day that we need to set up a netcat listener, while we run the nmap command. This will probably reveal some information to us.

So we start by scanning the ports first with nmap to reveal some information.

```
root@ip-10-10-112-225:~# nmap -p- -sV -A 10.10.111.86
Starting Nmap 7.80 ( https://nmap.org ) at 2025-10-13 16:58 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.111.86
Host is up (0.00027s latency).
Not shown: 65532 closed ports
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
2222/tcp  open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
31337/tcp open  Elite?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NULL, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, X11Probe: 
|     In case I forget - user:pass
|_    ubuntu:Dafdas!!/str0ng
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port31337-TCP:V=7.80%I=7%D=10/13%Time=68ED219A%P=x86_64-pc-linux-gnu%r(
SF:NULL,35,"In\x20case\x20I\x20forget\x20-\x20user:pass\nubuntu:Dafdas!!/s
SF:tr0ng\n\n")%r(GetRequest,35,"In\x20case\x20I\x20forget\x20-\x20user:pas
SF:s\nubuntu:Dafdas!!/str0ng\n\n")%r(SIPOptions,35,"In\x20case\x20I\x20for
SF:get\x20-\x20user:pass\nubuntu:Dafdas!!/str0ng\n\n")%r(GenericLines,35,"
SF:In\x20case\x20I\x20forget\x20-\x20user:pass\nubuntu:Dafdas!!/str0ng\n\n
SF:")%r(HTTPOptions,35,"In\x20case\x20I\x20forget\x20-\x20user:pass\nubunt
SF:u:Dafdas!!/str0ng\n\n")%r(RTSPRequest,35,"In\x20case\x20I\x20forget\x20
SF:-\x20user:pass\nubuntu:Dafdas!!/str0ng\n\n")%r(RPCCheck,35,"In\x20case\
SF:x20I\x20forget\x20-\x20user:pass\nubuntu:Dafdas!!/str0ng\n\n")%r(DNSVer
SF:sionBindReqTCP,35,"In\x20case\x20I\x20forget\x20-\x20user:pass\nubuntu:
SF:Dafdas!!/str0ng\n\n")%r(DNSStatusRequestTCP,35,"In\x20case\x20I\x20forg
SF:et\x20-\x20user:pass\nubuntu:Dafdas!!/str0ng\n\n")%r(Help,35,"In\x20cas
SF:e\x20I\x20forget\x20-\x20user:pass\nubuntu:Dafdas!!/str0ng\n\n")%r(SSLS
SF:essionReq,35,"In\x20case\x20I\x20forget\x20-\x20user:pass\nubuntu:Dafda
SF:s!!/str0ng\n\n")%r(TerminalServerCookie,35,"In\x20case\x20I\x20forget\x
SF:20-\x20user:pass\nubuntu:Dafdas!!/str0ng\n\n")%r(TLSSessionReq,35,"In\x
SF:20case\x20I\x20forget\x20-\x20user:pass\nubuntu:Dafdas!!/str0ng\n\n")%r
SF:(Kerberos,35,"In\x20case\x20I\x20forget\x20-\x20user:pass\nubuntu:Dafda
SF:s!!/str0ng\n\n")%r(SMBProgNeg,35,"In\x20case\x20I\x20forget\x20-\x20use
SF:r:pass\nubuntu:Dafdas!!/str0ng\n\n")%r(X11Probe,35,"In\x20case\x20I\x20
SF:forget\x20-\x20user:pass\nubuntu:Dafdas!!/str0ng\n\n")%r(FourOhFourRequ
SF:est,35,"In\x20case\x20I\x20forget\x20-\x20user:pass\nubuntu:Dafdas!!/st
SF:r0ng\n\n")%r(LPDString,35,"In\x20case\x20I\x20forget\x20-\x20user:pass\
SF:nubuntu:Dafdas!!/str0ng\n\n")%r(LDAPSearchReq,35,"In\x20case\x20I\x20fo
SF:rget\x20-\x20user:pass\nubuntu:Dafdas!!/str0ng\n\n")%r(LDAPBindReq,35,"
SF:In\x20case\x20I\x20forget\x20-\x20user:pass\nubuntu:Dafdas!!/str0ng\n\n
SF:")%r(LANDesk-RC,35,"In\x20case\x20I\x20forget\x20-\x20user:pass\nubuntu
SF::Dafdas!!/str0ng\n\n")%r(TerminalServer,35,"In\x20case\x20I\x20forget\x
SF:20-\x20user:pass\nubuntu:Dafdas!!/str0ng\n\n");
MAC Address: 02:56:E8:A5:12:59 (Unknown)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.80%E=4%D=10/13%OT=22%CT=1%CU=42626%PV=Y%DS=1%DC=D%G=Y%M=0256E8%
OS:TM=68ED21A6%P=x86_64-pc-linux-gnu)SEQ(SP=106%GCD=1%ISR=10B%TI=Z%CI=Z%II=
OS:I%TS=A)OPS(O1=M5B4ST11NW7%O2=M5B4ST11NW7%O3=M5B4NNT11NW7%O4=M5B4ST11NW7%
OS:O5=M5B4ST11NW7%O6=M5B4ST11)WIN(W1=FE88%W2=FE88%W3=FE88%W4=FE88%W5=FE88%W
OS:6=FE88)ECN(R=Y%DF=Y%T=3F%W=FAF0%O=M5B4NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=3F%S=
OS:O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=3F%W=0%S=A%A=Z%F=R%O=%RD
OS:=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0
OS:%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1
OS:(R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI
OS:=N%T=40%CD=S)

Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.27 ms 10.10.111.86

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.28 seconds
```

Well... that's awkward. I wanted to set up the netcat listener to retrieve some information, but this command already reveals way more than I expected. Let me just set up the listener to see what the output would be there.

```
root@ip-10-10-112-225:~# nc 10.10.111.86 31337
In case I forget - user:pass
ubuntu:Dafdas!!/str0ng
```

After establishing a connection to the service running on port 31337 of the target machine (10.10.111.86) we get valuable information. This port was likely configured to listen for incoming connections, and when we connected, the service responded, providing us with the output that may contain valuable information such as prompts, messages or in this case even credentials. The lesson in this task was to scan ports and identify open ones, indicating that a service is actively listening for connections, returning output after using the netcat command.

Now with these credentials we can try to login to ssh as per usual.

```
root@ip-10-10-112-225:~# ssh ubuntu@10.10.111.86
The authenticity of host '10.10.111.86 (10.10.111.86)' can't be established.
ECDSA key fingerprint is SHA256:tD+Aiagv/4teueystsEl6q9ZNvNF9C8v+dsZj3fhbdQ.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.111.86' (ECDSA) to the list of known hosts.
ubuntu@10.10.111.86's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.13.0-1014-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

$ whoami
ubuntu
```

While looking for the flag, we can see another user exists in the home directory.

```
$ ls -la
total 20
drwxr-xr-x 1 root   root   4096 Mar  2  2022 .
drwxr-xr-x 1 root   root   4096 Mar  2  2022 ..
drwxr-xr-x 1 ubuntu ubuntu 4096 Oct 13 16:16 ubuntu
drwxr-xr-x 2 root   root   4096 Mar  2  2022 user
```

At first I thought we wouldn't be able to access the root directory as we were logged in as an 'ubuntu' user, but the permissions *drwxr-xr-x* indicate that the directory is owned by the 'root* user, but it has read and execute permissions for others. This means that any user, including us, can traverse the directory and list its content, but cannot modify or delete anything inside it.

- d indicates it's a directory.
- rwx means the owner (root) has read, write, and execute permissions.
- r-x means the group (root) has read and execute permissions, but not write permissions.
- r-x means others have read and execute permissions as well.

<img width="449" height="193" alt="Bildschirmfoto vom 2025-10-13 18-23-04" src="https://github.com/user-attachments/assets/334fd04f-2dd6-4144-a9c7-1f0e67525225" />

And we are done. It's an interesting task, but if you already know the right commands for nmap, you might not even be in need of using the netcat listener. It's still good practice to get acquainted with strategies like this and I hope we get other opportunities to make use of netcat again.
