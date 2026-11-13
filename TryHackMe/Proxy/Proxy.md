<h1 align="center">Proxy </h1>

<p align="center">
  <img src="assets/proxy.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>:  ✔️ </p>

I thought it might be beneficial to work out Active Directory, since that is still kind of one of my weaknesses. In this challenge we have to exploit a careless service account and own the Domain Controller

Every request has to go through someone... but what if that someone is you? We have to route our way through an Active Directory environment, intercept what we shouldn't, and pull the strings from behind the proxy. Nothing gets through without our say.

Active Directory isn't supposed to run on port 80, so I did a quick nmap scan to figure out what kind of server we are dealing with

```
root@ip-10-112-91-53:~# nmap -sV -p- 10.112.162.116
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-11-13 13:44 UTC
Nmap scan report for ip-10-112-162-116.eu-central-1.compute.internal (10.112.162.116)
Host is up (0.00030s latency).
Not shown: 65516 filtered tcp ports (no-response)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2026-11-13 13:46:14Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: ctf.local0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: ctf.local0., Site: Default-First-Site-Name)
3269/tcp  open  tcpwrapped
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
7680/tcp  open  pando-pub?
9389/tcp  open  mc-nmf        .NET Message Framing
49668/tcp open  msrpc         Microsoft Windows RPC
49676/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49677/tcp open  msrpc         Microsoft Windows RPC
49678/tcp open  msrpc         Microsoft Windows RPC
49703/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 159.85 seconds
```
Apparently there is a command smbclient

