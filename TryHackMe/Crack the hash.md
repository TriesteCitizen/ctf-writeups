<h1 align="center">Challenge 020 - Crack the hash </h1>

<p align="center">
  <img width="89" height="90" alt="Bildschirmfoto vom 2025-09-11 09-24-12" src="https://github.com/user-attachments/assets/668ad2d3-3d8d-42af-b4eb-ba7c0fb371b1" />
</p>

<p align="center"> Difficulty: Completed:</p>

The first hash we have to crack is
```
48bb6e862e54f2a795ffc4e541caed4d
```

As md5 uses as a 32-character hexadecimal string, where each character represents 4 bits it felt only right to try this decryption first.

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

While this process is guaranteed to give some results I quickly realized how long it would take for the tool to go over the whole list. Maybe if I would have different CPUs with higher core count, clock speed and better features this could have been feasible, but I may have to overthing my strategy. I realized pretty fast that 
