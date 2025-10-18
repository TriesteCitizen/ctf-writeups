<h1 align="center">Challenge 043 - Summit </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/8f6b9803-eaf5-4a89-813c-24f5a8613771" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 18.10.2025  </p>

As I didn't have the opportunity to really engage in any real blue teaming I made sure to get some experience in, where I could get acquainted with some challenges a SOC might have to face. In this CTF we have to chase a simulated adversary up the Pyramid of Pain until they finally back down.

After participating in one too many incident response activities, the oganization PicoSecure has decided to conduct a threat simulation and detection engineering engagement to bolster its malware detection capabilities. We have been assigned to work with an external penetration tester in an iterative purple-team scenario. Here the tester will be attempting to execute malware samples on a simulated internal user workstation. At the same time, we will need to configure PicoSecure's security tools to detect and prevent the malware from executing.

We will follow the Pyramid of Pain's ascending priority of indicators, the objective being to increase the simulated adversaries' cost of operations and chase them away for good. Each level of the pyramid allows us to detect and prevent various indicators of attack.

After succesfully deploying the machine we are greeted with a mailbox and the following message

<img width="1846" height="820" alt="image" src="https://github.com/user-attachments/assets/fa53abc8-14de-4600-afb7-8963350febea" />

As the message itself already mentioned we probably should analyze the binaries with a Malware Analysis tool and review the generated report.

<img width="1846" height="820" alt="image" src="https://github.com/user-attachments/assets/a84b211d-d44b-4203-a21f-b5eb2b19bdc8" />

Having done that the checksums of the hashes get generated. We probably can add them to a Hash Blocklist. We click on the option "Manage Hashes" and now it was pretty evident how to move on from here.

I added the MD5

```
cbda8ae000aa9cbe7c8b982bae006c2a
```
SHA1
```
83d2791ca93e58688598485aa62597c0ebbf7610
```
and SHA256
```
9c550591a25c6228cb7d74d970d133d75c961ffed2ef7180144859cc09efca8c
```
hashes to the blocklist

<img width="1846" height="656" alt="image" src="https://github.com/user-attachments/assets/4e1f581b-defd-4b49-b368-2abcc594b5bf" />

but quickly realized that we only would have to do it for one of the hashes as the blocklist will take care of covering its SHA1 and SHA256 representations as well.

<img width="1151" height="201" alt="image" src="https://github.com/user-attachments/assets/7eab80f3-6ed6-4cc4-a394-ac52e29c88a8" />

We received another flag that also included the flag and the instructions for the next step we have to take

<img width="1163" height="577" alt="Bildschirmfoto vom 2025-10-18 13-19-05" src="https://github.com/user-attachments/assets/655adeb3-7ca4-4bcd-9241-6c9c9d21fa8f" />

The mail mentions how easy it is to block the malware from executing, since file hashes and digests are unique to each file. But when only one bit of that file is changed the detection mechanism will fail. With this second sample we need to figure out a new way to detect the executable. We move on and scan the malware sandbox

<img width="1157" height="538" alt="image" src="https://github.com/user-attachments/assets/6f0b565b-fe8e-40db-b5c7-64a0d1aa961e" />

In here we can recognize that there seems to be some suspicious network traffic, where a specific HTTP request is made. In our Firewall Rule Manager we can prevent that Request from ever being made.

<img width="1843" height="496" alt="image" src="https://github.com/user-attachments/assets/c9001d8f-7ff3-4f7e-b91b-f05524fbb667" />

Just to be sure that the difference between Ingress and Egress is clear for me. Ingress refers to incoming traffic to a network or system, while egress refers to outgoing traffic, which makes sense as the malware gets executed in our network and forces us to do an HTTP request to the spcific IP destination.

We receive another mail 

<img width="1186" height="613" alt="Bildschirmfoto vom 2025-10-18 13-43-18" src="https://github.com/user-attachments/assets/c4da9d25-a774-46bb-9929-625f3405efd9" />

The IP address was detected, but this method isn't that secure either, as an adversary can get around to using a new public IP address, e.g. like Sphinx mentioned, through a cloud service provider an adversary would have the possibility to access many more public IPs.

We will move on with scanning the third sample and realize pretty quick that this time there are some suspicious DNS requests being made

<img width="1161" height="172" alt="Bildschirmfoto vom 2025-10-18 13-50-08" src="https://github.com/user-attachments/assets/f712d4be-34c0-4f6b-bcd1-50558d752858" />

I already saw that there was a DNS Filter that we can utilize.

<img width="1825" height="474" alt="image" src="https://github.com/user-attachments/assets/73647551-ed02-420e-ad14-bbae45f1363b" />

While the first domain request didn't seem to be fake the second one was suspicious. We succeeded in filtering the right domain and can move on with the next mail.

<img width="1169" height="606" alt="Bildschirmfoto vom 2025-10-18 13-57-57" src="https://github.com/user-attachments/assets/3d4ea792-3dd3-4cd7-9890-78d1a95e012e" />

As the domain was able to get detected, every new IP address of the adversary is successfully being detected as well. He has to buy and register new domain names and modify DNS records. For this sample we have to consider what artifacts (or changes) the malware leaves on the vitim's host system now.

For that we can check the Registry Activity

<img width="1172" height="353" alt="image" src="https://github.com/user-attachments/assets/ea6b353c-1153-422a-a12f-9d59f269bfe4" />

Now we move on to the Sima Rule Builder and create a new rule. In this case we want to establish a rule that monitors and logs various system activities. It provides detailed information about command line activity, process creations, network connections, file creation, and more. As there clearly was some Registry Activity we choose the option that emphasizes Registry Modifications. In here the conditions we set are:

<img width="650" height="270" alt="image" src="https://github.com/user-attachments/assets/92a998ba-c7d5-4ee1-9854-048811f056cc" />

which gives us the following Sigma Rule Validation

<img width="1017" height="662" alt="image" src="https://github.com/user-attachments/assets/b5d888ab-f6c3-43f1-b109-dbe76a9117b9" />

We receive the next mail after having configured the rule.

<img width="1172" height="709" alt="Bildschirmfoto vom 2025-10-18 14-20-56" src="https://github.com/user-attachments/assets/0af08c94-2e72-4c36-a587-ce28e879624e" />

We learn that having the team develop new techniques in the adversaries tools is a time-consuming effort and a significant cost, which makes sense.

In the following sample all of the heavy lifting and instructions happen on the back-end server of Sphinx. Used artifacts left on the host and protocol types can easily be changed now. Something unique or abnormal about the behavior of the tool needs to be detected.  

The attachment contains the log of the last 12 hours.

```
2023-08-15 09:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 09:23:45 | Source: 10.10.15.12 | Destination: 43.10.65.115 | Port: 443 | Size: 21541 bytes
2023-08-15 09:30:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 10:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 10:14:21 | Source: 10.10.15.12 | Destination: 87.32.56.124 | Port: 80  | Size: 1204 bytes
2023-08-15 10:30:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 11:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 11:30:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 11:45:09 | Source: 10.10.15.12 | Destination: 145.78.90.33 | Port: 443 | Size: 805 bytes
2023-08-15 12:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 12:30:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 13:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 13:30:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 13:32:17 | Source: 10.10.15.12 | Destination: 72.15.61.98  | Port: 443 | Size: 26084 bytes
2023-08-15 14:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 14:30:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 14:55:33 | Source: 10.10.15.12 | Destination: 208.45.72.16 | Port: 443 | Size: 45091 bytes
2023-08-15 15:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 15:30:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 15:40:10 | Source: 10.10.15.12 | Destination: 101.55.20.79 | Port: 443 | Size: 95021 bytes
2023-08-15 16:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 16:18:55 | Source: 10.10.15.12 | Destination: 194.92.18.10 | Port: 80  | Size: 8004 bytes
2023-08-15 16:30:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 17:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 17:09:30 | Source: 10.10.15.12 | Destination: 77.23.66.214 | Port: 443 | Size: 9584 bytes
2023-08-15 17:27:42 | Source: 10.10.15.12 | Destination: 156.29.88.77 | Port: 443 | Size: 10293 bytes
2023-08-15 17:30:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 18:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 18:30:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 19:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 19:30:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 20:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 20:30:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
2023-08-15 21:00:00 | Source: 10.10.15.12 | Destination: 51.102.10.19 | Port: 443 | Size: 97 bytes
```

A pattern that we quickly recognize is the timeframe. We always seem to have time intervals of 30 minutes before the next request is being made, and it also seems to always contain a byte size of 97 bytes. We should probably create another Sigma Rule for that.  

This time the Sysmon Event Log needs to target the network connections, to establish a specific kind of network traffic pattern. The rule consitions we set are

<img width="719" height="512" alt="image" src="https://github.com/user-attachments/assets/9145304b-b3d5-4ff3-92d4-adc3e2b66d67" />

Which successfully creates the right validation

<img width="1014" height="699" alt="image" src="https://github.com/user-attachments/assets/221111bb-abf5-49d3-bdfb-ffd5f5b9453f" />

Checking the new mail gives us the next flag and our last instruction

<img width="1177" height="679" alt="Bildschirmfoto vom 2025-10-18 15-01-05" src="https://github.com/user-attachments/assets/91e450a9-ac20-42a2-9a2f-6143a5bfc4f9" />

We are given the hint to focus more on the techniques and procedures of the adversary and are given recorded command logs from the previous samples.

```
dir c:\ >> %temp%\exfiltr8.log
dir "c:\Documents and Settings" >> %temp%\exfiltr8.log
dir "c:\Program Files\" >> %temp%\exfiltr8.log
dir d:\ >> %temp%\exfiltr8.log
net localgroup administrator >> %temp%\exfiltr8.log
ver >> %temp%\exfiltr8.log
systeminfo >> %temp%\exfiltr8.log
ipconfig /all >> %temp%\exfiltr8.log
netstat -ano >> %temp%\exfiltr8.log
net start >> %temp%\exfiltr8.log
```

Now we have to create a sigma rule that focuses on File Creations and Modifications, clarifying the File Path, File Name and ATT&CK ID

<img width="660" height="351" alt="image" src="https://github.com/user-attachments/assets/c2a4cd56-aaa2-4fb8-94ac-0733e234484f" />

After that we are congratulated and are able to receive the very last flag.

<img width="1173" height="409" alt="Bildschirmfoto vom 2025-10-18 15-08-54" src="https://github.com/user-attachments/assets/c0ed9d8f-9026-4c82-87a5-0f2fa954ef0c" />

This was a very cool way to get acquainted with the Pyramid of Pain and play around with some Indicators of Attacks. It's not quite the simulation of a SOC I expected it to be, but it's a good way to get acquainted with basic ideas that might be valuable when trying to take your first steps in that field. Definetely entertaining.
