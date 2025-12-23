<h1 align="center">Challenge 058 - h4cked </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/1e1ceab5-338c-4003-a9da-9590ced8f2d4" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️  </p>

For this scenario it seems our machine got hacked by an enonymous threat actor. However, we are lucky to have a .pcap file from the attack. We need to determine what happened. 

## Oh no! We've been hacked!

Downloading the .pcap file we use Wireshark to get an idea about what went down and how our device got compromised.

Immediately when analyzing the file on Wireshark we recognize a bunch of TCP connections that were being made. Following the TCP stream in Wireshark allows us to view all the data exchanged between two endpoints in a TCP connection. It helps analyzing the contents of packets in the order they were sent and received, making it easier to identify issues, reconstruct conversations, and gather insights about the communication. 

<img width="917" height="366" alt="image" src="https://github.com/user-attachments/assets/d91d5dcd-3afa-40fc-8313-2311e03ca43f" />

The first question is specifically asking about the service the attacker was trying to log in to. Following the TCP stream makes it clear that it's the FTP service. It's a standard network protocol used to transfer files between a client and a server over a TCP/IP network.

The second question is mentioning a very popular tool by Van Hauser, which can be used to brute force a series of services. The name of that tool would be hydra. We can also identify patterns in Wireshark, where a lot of login attempts from a single IP address were executed within a short time period.

<img width="1102" height="592" alt="image" src="https://github.com/user-attachments/assets/df95f794-9a6d-4e72-b5e9-192483e62b2c" />

With the screenshot we can already determine the username with which the attacker was trying to login as well. Now if we want to find out the user' password we just keep on scrolling through the packets until we find a response packet, that talks about a successful login. The request packet before that contains the right password.

<img width="1060" height="75" alt="image" src="https://github.com/user-attachments/assets/db49e83c-7ece-4f68-a8a2-fa10e9c643f7" />

We keep on scrolling to find out the current FTP working directory after the attacker logged in. 

<img width="1168" height="92" alt="image" src="https://github.com/user-attachments/assets/1ded435b-e0eb-4483-b60e-baea6a8991ea" />

After that we are asked about the backdoor that the attacker uploaded. What is the backdoor's filename? Once again we just keep on following the procedure of scrolling through the packets sent through the FTP service and quickly find an executable that is being uploaded through the STOR command. 

<img width="1240" height="181" alt="image" src="https://github.com/user-attachments/assets/993b7b79-4b55-4802-b7b2-47e389af7f09" />

Now we are tasked to find out the URL, from which this specific backdoor can be downloaded. The location itself is clarified inside the uploaded file. To get a hold of those information, we can filter for FTP data transfer packets. This filter allows us to view the packets that are involved in the actual file transfer occuring during an FTP session, making it easier to analyze the data being transferred.

<img width="1117" height="931" alt="image" src="https://github.com/user-attachments/assets/f4e003da-ef3c-4e74-a8b0-4f371d1460dc" />

The line-based text data reveals all the information we need.

Now we are getting to the part where the attacker successfully got his reverse shell running and proceeds to manually execute commands. To find that part of the interaction in Wireshark we just have to look for packets that are running a HTTP GET request at '/shell.php', as this suggests the attacker is exploiting the vulnerability. After the GET request is being acknowledged and synchronization is taking place we can try following the TCP stream once again.

<img width="962" height="901" alt="image" src="https://github.com/user-attachments/assets/2c5326ec-70c0-4711-b4d2-d1bc6b217cb5" />

With that we get a good idea on the actions the attacker took after compromising the machine. When further scrolling through the TCP stream, we see a very particular segment, that turns the regular shell session into a new shell with elevated permissions (switching to the 'jenny' user).

<img width="849" height="469" alt="image" src="https://github.com/user-attachments/assets/a50a241c-dad7-4098-86f8-aebb0f6da94f" />

The prompt '$' changes to 'jenny@wir3:/$'. This indicates that we are now operating under the 'jenny' user's context, and 'wir3' is the hostname of the machine. The change signifies that we have successfully escalated privileges and are now in a different user environment. The same screenshot also showcases the command with which the attacker spawned a new TTY shell. With it, the attacker was able to gain information to finally get a root shell.

<img width="846" height="419" alt="image" src="https://github.com/user-attachments/assets/7c4093bb-2b9f-4f2d-a094-21f4cf001c49" />

The attacker did what a lot of people would, when trying to escalate privileges: check which kind of commands the user would be able to run as sudo. In this instance 'jenny' seems to have had the ability to run EVERY command with sudo. Very bad and a high security concern. Here the attacker used it to his advantage to just switch the user to root.

After gaining root privileges the attacker downloaded something from GitHub. What is the name of the GitHub project? Just follow through with the TCP stream to be enlightened and get the answer for said question.

<img width="477" height="231" alt="image" src="https://github.com/user-attachments/assets/170da34e-a641-4a1c-9569-dbb6b838be23" />

The last thing to determine was what kind of stealthy backdoor was being installed on the system. With the name of the GitHub project known I thought just setttling on checking out the repository itself would be enough, but unfortunately it had been disabled.

<div align="center">
  <img width="464" height="204" alt="image" src="https://github.com/user-attachments/assets/2cbbc2b6-3c3a-4c2e-bd66-d86cf5b3f3bf" />
</div>

By using common sense I still was able to determine that this probably would have to be a rootkit. If we consider the fact that the question itself is mentioning a stealthy backdoor, that is very hard to detect it very much aligns with the idea of a rootkit, that is designed to gain unauthorized access to a computer or network, *while hiding it's presence*. It allows an attacker to maintain control over a system without being detected. Problem solved! Well not quite. Hacking back to the machine is the next goal though...

## Hack your way back into the machine

