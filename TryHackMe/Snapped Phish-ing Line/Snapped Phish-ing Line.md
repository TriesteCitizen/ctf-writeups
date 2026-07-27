<h1 align="center">Snapped Phish-ing Line </h1>

<p align="center">
  <img src="assets/snapped.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️  </p>

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

