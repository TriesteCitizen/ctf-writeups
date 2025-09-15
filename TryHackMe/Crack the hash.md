<h1 align="center">Challenge 020 - Crack the hash </h1>

<p align="center">
  <img width="89" height="90" alt="Bildschirmfoto vom 2025-09-11 09-24-12" src="https://github.com/user-attachments/assets/668ad2d3-3d8d-42af-b4eb-ba7c0fb371b1" />
</p>

<p align="center"> Difficulty: Completed:</p>

The first hash we have to crack is
```
48bb6e862e54f2a795ffc4e541caed4d
```

As md5 uses a 32-character hexadecimal string, where each character represents 4 bits it felt only right to try this decryption first.

<img width="179" height="125" alt="image" src="https://github.com/user-attachments/assets/3d9a32cb-ae3a-4c82-bfbc-4d39070a090f" />


The second hash we move on to is
```
CBFDAC6008F9CAB4083784CBD1874F76618D2A97 
```

This hexadecimal hash has a fixed-length of 40 characters, which usually is a big hint for SHA-1. It would be 64 characters for SHA-256 and 128 characters for SHA-512. 
I used the 100L5 tool to decrypt

<img width="1021" height="221" alt="Bildschirmfoto vom 2025-09-11 17-38-25" src="https://github.com/user-attachments/assets/03848537-2178-4540-89d1-a1ca8bdd8601" />

The next hash had a hex length of 64 characters. 
```
1C8BFE8F801D79745C4631D09FFF36C82AA37FC4CCE4FC946683D7B336B63032
```

Time for the SHA-256 decryption

<img width="1021" height="221" alt="Bildschirmfoto vom 2025-09-11 17-47-15" src="https://github.com/user-attachments/assets/30d11cee-1c14-402a-b780-3bb79ff75b9f" />

It worked quite well and I swiftly moved on with the next hash, which looks like this

```
$2y$12$Dwt1BZj6pcyc3Dy1FWZ5ieeUznr71EeNkJkUlypTsgbX1H68wsRom
```

It's not a hexadecimal value and has a length of 60 characters, so I checked out hashes with these patterns. After a short research I found out that the BCrypt algorithm generates a string of such length. Another tool that is responsible for analyzing hashes confirmed it too

<img width="846" height="672" alt="image" src="https://github.com/user-attachments/assets/8f4da413-4393-4b35-927d-4748ebff0092" />

I tried looking for bcrypt decryption tools, which didn't lead to any valuable results. So I just decided to install that hashcat cracker onto my terminal, which is known to be the most popular password cracker.

<img width="526" height="41" alt="image" src="https://github.com/user-attachments/assets/053229be-25aa-4cbc-b89e-1d0ef61ec27e" />

First we saved the hash into a textfile, which we stored into a directory. The most popular textfile, which contains the most common passwords is rockyou.txt. So after downloading and putting it into a directory we could start using our hashcat tool. We run

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~$ hashcat -m 3200 Hash/hash.txt Dict/rockyou.txt
hashcat (v6.2.5) starting

OpenCL API (OpenCL 2.0 pocl 1.8  Linux, None+Asserts, RELOC, LLVM 11.1.0, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
=====================================================================================================================================
* Device #1: pthread-AMD Ryzen 3 5300U with Radeon Graphics, 2573/5211 MB (1024 MB allocatable), 8MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 72

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Single-Hash
* Single-Salt

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 0 MB

Dictionary cache built:
* Filename..: Dict/rockyou.txt
* Passwords.: 14344391
* Bytes.....: 139921497
* Keyspace..: 14344384
* Runtime...: 0 secs

Cracking performance lower than expected?                 

* Append -w 3 to the commandline.
  This can cause your screen to lag.

* Append -S to the commandline.
  This has a drastic speed impact but can be better for specific attacks.
  Typical scenarios are a small wordlist but a large ruleset.

* Update your backend API runtime / driver the right way:
  https://hashcat.net/faq/wrongdriver

* Create more work items to make use of your parallelization power:
  https://hashcat.net/faq/morework
```

While this process is guaranteed to give some results I quickly realized how long it would take for the tool to go over the whole list. Maybe if I would have different CPUs with higher core count, clock speed and better features this could have been feasible, but I may have to overthing my strategy. By checking the result that needs to come out I realized that the character length needs to be of 4, so I modified the command to specify a mask attack with 4 lowercase letters

```
hashcat -m 3200 -a 3 -o output.txt Hash/hash.txt ?l?l?l?l
```

The command specifies:
- -m 3200: The hash type for bcrypt
- -a 3: using a mask attack
- output.txt: where the cracked passwords will be saved
- hash.txt: the file containing your bcrypt hash
- ?l?l?l?l: a mask indicating that we want to try all combinations of 4 lowercase letters

Just as a future reminder. These are the ways we can adjust the mask accordingly:
- For lowercase and uppercase: ?u?l?l?l
- For lowercase and numbers: ?l?l?l?d
- For lowercase, uppercase, and numbers: ?u?l?d?d

This process took around 3 hours and will probably never be repeated by me again. Not with this CPU. 

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~$ hashcat -m 3200 -a 3 -o output.txt Hash/hash.txt  ?l?l?l?l
hashcat (v6.2.5) starting

OpenCL API (OpenCL 2.0 pocl 1.8  Linux, None+Asserts, RELOC, LLVM 11.1.0, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
=====================================================================================================================================
* Device #1: pthread-AMD Ryzen 3 5300U with Radeon Graphics, 2573/5211 MB (1024 MB allocatable), 8MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 72

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates

Optimizers applied:
* Zero-Byte
* Single-Hash
* Single-Salt
* Brute-Force

Watchdog: Temperature abort trigger set to 90c

Host memory required for this attack: 0 MB

Cracking performance lower than expected?                 

* Append -w 3 to the commandline.
  This can cause your screen to lag.

* Append -S to the commandline.
  This has a drastic speed impact but can be better for specific attacks.
  Typical scenarios are a small wordlist but a large ruleset.

* Update your backend API runtime / driver the right way:
  https://hashcat.net/faq/wrongdriver

* Create more work items to make use of your parallelization power:
  https://hashcat.net/faq/morework

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 3200 (bcrypt $2*$, Blowfish (Unix))
Hash.Target......: $2y$12$Dwt1BZj6pcyc3Dy1FWZ5ieeUznr71EeNkJkUlypTsgbX...8wsRom
Time.Started.....: Mon Sep 15 14:30:34 2025 (3 hours, 50 mins)
Time.Estimated...: Mon Sep 15 18:20:59 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Mask.......: ?l?l?l?l [4]
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:       29 H/s (2.02ms) @ Accel:8 Loops:32 Thr:1 Vec:1
Recovered........: 1/1 (100.00%) Digests
Progress.........: 405632/456976 (88.76%)
Rejected.........: 0/405632 (0.00%)
Restore.Point....: 15600/17576 (88.76%)
Restore.Sub.#1...: Salt:0 Amplifier:3-4 Iteration:4064-4096
Candidate.Engine.: Device Generator
Candidates.#1....: bamv -> bhii
Hardware.Mon.#1..: Temp: 77c Util: 87%

Started: Mon Sep 15 14:30:32 2025
Stopped: Mon Sep 15 18:21:01 2025
```

The output was saved in my text file.

<img width="644" height="85" alt="Bildschirmfoto vom 2025-09-15 18-29-42" src="https://github.com/user-attachments/assets/ed6cf8b1-cbc9-44bc-bbb0-d17e4dd3f305" />

I'll just use the AttackBox for all the following hashes.

The last hash of Level 1 was quite simple again.



```
279412f945939ba78ce0758d3fd83daa
```

This hash is 32 characters long, so I decided to check out the different md hashes.

<img width="166" height="112" alt="image" src="https://github.com/user-attachments/assets/98c53569-53e5-49e4-9cf9-5ce399bdf56e" />

Apparently it was an md4 hash, which concludes the Level 1 section of this challenge.
