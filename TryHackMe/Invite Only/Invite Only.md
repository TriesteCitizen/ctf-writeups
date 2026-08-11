<h1 align="center">Invite Only </h1>

<p align="center">
  <img src="assets/inviteonly.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️  </p>

We are a SOC analyst on the SOC team at Managed Server Provider TrySecureMe. Today we are supporting an L3 analyst in investigating flagged IPs, hashes, URLs, or domains as part or IR activities. One of the L1 analysts flagged two suspicious findings early in the morning and escalated them. Our task is to analyze these findings further and distil the information into usable threat intelligence.

Flagged IP: 101[.]99[.]76[.]120
Flagged SHA256 hash: 5d0509f68a9b7c415a726be75a078180e3f02e59866f193b0a99eee8e39c874f

We recently purchased a new threat intelligence search application called TryDetectThis2.0. We can use this application to gather information on the indicators above.

### What is the name of the file identified with the flagged SHA256 hash?
After deploying the machine we immediately make use of our new TryDetectThis2.0 application and search for the hash.

<img width="1118" height="796" alt="grafik" src="https://github.com/user-attachments/assets/3d21701a-b23f-4096-98da-ef353e0bf808" />

Immediately we get a lot of useful information, including the name of the file: syshelpers.exe.

### What is the file type associated with the flagged SHA256 hash?
Displayed right under the file name: Win32 EXE, a 32-bit executable program file made to run on Microsoft Windows.

### What are the execution parents of the flagged hash? List the names chronologically, using a comma as separator. Note down the hashes for later use.
Found out by looking under the Relations section

<img width="1118" height="796" alt="grafik" src="https://github.com/user-attachments/assets/d1a2b5d2-0998-4387-94a4-e066f8598a2d" />

Like the format is expecting we have exactly two execution parents: 361GJX7J (047c5eec0445746862710d20e50a5dd04510b7e625fa5c1f5d48ce078001c0de) and installer.exe (fa102d4e3cfbe85f5189da70a52c1d266925f3efd122091cdc8fe0fc39033942).

### What is the name of the file being dropped? Note down the hash value for later use
Further scrolling down also reveals the dropped file: AClient.exe (dd02c105809e4ca41a5489e585ba025eddb89a91703b73a566c9903e6406a08c).

<img width="483" height="174" alt="grafik" src="https://github.com/user-attachments/assets/624c4861-523d-4a77-965a-aa6fa77b77e2" />

### Research the second hash in question 3 and list the four malicious dropped files in the order they appear (from up to down), separated by commas
Querying the second hash in the application reveals 20 dropped files, but only the first four malicious ones are relevant for us: searchHost.exe, syshelpers.exe, nat1.vbs, runsys.vbs

<img width="479" height="323" alt="grafik" src="https://github.com/user-attachments/assets/18aa513d-828d-461b-8679-b2a4aac08eab" />

### Analyze the files related to the flagged IP. What is the malware family that links these files?
This time we query the flagged IP (without brackets) and can find some useful information in the community section of the entry.

<img width="821" height="758" alt="grafik" src="https://github.com/user-attachments/assets/0d8677e9-a931-4b2e-b7d6-750511290041" />

The malware family that is repeatedly mentioned is AsyncRAT (Asynchronous Remote Access Trojan) - an open-source remote administration tool written in C#. While built for legitimate IT management, it is heavily weaponized by hackers as malware to quietly monitor, steal data from, and control Windows computers through encrypted connections.

### What is the title of the original report where these flagged indicators are mentioned? Use Google to find the report.
In the prior screenshot we can already see that report being mentioned: "Discord Invite Hijacking: How Fake Links Are Delivering Infostealers" URL: https://darkatlas.io/blog/discord-invite-hijacking-how-fake-links-are-delivering-infostealers

From Trust to Threat: Hijacked Discord Invites Used for Multi-Stage Malware Delivery 📅Date: 2025-06-12 🔗References: https://research.checkpoint.com/2025/from-trust-to-threat-hijacked-discord-invites-used-for-multi-stage-malware-delivery
