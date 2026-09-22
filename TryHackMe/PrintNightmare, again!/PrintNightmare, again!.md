<h1 align="center">PrintNightmare, again! </h1>

<p align="center">
  <img src="assets/printnightmare.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

I have to know the fundamentals of Endpoint security, so I don't make a fool out of myself once I start work.

In the weekly internal security meeting it was reported that an employee overheard two co-workers discussing the PrintNightmare exploit and how they can use it to elevate their privileges on their local computers.

Our task is to inspect the artifacts on the endpoint to detect the exploit they used. For this challenge we have to use the FullEventLogView tool. Go to `Options > Advanced Options` and set `Show events from all times`.

<img width="627" height="456" alt="image" src="https://github.com/user-attachments/assets/976f61f1-2628-428e-89c5-7623499d1969" />

### The user downloaded a zip file. What was the zip file saved as?
In this instance checking the FullEventLogView for any string that matches with `.zip` might be our best shot. Through `Edit > Find` we quickly get ahold of a File creation event.

<img width="618" height="317" alt="image" src="https://github.com/user-attachments/assets/d2cd487c-72ff-4cd3-8dbc-9463459ffda2" />

### What is the full path to the exploit the user executed?
Moving on from the prior event I moved on through further events, where an exploit file was being executed being especially cautious for PowerShell scripts (ps1). I quickly found the dedicated target filename.

<img width="662" height="317" alt="image" src="https://github.com/user-attachments/assets/74ef7dd8-bebe-482d-94a7-130cded4308e" />

### What was the temp location the malicious DLL was saved to?
Since I already went through a few log events with the tool I already recognized a DLL named `nightmare.dll`, which is associated with the PrintNightmare exploit, which is a known vulnerability in the Windows Print Spooler service. It's a common payload used by attackers, thus it only makes sense to look for that specific string. We quickly get results that way.

<img width="662" height="317" alt="image" src="https://github.com/user-attachments/assets/934c9900-4ef1-4100-b94c-f9c2ec1970b2" />

### What was the full location the DLL loads from?
Further inspecting the event logs from the prior question reveals another .dll file being executed from the spool driver directory. It's the location where printer drivers are stored specifically for the Print Spooler service. This directory can be suspicious because it may be exploited by attackers to load malicious DLLs that take advantage of vulnerabilities in the Print Spooler service. Any unexpected DLLs in the directory are immediately suspicious.

<img width="662" height="317" alt="image" src="https://github.com/user-attachments/assets/bf7a3dd8-6c4d-4df3-a203-ad6926ea49d7" />

### What is the primary registry path associated with this attack?
The smartest step to take was looking for entries that mentioned `HKLM\System\CurrentControlSet\Control\Print`. HKLM is a registry hive in Windows that contains configuration settings and system information for the local machine. Searching for `HKLM\System\CurrentControlSet\Control\Print` is important because it specifically holds the registry keys related to printer drivers and settings. Doing that reveals the registry path.

<img width="801" height="345" alt="image" src="https://github.com/user-attachments/assets/d5f34ddf-7077-44cb-b802-cf5d91135456" />

### What was the PID for the process that would have been blocked from loading a non-Microsoft-signed binary?
It is important to look out for event logs that explicitly mention Microsoft-Windows-Security-Mitigations, which is the exact next log event in the FullEventLogView. We can see a message that says 

`Process '\Device\HarddiskVolume2\Windows\System32\spoolsv.exe' (PID 2600) would have been blocked from loading the non-Microsoft-signed binary '\Windows\System32\spool\drivers\x64\3\nightmare.dll'.`

It means the Windows Print Spooler process (`spoolsv.exe`) running as PID 2600, tried to load a DLL from the printer drivers folder (`\Windows\System32\spool\drivers\x64\3\nightmare.dll`), but a Windows mitigation (Microsoft-Windows-Security-Mitigations) detected that the DLL was not signed by Microsoft and prevented it from being loaded. In plain terms: a system service attempted to load a suspicious/untrusted driver DLL and the OS blocked that load attempt. Why this matters: loading unsigned DLLs into system services is a common technique used by PrintNightmare and similar exploits to run code with elevated/system privileges, so the event is strong evidence of a malicious driver load attempt - even if the block prevented execution, it shows an attempted compromise.

<img width="841" height="240" alt="image" src="https://github.com/user-attachments/assets/a1c736d9-6046-4108-a2ba-d7b3406798fb" />

### What is the username of the newly created local administrator account?
We look out for an event ID where a new user account is being created (Event ID 4720), which is the log event two entries later from the prior task. 

<img width="852" height="428" alt="image" src="https://github.com/user-attachments/assets/77534636-c1e6-43a1-83c0-f8d70961a8e5" />

### What is the password for this user?
