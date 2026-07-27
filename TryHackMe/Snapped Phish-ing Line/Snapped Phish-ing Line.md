<h1 align="center">Snapped Phish-ing Line </h1>

<p align="center">
  <img src="assets/snapped.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: 2/10 (Easy) <b>Completed</b>: ✔️ 27.07.2026 </p>

As a member of the IT department at SwiftSpend Financial, you are responsible for assisting employees with technical concerns. What initally appeared to be a routine day quickly escalated when multiple employees across different departments reported receiving a suspicious email. Several users noted unusual characteristics in the message, and unfortunately some had already submitted their credentials and were no longer able to access their accounts. With the potential for a wider compromise, the incident has been escalated for investigation. Our task is to analyze the available evidence, determine the scope of the attack, and uncover how the adversary operated.

## Begin reviewing the emails in the `phish-emails` folder on your desktop. Which individual received the email regarding a Quote for Services Rendered?
Once entering the phish-emails folder on the desktop we can easily deduce which mail is referring to rendered services.

<img width="877" height="264" alt="grafik" src="https://github.com/user-attachments/assets/14ee1902-90d8-4799-8b4e-9ebc93890d14" />

When opening the mail we are faced with a lot of useful information, like the recipient of this mail.

<img width="1018" height="761" alt="grafik" src="https://github.com/user-attachments/assets/dcd6c7a3-fb78-442c-a1db-8d0343a99eb9" />

## What email address was used by the adversary to send the phishing emails?
Also seen when checking the From segment.

## Investigate the attachment in the email addressed to Zoe Duncan. What is the root domain of the redirection URL found within the file?
First we download the attachment to then inspect its content and the embedded button.

<img width="871" height="793" alt="grafik" src="https://github.com/user-attachments/assets/56b12fd7-e7ee-460f-b598-15b87d6bf53c" />

Hovering over the button quickly reveals the root domain.

## Open the attachment in your VM web browser. Which company is the login page impersonating?
By the upper screenshot we can already deduce that the subscription service Office365 is being impersonated. It's made by Microsoft.

## Let's check if the attacker left any files exposed on the same website. Navigate to the `/data` directory. What is the name of the archive file?
Since normal browsing didn't work I just pivoted to using wget and downloading files from the web, in this case index.html to figure out the archive file.
```
damianhall@ip-10-112-182-75:~$ wget http://kennaroads.buzz/data/
--2026-07-27 23:50:48--  http://kennaroads.buzz/data/
Resolving kennaroads.buzz (kennaroads.buzz)... 172.67.216.206
Connecting to kennaroads.buzz (kennaroads.buzz)|172.67.216.206|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1150 (1.1K) [text/html]
Saving to: ‘index.html’

index.html          100%[===================>]   1.12K  --.-KB/s    in 0s      

2026-07-27 23:50:48 (127 MB/s) - ‘index.html’ saved [1150/1150]
```

Let's analyze the html file

```
damianhall@ip-10-112-182-75:~$ cat index.html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /data</title>
 </head>
 <body>
<h1>Index of /data</h1>
  <table>
   <tr><th valign="top"><img src="/icons/blank.gif" alt="[ICO]"></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr>
   <tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="/icons/back.gif" alt="[PARENTDIR]"></td><td><a href="/">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/compressed.gif" alt="[   ]"></td><td><a href="Update365.zip">Update365.zip</a></td><td align="right">2023-04-16 14:19  </td><td align="right">394K</td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/folder.gif" alt="[DIR]"></td><td><a href="Update365/">Update365/</a></td><td align="right">2023-05-03 15:56  </td><td align="right">  - </td><td>&nbsp;</td></tr>
   <tr><th colspan="5"><hr></th></tr>
</table>
<address>Apache/2.4.56 (Debian) Server at kennaroads.buzz Port 80</address>
</body></html>
```

The html seems to provide a file named Update365.zip. 

## Download the phishing kit archive to your virtual environment. Using the sha256sum command, what is the SHA256 hash of the file?
Since I still can't browse the domain I opted on using wget once again to download the file.

```
damianhall@ip-10-112-182-75:~$ wget http://kennaroads.buzz/data/Update365.zip
--2026-07-27 23:56:00--  http://kennaroads.buzz/data/Update365.zip
Resolving kennaroads.buzz (kennaroads.buzz)... 172.67.216.206
Connecting to kennaroads.buzz (kennaroads.buzz)|172.67.216.206|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 402999 (394K) [application/zip]
Saving to: ‘Update365.zip’

Update365.zip       100%[===================>] 393.55K  --.-KB/s    in 0.003s  

2026-07-27 23:56:00 (132 MB/s) - ‘Update365.zip’ saved [402999/402999]
```

Now we can figure out the SHA256 hash of the file.

```
damianhall@ip-10-112-182-75:~$ sha256sum Update365.zip
ba3c15267393419eb08c7b2652b8b6b39b406ef300ae8a18fee4d16b19ac9686  Update365.zip
```

## Investigate the file hash from the previous question using VirusTotal. Aside from phishing, what other threat category is assigned to the ZIP archive?
Pasting the hash into VirusTotal we get the following results.

<img width="1789" height="469" alt="grafik" src="https://github.com/user-attachments/assets/d009a2f4-982d-493e-9cdc-6165c59720f0" />

Trojan and hacktool are the other threat categories as it seems.

## Review the VirusTotal Details page for the phishing kit. How many files are contained within the archive?
We click on the Details of our hash.

<img width="1789" height="399" alt="grafik" src="https://github.com/user-attachments/assets/2ce7c404-654b-4ddb-ad9f-c502ed5724d7" />

49 contained files are listed.

## Let’s see if the attacker has exposed any captured credentials. Navigate to the `/data/Update365/` directory and investigate the log file. What is the email address of the user who submitted their credentials more than once?
Wget usage once again.

```
damianhall@ip-10-112-182-75:~$ wget http://kennaroads.buzz/data/Update365/
--2026-07-28 00:06:32--  http://kennaroads.buzz/data/Update365/
Resolving kennaroads.buzz (kennaroads.buzz)... 172.67.216.206
Connecting to kennaroads.buzz (kennaroads.buzz)|172.67.216.206|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1157 (1.1K) [text/html]
Saving to: ‘index.html.1’

index.html.1        100%[===================>]   1.13K  --.-KB/s    in 0s      

2026-07-28 00:06:32 (80.5 MB/s) - ‘index.html.1’ saved [1157/1157]
```

After downloading the html and clicking on the file we can see the log file that was mentioned in the task.

<img width="583" height="279" alt="grafik" src="https://github.com/user-attachments/assets/f53f9fb8-0379-499b-8811-5c2403db9150" />

Unfortunately we are not able to access the log.txt file by clicking on it. We have to use wget again.

```
damianhall@ip-10-112-182-75:~$ wget http://kennaroads.buzz/data/Update365/log.txt
--2026-07-28 00:21:13--  http://kennaroads.buzz/data/Update365/log.txt
Resolving kennaroads.buzz (kennaroads.buzz)... 172.67.216.206
Connecting to kennaroads.buzz (kennaroads.buzz)|172.67.216.206|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2530 (2.5K) [text/plain]
Saving to: ‘log.txt’

log.txt             100%[===================>]   2.47K  --.-KB/s    in 0s      

2026-07-28 00:21:13 (45.9 MB/s) - ‘log.txt’ saved [2530/2530]
```

This log text file contains sensitive information related to Office365 logins. It indicates potential phishing activity and captures user credentials along with their geographic information, IP addresses, and user agents used during login attempts.

```
---------+ Office365 Login  |+-------
Email : isaiah.puzon@gmail.com
Password : PhishMOMUKAMO123!
-----------------------------------
Client IP: 158.62.17.197
User Agent : Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0
Country : Philippines
Date: Mon Jun 29, 2020 10:00 am
--- http://www.geoiptool.com/?IP=158.62.17.197 ----
--+ Created BY Real Carder +---
---------+ Office365 Login  |+-------
Email : michael.ascot@swiftspend.finance
Password : Invoice2023!
-----------------------------------
Client IP: 64.62.197.80
User Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Country : United States
Date: Mon Jun 29, 2020 10:01 am
--- http://www.geoiptool.com/?IP=64.62.197.80 ----
--+ Created BY Real Carder +---
---------+ Office365 Login  |+-------
Email : zoe.duncan@swiftspend.finance
Password : Passw0rd1!
-----------------------------------
Client IP: 64.62.197.80
User Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Country : United States
Date: Mon Jun 29, 2020 10:01 am
--- http://www.geoiptool.com/?IP=64.62.197.80 ----
--+ Created BY Real Carder +---
---------+ Office365 Login  |+-------
Email : michael.ascot@swiftspend.finance
Password : Invoice2023!
-----------------------------------
Client IP: 64.62.197.80
User Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Country : United States
Date: Mon Jun 29, 2020 10:01 am
--- http://www.geoiptool.com/?IP=64.62.197.80 ----
--+ Created BY Real Carder +---
---------+ Office365 Login  |+-------
Email : derick.marshall@swiftspend.finance
Password : lol
-----------------------------------
Client IP: 64.62.197.80
User Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Country : United States
Date: Mon Jun 29, 2020 10:01 am
--- http://www.geoiptool.com/?IP=64.62.197.80 ----
--+ Created BY Real Carder +---
---------+ Office365 Login  |+-------
Email : michelle.chen@swiftspend.finance
Password : testing123
-----------------------------------
Client IP: 64.62.197.80
User Agent : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Country : United States
Date: Mon Jun 29, 2020 10:01 am
--- http://www.geoiptool.com/?IP=64.62.197.80 ----
--+ Created BY Real Carder +---
```

The email address of the user who submitted their credentials more than once was michael.ascot@swiftspend.finance.

## Extract the phishing kit archive and locate the `submit.php` file. What email address is used by the adversary to collect compromised credentials?
First we extract the phishing kit archive using the command `unzip Update365.zip`

```
damianhall@ip-10-112-182-75:~$ unzip Update365.zip
Archive:  Update365.zip
   creating: Update365/office365/
  inflating: Update365/office365/.DS_Store  
  inflating: Update365/office365/blocker.php  
  inflating: Update365/office365/delete.php  
  inflating: Update365/office365/error_log  
  inflating: Update365/office365/index.php  
  inflating: Update365/office365/robots.txt  
   creating: Update365/office365/scr/
  inflating: Update365/office365/script.st  
   creating: Update365/office365/Scriptup/
  inflating: Update365/office365/Scriptup/marvid  
  inflating: Update365/office365/Scriptup/newscr.pt  
  inflating: Update365/office365/Scriptup/pagescir  
  inflating: Update365/office365/Scriptup/script.st  
  inflating: Update365/office365/Scriptup/updat.cmd  
  inflating: Update365/office365/Scriptup/update  
  inflating: Update365/office365/updat.cmd  
   creating: Update365/office365/update/
  inflating: Update365/office365/update/cleanup  
  inflating: Update365/office365/update/pagesc.koo  
  inflating: Update365/office365/update/pagescir  
  inflating: Update365/office365/update/update  
  inflating: Update365/office365/update/viruscle.reg  
   creating: Update365/office365/Validation/
  inflating: Update365/office365/Validation/ay5mw92o3or77qgeyn118kxl.php  
  inflating: Update365/office365/Validation/enterpassword.php  
  inflating: Update365/office365/Validation/enterpasswordagain.php  
   creating: Update365/office365/Validation/images/
  inflating: Update365/office365/Validation/images/0.jpg  
 extracting: Update365/office365/Validation/images/arrow.png  
  inflating: Update365/office365/Validation/images/favicon.png  
  inflating: Update365/office365/Validation/images/ms-logo-v1.svg  
  inflating: Update365/office365/Validation/images/ms-logo-v2.jpg  
  inflating: Update365/office365/Validation/images/Office-365-Logo.png  
  inflating: Update365/office365/Validation/images/picker_account_msa.svg  
  inflating: Update365/office365/Validation/index.php  
   creating: Update365/office365/Validation/js/
  inflating: Update365/office365/Validation/js/jquery.js  
  inflating: Update365/office365/Validation/loader.gif  
  inflating: Update365/office365/Validation/redirecttoinbox.php  
  inflating: Update365/office365/Validation/resubmit.php  
  inflating: Update365/office365/Validation/retry.php  
  inflating: Update365/office365/Validation/robots.txt  
  inflating: Update365/office365/Validation/script.st  
  inflating: Update365/office365/Validation/security-assurance.php  
  inflating: Update365/office365/Validation/style.css  
  inflating: Update365/office365/Validation/submit.php  
  inflating: Update365/office365/Validation/updat.cmd  
  inflating: Update365/office365/Validation/update  
```

Now we locate the submit.php.

```
damianhall@ip-10-112-182-75:~$ find Update365 -name "submit.php"
Update365/office365/Validation/submit.php
```

After opening the file we look for the attackers email address, which is used to collect compromised credentials.

<img width="551" height="801" alt="grafik" src="https://github.com/user-attachments/assets/2cc10767-2fd0-4c71-aa8a-368e7ff63ebe" />

Line 112 clearly states the dedicated address.

## Return to the phishing URL and locate the `flag.txt` file. Using CyberChef (opens in new tab) to decode the flag, what is the secret value?
As I tried accessing the URL I was reminded by the fact that I couldn't access it. I tried to see where the URL was being redirected

```
damianhall@ip-10-112-182-75:~$ curl -I http://kennaroads.buzz/data/Update365/office365/
HTTP/1.1 302 Found
Server: nginx/1.23.4
Date: Mon, 27 Jul 2026 17:14:10 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
X-Powered-By: PHP/8.2.5
location: df519a29dbb585b013a9a64c48f205e7
```

The HTTP response indicates that the URL has been redirected (HTTP 302) to a new location specified by the `location` header. But even theat didn't lead to any interesting conclusions. Finally I just tested out what would happen if I would just check for a `flag.txt` file. Thankfully this seemed to have worked.

<img width="654" height="78" alt="grafik" src="https://github.com/user-attachments/assets/7d94f7b3-8b62-4e8c-a571-e0b95591a47c" />

Seems to be Base64 encoded. We put the input in CyberChef. After we reverse the output we finally get the solution.

<img width="875" height="561" alt="Bildschirmfoto vom 2026-07-27 19-31-16" src="https://github.com/user-attachments/assets/003f763f-5472-411d-8c47-bda65884878b" />

## Lesson Learned
A lot of directory enumeration, curl and wget can be of huge help, if we want to inspect unknown phoshing domains. At the same time sometimes we also need to inspect different url directories until something works out. There is no clear path on what direction is better to take in those situations. I want to return to this challenge at a later time to maybe figure out how to solve this tasks without using the linux commands.
