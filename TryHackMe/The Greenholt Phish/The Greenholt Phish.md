<h1 align="center">The Greenholt Phish </h1>

<p align="center">
  <img src="assets/thegreenholtphish.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 27.07.2026 </p>

A sales executive at Greenholt PLC has reported a suspicious email received from a known customer. The message raised several red flags: a generic greeting, an unexpected request for money transfer, and an unsolicited attachment. According to the employee, this behaviour does not align with the customer'S usual communication style. Concerned that the email may be malicious, the message has been escalated to the SOC (Security Operations Center) for further investigation. Your goal is to analyze the provded email sample and determine whether it is legitimate or part of a phishing attempt.

## What is the Transfer Reference Number listed in the email's Subject line?
By opening the mail and looking at the subject line we get the answer.

<img width="858" height="182" alt="grafik" src="https://github.com/user-attachments/assets/d78b3fc6-9f6f-4244-9cc3-e8cb095650b5" />

## What is the display name of the sender?
This can also be seen in the upper screenshot in the upper left side of the mail.

## Continue investigating the email headers. What is the sender's email address?
Yet again another information seen in the screenshot. The email address can be found under the display name of the sender.

## What email address will receive a reply to this email?
The "Reply to" segment of the screenshot reveals the answer.

## Begin analyzing the message source.

<img width="859" height="295" alt="grafik" src="https://github.com/user-attachments/assets/d09cd903-5bf3-4347-a284-c343ae4112ad" />

## What is the originating IP address of this email?

<img width="641" height="502" alt="grafik" src="https://github.com/user-attachments/assets/5c5292ec-d7c0-4566-a117-8f986befa06c" />

Looking at the "Received" section.

## Investigate the IP address from the previous question. Who is the owner of the originating IP?
I was looking for information in the message source, but was later advised to use IP lookup tools on the internet. We use the IP address from the prior answer.

<img width="877" height="736" alt="grafik" src="https://github.com/user-attachments/assets/149e1374-9eb0-43d1-90c8-a8c5d51e1ce3" />

## Run an SPF record check on the Return-Path domain identified in the email headers. What is the full SPF record for this domain?

From the Message header we identify the Return-Path: info@mutawamarine.com. To check the SPF record for the domain, we can use the following command.

`dig +short TXT mutawamarine.com`

```
ubuntu@tryhackme:~$ dig +short TXT mutawamarine.com
"v=spf1 include:spf.protection.outlook.com -all"
"MS=842BCB91F2AB2807BE05D25DC690D1226B349676"
"MS=ms97822417"
```

This will retrieve the TXT records for the domain, including the SPF record if it exists.

## Perform a DMARC lookup for the Return-Path domain found in the email headers. What is the complete DMARC record for this domain?
To perform a DMARC lookup we need to query the DMARC record for the domain mutawamarine.com, which can be done with the command

`dig +short TXT _dmarc.mutawamarine.com`

```
ubuntu@tryhackme:~$ dig +short TXT _dmarc.mutawamarine.com
"v=DMARC1; p=quarantine; fo=1"
```

## What is the file name of the attachment found in the email?
We move on and save the attachment in our sandbox

<img width="442" height="181" alt="grafik" src="https://github.com/user-attachments/assets/e6f305ab-669f-4870-83a8-cad017cb498f" />

That way we also figure out the name.

## Download the attachment to your virtual environment. Using the sha256sum command, what is the SHA256 hash of the file?
```
ubuntu@tryhackme:~$ sha256sum SWT_#09674321____PDF__.CAB
2e91c533615a9bb8929ac4bb76707b2444597ce063d84a4b33525e25074fff3f  SWT_#09674321____PDF__.CAB
```

## Investigate the file hash from the previous question using VirusTotal. What is the attachment's file size in KB (e.g. 122.31 KB)?

<img width="1787" height="282" alt="grafik" src="https://github.com/user-attachments/assets/ff73e321-67b9-437c-a880-7fb1a2962a9d" />

Look at the file size on the right. It's displayed right there.

## Continue your research on the file. What is the actual file type of the attachment?
Under Details we can figure out the actual file type under Basic properties.

<img width="1735" height="398" alt="grafik" src="https://github.com/user-attachments/assets/68e8787b-37cb-43ae-9b1a-082f4d880c74" />

It's a rar file.

### Lesson Learned
The active analyzation of Mail headers, VirusTotal, IP Address Lookups and Mail certifications like SPF and DMARC.

