<h1 align="center">Benign </h1>

<p align="center">
  <img src="assets/benign.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 11.08.2026 </p>

This is a challenge that focuses on investigating a compromised host. We will analyze host-centric logs to find suspicious process execution. We start by deploying the machine.

## Scenario: Identify and Investigate an Infected Host
One of the client's IDS indicated a potentially suspicious process execution indicating one of the hosts from the HR department was compromised. Some tools related to network information gathering/scheduled tasks were executed which confirmed the suspicion. Due to limited resources, we could only pull the process execution logs with Event ID: 4688 and ingested them into Splunk with the index **win_eventlogs** for further investigation.

### About the Network Information
The network is divided into three logical segments. It will help in the investigation.

**IT Department**
- James
- Moin
- Katrina

**HR Department**
- Haroon
- Chris
- Diana

**Marketing Department**
- Bell
- Amelia
- Deepak

### How many logs are ingested from the month of March, 2022?
After opening Splunk I opted on setting the date range between the SYSTEMfirst and last day of March the 2022th for our index "win_eventlogs". 

<img width="1119" height="490" alt="Bildschirmfoto vom 2026-08-11 12-39-28" src="https://github.com/user-attachments/assets/cc0fbd04-94fc-4ef9-b905-f24714e754a3" />

The output gives us the right answer.

### Imposter Alert: There seems to be an imposter account observed in the logs, what is the name of that user?
Looking at the left sidebar it might make sense taking a closer look at the UserName field.

<img width="862" height="533" alt="grafik" src="https://github.com/user-attachments/assets/3145cd0d-aa5b-43b1-83ea-e85b9076b209" />

We get an overview of the top 10 values. At the same time all of these usernames align with the given network information. The total amount of username values is 11. Let's check the last one, by getting a report for rare values.

<img width="858" height="786" alt="grafik" src="https://github.com/user-attachments/assets/39f50be3-7a81-49af-b3ee-da8ff32fc24d" />

There we have our imposter.

### Which user from the HR department was observed to be running scheduled tasks?
This one was a little tricky. I managed to construct a query that looked for a command containing sc, which communicates the Service Control Manager to manage, configure, start, stop, and query Windows services and system drivers. I grouped the processes to the corresponding users, who started the command.

<img width="866" height="438" alt="grafik" src="https://github.com/user-attachments/assets/6c317edf-ee4c-4454-8f35-3edb87240713" />

As we can see a command was found that created a new scheduled task. 
- With `/create` the system was instructed to build a brand new scheduled task
- `tn OfficUpdater` sets the Task Name to "OfficUpdater", which tries to mimic legitimate updates
- `/tr "C:\Users\Chris.fort\AppData\Local\Temp\update.exe` defines the Task Run path, which is the exact program or executable that the task will launch
- Finally `/sc onstart` sets the Schedule trigger. This tells Windows to run this executable automatically every single time the computer boots up

The user in question was Chris.fort.

### Which user from the HR department executed a system process (lolbin) to download a payload from a file-sharing host?
Since I did not know what kind of binaries could be used to download payloads I did some research. Firstly a LOLbin (Livin off the Land Binary) process name is a legitimate, pre-installed operating system file - such as `powershell.exe, rundll32.exe`, or `certutil.exe` - that is abused to perform unauthorized tasks. Because these process names belong to trusted system tools, they help malicious activity blend in with normal computer operations. With that knowledge I fixed my command to search for Process Names that contained the certutil executable.

<img width="866" height="438" alt="grafik" src="https://github.com/user-attachments/assets/a13642fc-3682-4147-9133-e83b49ed07d8" />

And yet again this highly suspicious command was found. Here the breakdown:
- `certutil.exe` is a legitimate, pre-installed Windows utility designed for managing certificates. Because it is a trusted Microsoft binary, security tools often allow it to run and network-communicate without triggering immediate blocks.
- `urlcache`: an option within `certutil` meant to display or delete URL cache entries. Threat actors abuse it because it forces the binary to perform network requests.
- `-f`: Forces `certutil` to fetch the URL and overwrite any existing local files with the same name.
- `-`: Tells the utility to suppress standard output or processes the URL directly from the stream.
- `https://controlc.com/e4d11035`: The target URL containing the hosted code.

This time the perpetrator is haroon.

### To bypass the security controls, which system process (lolbin) was used to download a payload from the internet?
We already figured this out in the prior task: certutil.exe

### What was the date that this binary was executed by the infected host?
I clicked on the event to see all necessary information and fields.

<img width="678" height="529" alt="grafik" src="https://github.com/user-attachments/assets/2fe9cd63-dda9-401a-89cc-126f21d20d51" />

This also revealed the date: 2022-03-04.

### Which third-party site was accessed to download the malicious payload?
Once again, we already figured this out beforehand: The answer is `controlc.com`, which is a legitimate, free online pastebin service. It allows users to quickly paste plain text, source code, or configuration files into a web form and generate a unique, shareable URL. Because it is a public platform that doesn't require strict identity verification, it is heavily used - and frequently abused - by different groups of people. In our context the URL acts as a staging server or Command and Control (C2) delivery channel.

### What is the name of the file that was saved on the host machine from the C2 server during the post-exploitation phase?
The file in question should be `benign.exe`. It is listed in the very end of the CommandLine field. 

### The suspicious file downloaded from the C2 server contained malicious content with the pattern THM{...}; what is the pattern?
To find that out we simply have to browse the same URL that is specified in the CommandLine field we found.

<img width="867" height="384" alt="Bildschirmfoto vom 2026-08-11 14-20-17" src="https://github.com/user-attachments/assets/6fc55a91-0aeb-42f7-bed3-3b21fc73cc08" />

It harbors a flag, that we can paste in our answer.

### What is the URL that the infected host connected to?
See the previous tasks.

## Lesson Learned
This challenge taught me some intuitive Splunk queries that should hopefully help me in the future if I ever need to find out specific Command lines and map them to a specific user. I also deepened my knowledge regarding lolbins and how a threat actor could try to construct a C2 server. I have to keep my eyes open for URLs like controlc.com and how an attacker thinks. This was very enjoyable, even if easy. Hopefully it gets more difficult in future.
