# Challenge 012 - Brooklyn Nine Nine

Difficulty: Easy (2/10)
Completed: ✔️ 24.08.2025

In this challenge we had to get acquainted with Stenography and work out Privilege Escalation in Linux. I worked in a bigger group to solve this task, which severely shortened the time we had to take to beat this challenge. 
To start with I entered the target IP Address 10.10.10.171, which led me to the website, which obviously is very Brooklyn Nine-Nine inspired. Everyone in my group can recommend the show. I felt out of the loop as I never really watched it. Sorry, I'm more of a The Office kind of guy.

<img width="1383" height="953" alt="brooklynnine" src="https://github.com/user-attachments/assets/85bb4382-19bb-4488-a5b7-07b9d363d542" />
 
The first thing we did was checking the Page Source, which immediately gave a clue as it mentioned Steganography in a HTML comment. 
I thought that maybe we would need to look for some hidden directory, which contains some secret assets, so I tried to bruteforce with ffuf and didn't find anything valuable. On hindsight, it was very obvious that we would just need to inspect the jpg from the website. As always I was thinking way too complicated. A friend in the group mentioned StegCracker (not Stack Cracker) as a Steganography brute-force utility so we downloaded and made use of it on the jpg. 
```
root@ip-10-10-109-187:~/Downloads# stegcracker brooklyn99.jpg
StegCracker 2.1.0 - (https://github.com/Paradoxis/StegCracker)
Copyright (c) 2025 - Luke Paris (Paradoxis)

StegCracker has been retired following the release of StegSeek, which 
will blast through the rockyou.txt wordlist within 1.9 second as opposed 
to StegCracker which takes ~5 hours.

StegSeek can be found at: https://github.com/RickdeJager/stegseek

No wordlist was specified, using default rockyou.txt wordlist.
Counting lines in wordlist..
Attacking file 'brooklyn99.jpg' with wordlist '/usr/share/wordlists/rockyou.txt'..
Successfully cracked file with password: admin
Tried 20458 passwords
Your file has been written to: brooklyn99.jpg.out
admin
```

After succesfully inspecting the file, we were able to get a hold of Holts password. Very good.

<img width="652" height="200" alt="brooklynnine2" src="https://github.com/user-attachments/assets/603d8d82-7d30-43ec-b289-0d6371e64725" />

Now the question would be were to input this password. The assumption was made that maybe through analyzing the network we could find some open port to connect to and write in the newly found password. We immediately used nmap and got what we wanted.

```
root@ip-10-10-109-187:~# nmap 10.10.10.171 22
Starting Nmap 7.80 ( https://nmap.org ) at 2025-08-24 21:49 BST
Stats: 0:00:03 elapsed; 0 hosts completed (1 up), 1 undergoing Ping Scan
Ping Scan Timing: About 99.99% done; ETC: 21:49 (0:00:00 remaining)
Nmap scan report for ip-10-10-10-171.eu-west-1.compute.internal (10.10.10.171)
Host is up (0.00014s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http
MAC Address: 02:07:8F:65:89:11 (Unknown)
```

My friends were especially happy about the fact that the ftp service was open and usable, which I was completely unfamiliar with. I ignored their celebration and instead tried to use ssh to conntect to our target machine, without much success. I was kindly reminded of the fact that maybe I needed to specify which kind of user I was trying to login as, which made a lot of sense. I quickly checked with the help flag which commands would be possible to use in such a situation and got my answer.

```
root@ip-10-10-109-187:~# ssh holt@10.10.10.171 
holt@10.10.10.171's password: 
Permission denied, please try again.
holt@10.10.10.171's password: 
Last login: Tue May 26 08:59:00 2020 from 10.10.10.18
holt@brookly_nine_nine:~$
```

We are in! After checking the directories I saw a user.txt file, which we immediately checked out with cat. We managed to receive the first flag that way. 
Now it was time to explore the directories some more and check what options we had.

<img width="725" height="683" alt="brooklynnine3" src="https://github.com/user-attachments/assets/1d031cc9-9cf4-4135-bb59-f6faf9439adf" />
 
We also tried to use some chmod commands in the hopes of maybe changing user priviliges around, but that was not doable.

```
holt@brookly_nine_nine:/$ chmod 777 root
chmod: changing permissions of 'root': Operation not permitted
holt@brookly_nine_nine:/$ sudo chmod 777 root
[sudo] password for holt: 
Sorry, user holt is not allowed to execute '/bin/chmod 777 root' as root on brookly_nine_nine.
```

We discussed if Horizontal escalation could maybe give us some other hints as to what to do exactly. As we changed to the other user accounts to check if there were other files that we could use to our advantage. In the directory of jack we saw a file named .sudo_as_admin_successful. We thought that maybe through copying the file to the home directory we could be able to get admin privileges. Because of that we used 
```
holt@brookly_nine_nine:/home/amy$ cp .sudo_as_admin_successful ~/
```
But that didn't seem to solve anything. At least I tried the cp command again and knew of a shortcut to use, when copying files into a home directory.
As we hit a dead end we just decided to use the sudo -l command to see if we receive a list of available sudo privileges and indeed the results were very interesting.

```
holt@brookly_nine_nine:/home$ sudo -l
Matching Defaults entries for holt on brookly_nine_nine:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User holt may run the following commands on brookly_nine_nine:
    (ALL) NOPASSWD: /bin/nano
```
So we would be  able to use sudo nano to check some files, which would usually need some root priviliges. We quickly brainstormed and thought about all the files we saw through discovering all the directories, to check if there maybe was a possibility to get a hold of some other information that we didn't know of yet. There was a file from jakes directory, but we really weren't able to decipher what the information in that file could have meant. 

<img width="738" height="496" alt="brooklynnine4" src="https://github.com/user-attachments/assets/9aeec571-abf3-4c90-bcd2-5110a1aca566" />

I still decided to do a screenshot as maybe in the future there could be something we overlooked when looking at that file. In the end there are multiple ways to gain root privileges. 
We took a break and just started chatting a bit until a friend of ours reminded us that maybe there was a way to use nano to change around the sudoers file in the /etc/ directory. Frankly I'm quite annoyed that I didn't think of that. It's one of the most basic strategies when talking about privilege escalation. I can only hope, that after this, I will not overlook this ever again.  When accessing the file with nano, we got the following output:
 
It was clear as day what we needed to do now. Change the permissions.
```
holt	ALL=(ALL:ALL) ALL
```
We saved (Ctrl+O) and confirmed (ENTER) the changes. Now we would finally be able to use every command with sudo. With that knowledge we switched users
```
sudo su root
```

<img width="726" height="278" alt="brooklynnine8" src="https://github.com/user-attachments/assets/572897be-a313-4662-8f7b-9dfd14191f7c" />

The root flag was ours. It felt great to get some first practical experiences in regards to Steganography and the escalation of root privileges. I'm a little unsatisfied by the fact that I needed to be guided a lot by my friends, but practice makes perfect and this certainly was a fairly good experience. Here is to hoping I can soon give some good hints about what to do in some CTFs that will follow.

## Easter Egg:
Another thing I really wanted to mention is this funny red herring (?) Maybe this is a wrong lead, but we could also just be overlooking something. In any case, after realizing that sudo nano could be used to open some files, the .bash_history file from jakes directory was inspected. It was filled with commands that user probably used in his session.
```
cd .ssh/
ls
chmod 600 id_rsa
ssh -i id_rsa holt@127.0.0.1
cat id_rsa
ssh -i id_rsa holt@127.0.0.1
ssh-copy-id holt@10.10.10.30
ssh holt@10.10.10.30
cd ..
chmod 700 ,ssh
chmod 700 .ssh
chmod go-w
chmod go-w .
cd .
cd ..
chmod 700 holt/
cd holt/
service ssh restart
chmod ../holt 755
chmod 755 ../holt
chmod 755 .ssh/
service ssh restart
su - holt
service ssh restart
su - holt
nano /etc/ssh/sshd_config
service ssh restart
nano /etc/ssh/ssh_config
service ssh restart
nano /etc/ssh/sshd_config
grep -ni Allow /etc/ssh/sshd_config
nano +77 /etc/ssh/sshd_config
service ssh restart
nano +77 /etc/ssh/sshd_config
service ssh restart
ls
su - holt
rm -rf /var/www/html/robots.txt
rm -rf /var/www/html/holt
ls
cd /var/www/gtml
cd /var/www/html
ls
cat index.html
nano index.html
nano holt_password.txt
ls
steghide embed -cf brooklyn99.jpg -ef brooklyn99.jpg
steghide embed -cf brooklyn99.jpg -ef holt_password.txt
rm -rf holt_password.txt
ls
apt-get install python3-pip
pip3 install stegcracker
stegcracker brooklyn99.jpg
ls
nano note.txt
ls
stegide embed -cf photo.jpg -ef note.txt
steghide embed -cf photo.jpg -ef note.txt
nano index.html
rm -rf note.txt
ls
stegide extract -sf photo.jpg
steghide extract -sf photo.jpg
cat note.txt
rm -rf note.txt
ls
nano note.txt
steghide embed -cf brooklyn99.jpg -ef note.txt
rm -rf note.txt
ls
exit
```

By analyzing the history we quickly saw that by the end of the file the steghide extract -sf command was called. A tool that is used to hide steganography. With extract we can tell steghide that we want to pull hidden data out. -sf means stegofile and is the carrier file that supposedly has secret stuff inside. This led us to the conclusion that we should maybe try to bruteforce the photo.jpg that lies inside the var/www/html. For that we had to use stegcracker again, but obviously this tool was only installed in our local machine, so we googled for a command which would make it possible for us to copy files between our local machine and a remote one over SSH. Apparently scp could be used for that. It stands for secure copy 
```
root@ip-10-10-6-241:~# scp holt@10.10.10.171:/var/www/html/photo.jpg ~
holt@10.10.10.171's password: 
photo.jpg                                     100%   30KB  22.4MB/s   00:00   
```
We really thought we were slick when doing this. Instead we were in for a rude awakening after we were already laughinng about the fact that there was no password for the file.
```
root@ip-10-10-6-241:~# steghide extract -sf photo.jpg
Enter passphrase: 
wrote extracted data to "note.txt".

root@ip-10-10-6-241:~# cat note.txt
----------- StillNoob was here ------------------
```

Yup. This was very humbling. We definetely should not get too cocky, when doing these challenges as we are still at the very beginning of our journey, when it comes to Cybersecurity. 
Still, I enjoyed my time and am curious on what other ways exist to solve this challenge. Maybe I will return to this one after a bit more time to see what kind of progress I have made. For now I will put the AttackBox to rest though. 
