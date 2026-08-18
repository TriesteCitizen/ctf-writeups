<h1 align="center">Tempest </h1>

<p align="center">
  <img src="assets/tempest.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

This room aims to introduce the process of analyzing endpoint and network logs from a compromised asset. Given the artefacts, we will aim to uncover the incident from the Tempest machine. In this scenario, we will be tasked to be one of the Incident Responders that will focus on handling and analyzing the captured artefacts of a compromised machine

## Preparation - Tools and Artifacts
Before conducting the investigation one of the most important steps is to compare the artefacts by their hashes. It is a common practice to verify if the artefacts are expected as it is.

You can get the hashes of each artefact by running Powershell from the taskbar and executing the following commands:

```
PS C:\Users\user> cd Desktop
PS C:\Users\user\Desktop> cd 'Incident Files'
PS C:\Users\user\Desktop\Incident Files> ls


    Directory: C:\Users\user\Desktop\Incident Files


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        6/21/2022   1:46 AM       17479060 capture.pcapng
-a----        6/21/2022   1:30 AM        3215360 sysmon.evtx
-a----        6/21/2022   1:29 AM        1118208 windows.evtx

PS C:\Users\user\Desktop\Incident Files> Get-FileHash -Algorithm SHA256 .\capture.pcapng

Algorithm       Hash                                                                   Path
---------       ----                                                                   ----
SHA256          CB3A1E6ACFB246F256FBFEFDB6F494941AA30A5A7C3F5258C3E63CFA27A23DC6       C:\Users\user\Desktop\Inciden...

PS C:\Users\user\Desktop\Incident Files> Get-FileHash -Algorithm SHA256 .\sysmon.evtx

Algorithm       Hash                                                                   Path
---------       ----                                                                   ----
SHA256          665DC3519C2C235188201B5A8594FEA205C3BCBC75193363B87D2837ACA3C91F       C:\Users\user\Desktop\Inciden...

PS C:\Users\user\Desktop\Incident Files> Get-FileHash -Algorithm SHA256 .\windows.evtx

Algorithm       Hash                                                                   Path
---------       ----                                                                   ----
SHA256          D0279D5292BC5B25595115032820C978838678F4333B725998CFE9253E186D60       C:\Users\user\Desktop\Inciden...
```

The toolset needed for this task is focused on analyzing Sysmon Logs, Windows Event Logs, and Packet Capture.

To analyze Windows artefacts such as Windows Event Logs and Sysmon logs, we will use the following tools:
- EvtxEcmd
- Timeline Explorer
- SysmonView
- EventViewer

To analyze the provided packet capture, we will use the following tools:
- Wireshark
- Brim

### EvtxEcmd & Timeline Explorer
Eric Zimmerman has created a set of forensic tools used to analyze Windows artefacts called EZTools (Eric Zimmerman's Tools). For this task, we will focus on **EvtxEcmd and Timeline Explorer**, as these tools are mainly used for parsing and analyzing Evtx logs.

EvtxEcmd is a command-line tool which parses Windows Event Logs into different formats such as CSV, JSON, XML, etc. We may use this tool in conjunction with Timeline Explorer, created by the same author, Timeline Explorer is a GUI-based tool that functions as a data filtering and navigating application to ease incident responders in handling raw data.

To parse the provided logs, we need first to convert the EVTX logs into CSV using EvtxEcmd and then feed into Timeline Explorer.

```
PS C:\Tools\EvtxECmd> .\EvtxECmd.exe -f 'C:\Users\user\Desktop\Incident Files\sysmon.evtx' --csv 'C:\Users\user\Desktop\Incident Files' --csvf sysmon.csv
EvtxECmd version 1.0.0.0

Author: Eric Zimmerman (saericzimmerman@gmail.com)
https://github.com/EricZimmerman/evtx

Command line: -f C:\Users\user\Desktop\Incident Files\sysmon.evtx --csv C:\Users\user\Desktop\Incident Files --csvf sysmon.csv

Warning: Administrator privileges not found!

CSV output will be saved to C:\Users\user\Desktop\Incident Files\sysmon.csv

Maps loaded: 383

Processing C:\Users\user\Desktop\Incident Files\sysmon.evtx...
Chunk count: 42, Iterating records...

Event log details
Flags: None
Chunk count: 42
Stored/Calculated CRC: EAFDE57A/EAFDE57A
Earliest timestamp: 1601-01-01 00:00:00.0000000
Latest timestamp:   2022-06-20 17:30:35.3630890
Total event log records found: 2,559

Records included: 2,559 Errors: 0 Events dropped: 0

Metrics (including dropped events)
Event ID        Count
1               238
2               2
3               92
5               3
8               3
11              1,024
12              186
13              869
15              6
22              136

Processed 1 file in 19.8850 seconds
```

For TimelineExplorer.exe, we can load the exported CSV file by doing the following: File > Open > Choose sysmon.csv from C:\Users\user\Desktop\Incident Files directory

<img width="1832" height="858" alt="grafik" src="https://github.com/user-attachments/assets/0f563773-372f-41aa-b13c-4cab2a577b86" />

Once the logs are loaded, we may navigate through each column and use the input field to filter specific logs via a unique string.

<img width="1920" height="566" alt="grafik" src="https://github.com/user-attachments/assets/b76fcba3-725c-4319-bc4a-bba5df7b06d1" />

Lastly, we may use the search feature in the upper right-hand corner to find a unique string that may exist on a column.

### SysmonView
SysmonView is a Windows GUI-based tool that visualizes Sysmon Logs.

Before using this tool, we must export the log file's contents into XML via **Event Viewer**.

<img width="1958" height="1044" alt="grafik" src="https://github.com/user-attachments/assets/4f0c5c45-f3ad-4e94-ad89-86be061219a1" />

The machine will notify us once the file has been successfully exported.

Usage:

- We have to go to File > Import Sysmon Event Logs then choose the XML files generated using the Event Viewer.
- Once loaded, the left sidebar has search functionality that can filter a specific process in mind.
- Choose the image path and session GUID to render the mapped view.

<img width="2474" height="1458" alt="grafik" src="https://github.com/user-attachments/assets/cd5e9647-3429-4a16-8581-c439bb9d433b" />

This tool can easily view the correlated events from a specific process. The example above summarizes all Sysmon events related to **explorer.exe**.
