<h1 align="center">Challenge 022 - Epoch </h1>
<p align="center">
  <img width="106" height="107" alt="output-onlinepngtools" src="https://github.com/user-attachments/assets/77db303d-12cb-49be-a6a1-3d31eeaf1315" />
</p>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: 18.09.2025 </p>

In this challenge we work with a tool that is able to convert our UNIX dates and timestamps. For that we only have to access a website that passes our input along to that command-line program. When we write down the targets information we are greeted with following URL

<img width="934" height="326" alt="image" src="https://github.com/user-attachments/assets/ab8ab794-7fa4-4327-9f66-a0b9b6f5a87b" />

As I already used 

```
root@ip-10-10-224-212:~# date +%s
1758202064
```

I was easily able to check for the right output.
The task itself hints at the fact that one should consider command injections as a way to get the flag. The task itself also has the decency to already tell us that the website passes our input right along to the Linux command line, which we will take to our advantage. First I started the simple semicolon break with ls.

<img width="468" height="277" alt="image" src="https://github.com/user-attachments/assets/1640585c-ff7e-4f2e-8a82-8b6197cfe761" />

My god. It was that easy. Amazing. At first I started cat'ing the main, which was not the smartest idea, as the application almost broke through that. 

While trying to craft some other payloads I was thinking of what kind of sensitive data could now be accessed. The hint given by the exercise itself was to consider that the developer likes to store data in environment veriables, which would be a security risk as there could be API keys or database credentials that a typical end-user should not be able to directly access or even modify, so I used 

<img width="470" height="175" alt="Bildschirmfoto vom 2025-09-18 15-51-11" src="https://github.com/user-attachments/assets/576004d0-7de2-4e32-b3f7-97dcdd057878" />

This is a clear indication that the command I injected is being processed, but not correctly interpreted. This could indicate that the command injection isn't functioning as intended possibly due to how the input is being sanitized or executed. Even trying things like

```
; find -name 'flag*'
```

lead to the same result, so I tried thinking of easier commands that wouldn't be so long.

Finally, shortening the input to *; env* lead to the reveal of the flag itself

<img width="543" height="340" alt="Bildschirmfoto vom 2025-09-18 15-56-09" src="https://github.com/user-attachments/assets/74ef6c61-227e-4e63-9942-0a0ad1e567b4" />

Environment variables are key-value pairs that store configuration settings or system information that applications can access during execution. The *env* command is used in Unix-like operating systems to display the current environment variables. It allows users to see what variables are set, which can include paths, configuration settings, and other crucial information the application relies on.

It's never good to create websites that just forward the commands of a Linux shell, as that makes a lot of command injection vulnerabilities possible. If there already is a command-line Linux program that does the intended job for the website there is no need to create unnecessary websites, or IF you really want to create such a site, at least sanitize the input!
