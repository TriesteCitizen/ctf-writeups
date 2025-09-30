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
- TryHackMe/Gallery/README.md) ✔️ (multiple attack vectors here, so worth another try)

## ⚔️ Attack Vectors
- Reverse-Engineering
  1. check permissions (change them with chmod 777/chmod +x if not executable)
  2. run application
  3. strings
  4. ltrace
  5. Ghidra (Decompiler)
  6. check for hexadecimal value and if we can convert to ascii or decimal
- IT-Forensic
  1. Filter protocols (http.request.method=="GET", given protocol)
  2. Check TCP stream
  3. Look for interesting files (.exe, .zip, passwords etc.)
  4. If stream contains zip file --> save tcp stream as raw and unzip
- Check Page Source
- CyberChef
- Esoteric Programming Languages
- Wayback machine
- png (Check header information through hex dump)
- Security through obscurity (tools: binwalk / StegOnline)
- Spectography ( https://academo.org/demos/spectrum-analyzer/ )
- Steganography (steghide (with given password) and stegcracker) 
- Use decryption tools and Hash Analyzers (ROT, Vigenère Cipher, md5/4)
- SQL Injection
- Network Inspection
- Brute Forcing (with tools like hydra (e.g. Agent Sudo)
- curl (-A to specify User-Agent. -L to follow any redirects)
- Command Injection (modify payload according to given program/check for environment variables)
- (PHP/Bash) Reverse Shells ( https://www.invicti.com/learn/reverse-shell/ )
- Enumeration (with hidden directories)
In Shell:
- if www-data user: Check configuration files in /var/www/html or other useful phps that get mentioned in the configuration file that could have sql credentials
  1. mysql -u <username> -p
  2. SHOW DATABASES; | USE <DATABASE>; | SHOW TABLES; | SELECT * FROM <TABLE>; etc.
- boot to root
  1. SUID binaries
  2. sudo -l (list of all commands the user can run as sudo)
  3. sudoers file
  4. Enumeration (check for backup files in var (log_history)
  5. check loghistory (RCE through Docker)
  6. sudo
  7. cronjob vulnerability

## 📌 Final Remark
- The solutions are **self-acquired** and document **my approach**
- I only post solution of retired machines or publicly available challenges
- Some of these write-ups may be a little long winded and need to be cut down. As I am at my humble beginnings I tend to write down a lot of details to remember for the future. Hopefully this is a skill that will improve over time
- There may are write-ups that I will return to, because there are several attack vectors for specific challenges and I'm only showcasing one type of it. The more knowledge I will gather the more I will try to experiment with what I'm given.

<p align="center">
  <img width="232" height="238" alt="Bildschirmfoto vom 2025-09-25 12-21-11" src="https://github.com/user-attachments/assets/644db5df-efed-4473-9b2d-539758ff45a0" />
</p>
