<h1 align="center">Challenge 020 - Crack the hash </h1>

<p align="center">
  <img width="89" height="90" alt="Bildschirmfoto vom 2025-09-11 09-24-12" src="https://github.com/user-attachments/assets/668ad2d3-3d8d-42af-b4eb-ba7c0fb371b1" />
</p>

<p align="center"> Difficulty: Completed:</p>

## Level 1

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

## Level 2

Level 2 is where the difficulty is supposed to get higher. We probably will have to use tools like hashcat now. Not for the first Hash though, which is the following.

```
F09EDCB1FCEFC6DFB23DC3505A882655FF77375ED8AA2D1C13F640FCCC2D0C85
```

After using CrackStation this was fairly easy to solve

<img width="1841" height="529" alt="Bildschirmfoto vom 2025-11-03 18-27-43" src="https://github.com/user-attachments/assets/b9ad7f70-6789-4276-b5c4-c8daa66d025d" />

And we can move on.

Hash number 2 is:

```
1DFECA0C002AE40B8619ECF94819CC1B
```

Same procedure as before

<img width="1841" height="529" alt="Bildschirmfoto vom 2025-11-03 18-29-10" src="https://github.com/user-attachments/assets/63bfef04-658b-45a0-ae28-cb39b29ff84e" />

Alright, NOW the difficulty spike is going up though, as I can see that we are also handed a salt with the hash now. A salt is a random value added to a password before hashing to ensure that identical passwords produce different hash values. By including a unique salt for each password, it increases security, making it more difficult for attackers to use precomputed hashes to guess passwords. The one we are dealing with now is this

```
Hash: $6$aReallyHardSalt$6WKUTqzq.UQQmrm0p/T7MPpMbGNnzXPMAXi4bJMl9be.cfi3/qxIf.hsGpS41BqMhSrHVXgMpdjS6xeKZAs02.

Salt: aReallyHardSalt
```

At least we know pretty quickly what type of hash this is due to the format. The hash starts with *$6$*, which denotes that it is using the SHA-512 algorithm. In this specific context, the presence of the salt (aReallyHardSalt) following the algorithm identifier and before the actual hash value confirms that it is a salted hash. I tried 

```
root@ip-10-10-224-21:~# hashcat -m 1800 -o output.txt hash.txt /usr/share/wordlists/rockyou.txt
```

The -m 1800 specifies the hash type for SHA-512 in hashcat, but it was painfully slow. Too slow. There had to be a way to shorten the process and indeed if we consider that the answer will have 6 letters the possibility of filtering the rockyou.txt file to extract all words with only 6 letters using the grep command in the terminal seemed very smart. I initiated the following command:

```
grep -E '^.{6}$' /usr/share/wordlists/rockyou.txt > six_letter_words.txt
```

The -E parameter in the grep command is used to enable extended regular expressions, allowing for more complex pattern matching. In this context, '^.{6}$' is a regular expression that matches lines with exactly 6 characters. Here's the breakdown:

- **^** asserts the start of the line.
- **.** matches any character.
- **{6}** specfies that the preceeding element (any character) must occur exactly 6 times.
- **$** asserts the end of a line. So, the whole expression checks for lines that are exactly 6 characters long, helping to filter words of that length from *rockyou.txt*

Now we made hashcat run again.

```
root@ip-10-10-224-21:~# hashcat -m 1800 -o output.txt hash.txt /usr/share/wordlists/six_letter_words.txt
hashcat (v6.1.1-66-g6a419d06) starting...

* Device #2: Outdated POCL OpenCL driver detected!

This OpenCL driver has been marked as likely to fail kernel compilation or to produce false negatives.
You can use --force to override this, but do not report related errors.

OpenCL API (OpenCL 1.2 LINUX) - Platform #1 [Intel(R) Corporation]
==================================================================
* Device #1: AMD EPYC 7571, 3800/3864 MB (966 MB allocatable), 2MCU

OpenCL API (OpenCL 1.2 pocl 1.4, None+Asserts, LLVM 9.0.1, RELOC, SLEEF, DISTRO, POCL_DEBUG) - Platform #2 [The pocl project]
=============================================================================================================================
* Device #2: pthread-AMD EPYC 7571, skipped

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Applicable optimizers applied:
* Zero-Byte
* Single-Hash
* Single-Salt
* Uses-64-Bit

ATTENTION! Pure (unoptimized) backend kernels selected.
Using pure kernels enables cracking longer passwords but for the price of drastically reduced performance.
If you want to switch to optimized backend kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Hardware monitoring interface not found on your system.
Watchdog: Temperature abort trigger disabled.

Host memory required for this attack: 0 MB

Dictionary cache built:
* Filename..: /usr/share/wordlists/six_letter_words.txt
* Passwords.: 1949232
* Bytes.....: 13653415
* Keyspace..: 1949232
* Runtime...: 0 secs

[s]tatus [p]ause [b]ypass [c]heckpoint [q]uit => s

Session..........: hashcat
Status...........: Running
Hash.Name........: sha512crypt $6$, SHA512 (Unix)
Hash.Target......: $6$aReallyHardSalt$6WKUTqzq.UQQmrm0p/T7MPpMbGNnzXPM...ZAs02.
Time.Started.....: Mon Nov  3 18:17:04 2025 (12 secs)
Time.Estimated...: Mon Nov  3 19:59:28 2025 (1 hour, 42 mins)
Guess.Base.......: File (/usr/share/wordlists/six_letter_words.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:      317 H/s (9.68ms) @ Accel:32 Loops:256 Thr:1 Vec:4
Recovered........: 0/1 (0.00%) Digests
Progress.........: 3840/1949232 (0.20%)
Rejected.........: 0/3840 (0.00%)
Restore.Point....: 3840/1949232 (0.20%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:1280-1536
Candidates.#1....: blue15 -> tillie

[s]tatus [p]ause [b]ypass [c]heckpoint [q]uit => 
```
It improved perfomance a little bit. It was enough to crack the hash, but I would think that getting to that idea probably covered as much time as it would have taken for hashcat to crack the hash manually. Truly painful.
