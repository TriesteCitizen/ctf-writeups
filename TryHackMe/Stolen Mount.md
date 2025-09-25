<h1 align="center">Challenge 026 - Stolen Mount </h1>
<p align="center">
  <img width="150" height="150" alt="Bildschirmfoto vom 2025-09-25 13-42-42" src="https://github.com/user-attachments/assets/990cb54d-da3c-490f-979b-7283b18e5c7f" />
</p>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 25.09.2025 </p>

This is a challenge where we tackle Computer forensics. We will analyse network traffic related to an unauthenticated file share access attempt, focusing on potential signs of data exfiltration. I never did something like that so this will probably be a huge learn effect for me. At least I hope so.

In this task the an intruder has targeted the NFS server where the backup files are stored. A classified secret was acessed and stolen. Our only trace that we have is a packet capture (PCAP) file recorded during the incident. We need to discover the contents of the stolen data.

The packet capture is stored in the ~/Desktop directory and is called *challenge.pcapng*, so we first make sure to open that with Wireshark. In this file our first job should be to filter to NFS protocol traffic.

<img width="955" height="391" alt="image" src="https://github.com/user-attachments/assets/b6dd4577-ddea-4e96-ab4f-5f63f25ca70b" />

After having done that we can make sure to follow the TCP stream of any of these packets to get some valuable insight. By analyzing the stream, we can see the entire conversation between the client and server, which may reveal unauthorized access attempts, commands executed, or file transfers. In this case we spot an md5 hash password after hovering through the stream

<img width="629" height="773" alt="image" src="https://github.com/user-attachments/assets/0edcc616-faae-4af3-95a5-be2aa7b80e25" />

Let's use a tool to decrypt. 

<img width="998" height="141" alt="Bildschirmfoto vom 2025-09-25 15-11-41" src="https://github.com/user-attachments/assets/eb6c669f-cf5f-4ee5-8a72-ea4ceea32a97" />

The password seems to be avengers. Now we just need to find out, where to insert that password. By further examining the TCP stream there is a zip.file that I seemed to have overlooked

<img width="597" height="98" alt="image" src="https://github.com/user-attachments/assets/e8194151-7214-4605-b3d9-395cbc139310" />

By converting the TCP stream into a raw zip file, we were able to make sure that the data packets that were transferred over the network were included. It also contained any commands and payloads that were issued. As a zip file was being transferred in the TCP stream, it would include the encrypted content, that we were then able to decrypt with the given password. 

```
ubuntu@tryhackme:~$ ls
Desktop    Downloads  Pictures  Templates  file.zip
Documents  Music      Public    Videos     snap
ubuntu@tryhackme:~$ unzip file.zip
Archive:  file.zip
warning [file.zip]:  36452 extra bytes at beginning or within zipfile
  (attempting to process anyway)
[file.zip] secrets.png password: 
  inflating: secrets.png             
ubuntu@tryhackme:~$ 
```

After the procedure of unzipping the file we are faced with a *secrets.png* that contains a QR code. I just scanned it with my smartphone and received the necessary flag.

<img width="432" height="199" alt="image" src="https://github.com/user-attachments/assets/0a1d10f3-4908-4e8e-a0aa-28d44693f016" />

Great. This wasn't even THAT difficult, but as it was my first time really diving into network traffic I made a lot of unnecessary mistakes and was not sure how to tackle this challenge. Hopefully next time, I will be able to solve such a task sooner.

### Lessons Learned

- **Stay systematic**: Filtering protocols (like *nfs* or *tcp*) and following the data flow step by step is the fastest way to spot intruder activity
- **Always hunt for file transfers**: If there's a PCAP and suspicious activity, chances are something interesting like a ZIP, EXE, or weird binary blob is hiding in those streams
- **Zip signatures**: Zip parsers scan the file for ZIP signatures (e.g. *PK\x03\x04* for file headers and the central directory at the end) and will attempt extraction when a valid structure exists inside the blob. It doesn't matter if there are extra payloads/commands as *unzip* will only focus on the headers. Even with extra bytes a zip is not necessarily corrupted.
