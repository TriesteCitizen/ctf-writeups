<h1 align="center">Challenge 045 - Friday Overtime </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/a89be69e-3af7-4771-8610-01ec0ae80647" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 27.10.2025 </p>

This is another task which gives us an insight on how the daily activities of a Security Analyst looks like. 

The scenario is the following. It's a Friday evening at PandaProbe Intelligence when a notification appears on the CTI platform. While most are already looking forward to the weekend, we realise we must pull overtime because SwiftSpend Finance has opened a new ticket, raising concerns about potential malware threats. The finance company, known for its meticulous security measures, stumbled upon something suspicious and wanted immediate expert analysis.

As the only remaining CTI Analyst on shift at PandaProbe Intelligence, we quickly take charge of the sitation, realizing the gravity of a potential breach at a financial institution. The ticket contained multiple file attachments, presumed to be malware samples.

For the beginning we need to download the malware samples provided in the ticket, ensuring they were contained in a secure environment. First we login to the PandaProbe website and can see that we received an email

<img width="1156" height="488" alt="grafik" src="https://github.com/user-attachments/assets/f3131d70-c110-4d19-a23c-fa283c31ac66" />

The mail says the following

```
Urgent: Malicious Malware Artefacts Detected
by SwiftSpend Finance - Registered 2023-12-07T23:10:51.5503900

Dear PandaProbe Intel team,

I hope this message finds you well. My name is Oliver Bennett from the Cybersecurity Division at SwiftSpend Finance. During our recent security sweep, we have identified a set of malicious files which, based on our preliminary analysis, seem to be associated with .

Details

Date Detected: Friday, December 8, 2023

Infected Systems: Over 9000 systems

Nature of Malware: Unknown / Suspected RAT

We believe the intent of this malware is to gain a foothold to ultimately exfiltrate sensitive financial data and possibly deploy ransomware.

Immediate Actions Taken

- Isolated the infected systems from the network.

- Initiated a comprehensive scan across all systems.

- Collected and stored malware samples securely for further analysis.

- We are currently collaborating with external cybersecurity agencies and our security solutions providers to get a deeper understanding of this malware. However, we wanted to raise this with you immediately given the potential risk associated with APTs.

We strongly need your team's assistance with conducting a thorough review of the malware sample. The password to the attached archive is: Panda321!

Moving forward, we are going to conduct a User Awareness Training to inform all staff members to be extra cautious, especially when dealing with email attachments and links.

Attached are the indicators of compromise (IoCs) for your perusal. I am also available for a call or meeting to discuss our findings in detail and strategise our response.

Your prompt attention to this matter is highly appreciated. Let's work together to ensure the safety and integrity of our systems and data.

Warm regards,

Oliver Bennett

Cybersecurity Division

SwiftSpend Finance


Phone: +123 456 7890

Email: oliver.bennett@swiftspend.finance
```

The email also reveals the first question to us, which asks us who shared the malware sample? It was Oliver Bennett.

Now we look for the zip file and check out what the SHA1 hash of the "prSm.dll" file inside the samples.zip is.

```
[ericatracy@ip-10-10-189-185 ~]$ ls
Desktop  Downloads
[ericatracy@ip-10-10-189-185 ~]$ cd Downloads
[ericatracy@ip-10-10-189-185 Downloads]$ ls
samples.zip
[ericatracy@ip-10-10-189-185 Downloads]$ unzip samples.zip
Archive:  samples.zip
[samples.zip] cbmrpa.dll password: 
  inflating: cbmrpa.dll              
  inflating: maillfpassword.dll      
  inflating: pRsm.dll                
  inflating: qmsdp.dll               
  inflating: wcdbcrk.dll             
[ericatracy@ip-10-10-189-185 Downloads]$ ls
cbmrpa.dll  maillfpassword.dll  pRsm.dll  qmsdp.dll  samples.zip  wcdbcrk.dll
[ericatracy@ip-10-10-189-185 Downloads]$ sha1sum pRsm.dll
9d1ecbbe8637fed0d89fca1af35ea821277ad2e8  pRsm.dll
```

That same hash value can be reused to figure out which malware framework utilizes these DLLs as add-on modules. One website that gives us a clear idea of that is VirusTotal.

<img width="1850" height="472" alt="grafik" src="https://github.com/user-attachments/assets/8c30cbfd-8ca7-4acd-87f9-35a36fe088fb" />

Under the Family label we get a good idea which kind of labels are possible candidates.

While browsing the internet we are also able to access a website that gives us a thorough report on how the malware functions, its capabilities, which group was the mastermind of it and so on.

<img width="1850" height="962" alt="Bildschirmfoto vom 2025-10-24 17-34-41" src="https://github.com/user-attachments/assets/c825c3e2-8db8-412f-96e4-eba30e615b91" />

The report mentions how Evasive Panda - a chinese APT group - made use of cyber spionage. The group uses their own malware framework with a modular architecture, which enables their MgBot labelled backdoor to receive modules, with which they can spy on their victims and improve their skills.

This answers the question as to which malware framework utilizes the beforementioned DLLs as add-on modules. It's the MgBot.

When further scrolling down we also get a good idea on the kind of MITRE ATT&CK techniques that were utilized.

<img width="777" height="748" alt="grafik" src="https://github.com/user-attachments/assets/33760d58-19a5-4185-aed1-c16cf7438b68" />

One of the tactics found under the "Collection" label is the Audio Capture, which mentions how the MgBot's plugin module pRsm.dll is used to capture input and output audio streams. As the task was also asking us which Technique is linked to using pRsm.dll in this malware framework the answer of said ID seems only logical.

Now moving on we have to figure out the defanged URL of the malicious download location first seen on 2020-11-02? Luckily for us, there seems to be a section for technical analysis in the webpage that mentions this exact URL of said timeperiod.

<img width="772" height="387" alt="grafik" src="https://github.com/user-attachments/assets/acb63d7a-fd9e-4fdf-aec0-bde1b74a573a" />

This URL only needs to be defanged now, so there are no risks while browsing for it. Cyberchef is a good resource for that

<img width="1162" height="558" alt="Bildschirmfoto vom 2025-10-27 16-34-18" src="https://github.com/user-attachments/assets/646385f8-c4ac-49d5-aa2d-fa5220403e1d" />

Moving on we need to figure out the defanged IP address of the C&C (Command and Control) server, which is a computer used by cybercriminals to remotely communicate with and control a network of infected decives, such as computers, smartphones, and IoT devices.The server sends malicious commands to the compromised machines and receives stolen data or other information from them.

The report thankfully also mentions IP addresses under the Network label, with one in particular being detected on 2020-09-14. This is the one we are looking for.

<img width="817" height="284" alt="grafik" src="https://github.com/user-attachments/assets/e80a6cbe-3d3c-4b16-ba8b-33cc4c2c149c" />

We can use Cyberchef again to defang the IP-address this time (just make sure to insert the original IP-address).

<img width="732" height="561" alt="Bildschirmfoto vom 2025-10-27 16-45-31" src="https://github.com/user-attachments/assets/b5ff03af-0cc0-4727-8cb2-8aefdb587a94" />

Now the last task is asking us something very specific. We need to find out the md5 hash of the spyagent family spyware hosted on the same IP targeting Android devices in Jun 2025. As the report was written in 2023, it unfortunately cannot help us out in this endeavor. VirusTotal however can help us. We just use the IP address that we found before and look under relations for some clues and immediately recognize an android file which also already has an md5 name attached to it.

<img width="1843" height="725" alt="Bildschirmfoto vom 2025-10-27 17-08-44" src="https://github.com/user-attachments/assets/6dc0d9ab-f188-4b35-baf8-01430235cac6" />

With this we solved the challenge and got a feeling on how a Cyber Threat Intelligence analyst would go about solving these kinds of situations. It kind of seemed easy to me, as we didn't really had to make use of that many different websites, but it's a good entry point nonetheless to get your hands dirty. 

