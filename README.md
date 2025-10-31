# 🛡️ ctf-writeups

Welcome to my personal CTF archive. This is where I will document my progress in regards to platforms like TryHackMe and HackTheBox. This is purely for educational purposes and to enforce my learnings.

---

## ⭐ Content
- (TryHackMe/Brookyln Nine-Nine/README.md) ✔️
- (TryHackMe/Neighbor/README.md)
- (TryHackMe/Pickle Rick/README.md) ✔️
- (TryHackMe/RootMe/README.md) ✔️ (might have to edit this)
- (TryHackMe/TakeOver/README.md) ✔️ (might have to edit this)
- (TryHackMe/Evil-GPT v2/README.md) ✔️ (return at a later rate for other attack vector)
- (TryHackMe/Order/README.md) ✔️ (return to construct a Python script for it)
- (TryHackMe/Jax sucks alot............./README.md) ❎ (still need to beat this)
- (TryHackMe/Fowsniff CTF/README.md) ✔️ (Figure out Metasploit)
- (TryHackMe/Crack The Hash/README.md) ❎ (Not finished due to poor performance of CPU, which makes the running of rockyou.txt close to impossible. Will finish once I have found a workaround to this)
- (TryHackMe/Couch/README.md) ✔️
- (TryHackMe/Epoch/README.md) ✔️
- (TryHackMe/Easy Peasy/README.md) ✔️ (add python script for ROT13 if necessary)
- (TryHackMe/c4ptur3-th3-fl4g/README.md) ✔️
- (TryHackMe/Agent sudo/README.md) ❎ (Not finished due to no proper configuration of binwalk in VM. Will return to it once I have set up my own VM with Kali Linux)
- (TryHackMe/Stolen Mount/README.md) ✔️ (maybe return at a later date, to try other ways to retrieve the files of the TCP stream)
- (TryHackMe/CTF collection Vol.1/README.md) ✔️
- (TryHackMe/Reversing ELF/README.md) ✔️ (sure... maybe I return to see how good I can read Assembly)
- (TryHackMe/Gallery/README.md) ✔️ (multiple attack vectors here, so worth another try)
- (TryHackMe/SakuraRoom/README.md) ❎ (deprecated sites that make the finding of the BSSID and deep paste impossible (or at least difficult. I also never used Tor)
- (TryHackMe/Anthem/READMe.md) ✔️ (Try the last few tasks with Power Shell)
- (TryHackMe/Archangel/README.md) ❎ (still on going. Need to look up Log Poisoning first, as I never did that)
- (TryHackMe/Lo-Fi/README.md) ✔️
- (TryHackMe/Surfer/README.md) ✔️
- (TryHackMe/Res/README.md) ❎ (still on going. Need to research how to set up the right script for a web shell, which shouldn't be difficult)
- (TryHackMe/Agent T/README.md) ✔️
- (TryHackMe/Simple CTF/README.md) ✔️ (get back to it, to abuse the CVE-2019-9053 exploit instead of anonymously logging into the FTP port)
- (TryHackMe/Cat Pictures/README.md) ❎ (look up Port Knocking to move on here)
- (TryHackMe/Scripting/README.md) ❎ (Finished only one of the three tasks. Need to figure out how to print the whole response body first before trying to extract the given port on which we read the operations)
- (TryHackMe/Dig Dug/README.md) ✔️
- (TryHackMe/Memory Forensics/README.md) ❎ (Wrong configuration of Volatility. Before that isn't set up right, I can't do any proper memory forensics.)
- (TryHackMe/Intermediate Nmap/README.md) ✔️
- (TryHackMe/Shadow Trace/README.md) ✔️
- (TryHackMe/Summit/README.md) ✔️
- (TryHackMe/Friday Overtime/README.md) ✔️
- (TryHackMe/CyberHeroes/README.md) ✔️
- (TryHackMe/Brute It/README.md) ❎ (My file was deleted and never recovered after my laptop crashed and I'm too lazy to repeat that process. If some time passed I will take care of this)

## ⚔️ Attack Vectors
- Reverse-Engineering
  1. check permissions (change them with chmod 777/chmod +x if not executable)
  2. run application
  3. strings
  4. ltrace
  5. Ghidra (Decompiler)
  6. check for hexadecimal value and if we can convert to ascii or decimal
- Blue Teaming 🔵
  - Pyramid of Pain (1. Hash values | 2. IP-Addresses | 3. Domain Names | 4. Network/Host Artifacts | 5. Tools | 6. TTPs
- IT-Forensic
  1. Filter protocols (http.request.method=="GET", given protocol)
  2. Check TCP stream
  3. Look for interesting files (.exe, .zip, passwords etc.)
  4. If stream contains zip file --> save tcp stream as raw and unzip
  5. Volatility tool if we need to handle dmp/vmem files (look up Cheat sheet)
  6. VirusTotal
  7. Check hashsum of specific sha1sum file.txt
  8. Look for reports on specific libraries 
  
- Check Page Source
  1. for client-side written JavaScript code that should be written on the server side and can be exploited (Authentification Bypass)
  2. for hidden messages
- Scripting
  1. See source code examples for different scenarios (Scripting.md)
- OSINT (Open Source Intelligence)
  1. Inspect picture
  2. Wayback machine
  3. check social media sites / alternative usernames
  4. check commits
- Gain access to a Windows machine through Linux -> rdesktop IP-ADDRESS
  1. View < Hidden Items
  2. Change Permissions: Right Click < Properties < Security < Edit < "everyone" < OK < Apply
  3. Power Shell 
- Esoteric Programming Languages
- png (Check header information through hex dump)
- Security through obscurity (tools: binwalk / StegOnline)
- Spectography ( https://academo.org/demos/spectrum-analyzer/ )
- Steganography (steghide (with given password) and stegcracker) 
- Use decryption tools and Hash Analyzers (ROT, Vigenère Cipher, md5/4)
- SQL Injection
- Network Inspection
- Web Shells (malicious script that can be uploaded to a web server)
- Brute Forcing (with tools like hydra into FTP or SSH (e.g. Agent Sudo))
- Port Knocking when ports are given
- DNS enumeration with dig or nslookup
  1. For mail server checking: dig givemetheflag.com MX
  2. For text record checking: dig givemetheflag.com TXT
  3. For general information about a domain: dig dig @10.10.240.191 givemetheflag.com
- nmap -p- -sV -A
  1. Check version of software by browsing too. Can it be exploited? https://www.exploit-db.com/ 
- curl (-A to specify User-Agent. -L to follow any redirects)
- Command Injection (modify payload according to given program/check for environment variables)
- (PHP/Bash) Reverse Shells ( https://www.invicti.com/learn/reverse-shell/ )
- Enumeration (with hidden directories)
- robots.txt
- SSRF (Server-Side Request Forgery)
  1. Check for any hidden server, where crafted requests from a vulnerable server to internal or external resources can be done using Burp Suite (url parameter can maybe be modified) 
- Does the webserver host multiple websites?
  1. If yes -> add that domain name to the etc/hosts file with the IP-Address
- LFI (Local File Inclusion) https://www.hackthebox.com/files/cheatsheet-file-inclusion.pdf
  1. PHP Wrappers (e.g. http://mafialive.thm/test.php?view=php://filter/read=convert.base64-encode/resource=/var/www/html/development_testing/test.php) -> then analyze source code
- In Shell:
  1.if www-data user: Check configuration files in /var/www/html or other useful phps that get mentioned in the configuration file that could have sql credentials
  2. mysql -u <username> -p
  3. SHOW DATABASES; | USE <DATABASE>; | SHOW TABLES; | SELECT * FROM <TABLE>; etc.
- boot to root
  1. SUID binaries
  2. sudo -l (list of all commands the user can run as sudo)
  3. sudoers file
  4. Enumeration (check for backup files in var (log_history)
  5. check loghistory (RCE through Docker)
  6. sudo
  7. cronjob vulnerability
  8. always check the permissions. We might still be able to access or read specific directories and files
- CyberChef
- GTFOBins

## 📌 Final Remark
- The solutions are **self-acquired** and document **my approach**
- I only post solution of retired machines or publicly available challenges
- Some of these write-ups may be a little long winded and need to be cut down. As I am at my humble beginnings I tend to write down a lot of details to remember for the future. Hopefully this is a skill that will improve over time
- There may are write-ups that I will return to, because there are several attack vectors for specific challenges and I'm only showcasing one type of it. The more knowledge I will gather the more I will try to experiment with what I'm given.

<p align="center">
  <img width="238" height="214" alt="Bildschirmfoto vom 2025-10-01 22-06-31" src="https://github.com/user-attachments/assets/348da3d7-d3bb-4191-9e2e-b923273f31a8" />
</p>
