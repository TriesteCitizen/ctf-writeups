<p align="center">
  <img src="assets/itsybitsy.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 22.07.2026  </p>

This is a challenge room, which gives us the simple challenge to investigate an alert by IDS regearding a potential C2 communication.

## Scenario
During normal SOC monitoring, Analyst John observed an alert on an IDS solution indicating a potential C2 communication from a user Browne from the HR department. A suspicious file was accessed containing a malicious pattern THM:{ ________ }. A week-long HTTP connection logs have been pulled to investigate. Due to limited resources, only the connection logs could be pulled out and are ingested into the connection_logs index in Kibana.

After deploying we enter the dedicated machine IP.

<img width="754" height="359" alt="Bildschirmfoto vom 2026-07-22 21-56-18" src="https://github.com/user-attachments/assets/c8723d3d-8a5d-4c7b-9e9a-6b6f0f102f9b" />

## How many events were returned for the month of March 2022?
I adjusted the date to a bigger timeframe so I could overlook all possible events.

<img width="757" height="794" alt="grafik" src="https://github.com/user-attachments/assets/f400652f-212a-4790-a658-ed56abf36c61" />

We get 1482 hits. Which is also the total number of events for March it seems. 

## What is the IP associated with the suspected user in the logs?
This is the time where we add fields like the source ip to our overview. Clicking on it already gives us insights about possible suspicious outliers.

<img width="757" height="794" alt="grafik" src="https://github.com/user-attachments/assets/1e139185-b673-419c-8dbd-3fad56ae6787" />

By adding it to our filter we can also filter out all unnecessary entries.

<img width="756" height="717" alt="grafik" src="https://github.com/user-attachments/assets/1e66c056-c2c9-4e09-935d-4585383e6661" />

## The user’s machine used a legit windows binary to download a file from the C2 server. What is the name of the binary?
Through our previous filter we can now focus on both entries, that give us all necessary information for all the last questions. The binary in question that was used is bitsadmin.

<img width="1085" height="690" alt="Bildschirmfoto vom 2026-07-22 22-13-54" src="https://github.com/user-attachments/assets/dbcb119b-935c-4006-94ff-3842b74a7ebb" />

Bitsadmin is a built-in Windows command-line tool used to create, manage and monitor file download or upload jobs. It relies on the Windows Background Intelligent Transfer Service (BITS), which transfers files in the background using idle network bandwidth. Someone tried to silently download or upload a file over HTTP/HTTPS.

## The infected machine connected with a famous filesharing site in this period, which also acts as a C2 server used by the malware authors to communicate. What is the name of the filesharing site?
pastebin.com
<img width="1085" height="690" alt="grafik" src="https://github.com/user-attachments/assets/8646db17-2dff-4ccf-a2c3-c16b4882188c" />

## What is the full URL of the C2 to which the infected host is connected?
pastebin.com/yTg0Ah6a
<img width="1085" height="690" alt="grafik" src="https://github.com/user-attachments/assets/669b2c96-70ab-42ac-b810-6bfb7de99107" />

## A file was accessed on the filesharing site. What is the name of the file accessed?
<img width="1084" height="281" alt="Bildschirmfoto vom 2026-07-22 22-27-52" src="https://github.com/user-attachments/assets/8427d644-c95d-4c65-9647-791fd3db53b9" />

## The file contains a secret code with the format THM{_____}.
Indeed it does. It can be seen in the upper screenshot.
