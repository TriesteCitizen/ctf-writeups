<h1 align="center">Challenge 027 - Reversing ELF </h1>
<p align="center">
  <img width="90" height="88" alt="Bildschirmfoto vom 2025-09-29 11-04-37" src="https://github.com/user-attachments/assets/8dbd8774-22f0-4da7-ac5b-8a135a34bb2d" />
</p>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 29.09.2025 </p>

This is my first real attempt to do some reverse engineering without using the *strings* command (or so I thought). This will be very intimidating I'm sure (it wasn't), but have so many advantages afterwards (it really didn't).

### Crackme1

First I started Ghidra and dropped the binaries into a project

I analyzed a lot of registers but then figured I should maybe first run the program to see what could happen.

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ ./crackme1
bash: ./crackme1: Keine Berechtigung
```

We were not able to run the binaries. Checking the permissions reveals why

```
-rw-rw-rw-  1 lorenzo lorenzo      7192 Sep 29 11:07  crackme1
```

We have no execution permissions. Something we can quickly change with *chmod*

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ chmod 777 crackme1
```

<img width="711" height="54" alt="Bildschirmfoto vom 2025-09-29 12-18-37" src="https://github.com/user-attachments/assets/386872a1-8353-41bb-9422-e444c220b1e5" />

I apparently thought too much about it and just needed to run the binaries first. I will note that as something general to keep in mind for the future.

### Crackme2

Now before starting Ghidra I did exactly what I learned from the last task and tried running the binaries. The permissions were off again so I swiftly changed those and got the following output afterwards

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ ./crackme2
Usage: ./crackme2 password
```

Now we know for a fact that we had to check what Ghidra would spit out and the Decompiler gave a lot of clues on this one.

<img width="475" height="445" alt="Bildschirmfoto vom 2025-09-29 12-29-18" src="https://github.com/user-attachments/assets/68be5768-61ea-4a60-96a8-a383e74fca51" />

We can see from the main that in this function a string compare is done. A certain parameter equals 2 and compares another parameter against the string, which in this case would be the password. All of this can be deduced by direct observation of the program's logic. We are then able to submit the password.

<img width="738" height="77" alt="Bildschirmfoto vom 2025-09-29 12-42-50" src="https://github.com/user-attachments/assets/dd27ddf1-7948-4b9b-a9ae-5aad56a21c94" />

### Crackme3

Now this task is where the REAL reverse engineering starts. Or so I thought. Out of boredom I used the *strings* command again and immediately saw something that looked like base64. Checking it in Ghidra quickly confirmed all suspicions.

<img width="721" height="591" alt="image" src="https://github.com/user-attachments/assets/7570ab7e-f4c8-4a6f-8a47-e83fd6598aba" />

Time to get those tools to working.

<img width="630" height="496" alt="Bildschirmfoto vom 2025-09-29 12-54-44" src="https://github.com/user-attachments/assets/aed643c9-788e-4d4d-9529-1e0ebf5638a7" />

And the flag jumps out. If we insert the output as a password into the executable we also get told that the password is correct.

<img width="729" height="60" alt="Bildschirmfoto vom 2025-09-29 12-56-44" src="https://github.com/user-attachments/assets/95477839-e028-40ce-9e67-7b2b3df4832e" />

### Crackme4

Once again we have to find a password.

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ ./crackme4 
bash: ./crackme4: Keine Berechtigung
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ chmod 777 crackme4
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ ./crackme4 
Usage : ./crackme4 password
This time the string is hidden and we used strcmp
```

the output itself hints at the idea that the string is hidden in a strcmp function.

At the beginning I tried analyzing the Decompiler and jumping between different functions but instead then just settled on using the *ltrace* function, which works equally well for this sort of task. *ltrace* is a debugging tool that traces library calls made by a program. It intercepts and records the calls to shared libraries and displays the arguments passed to these functions, as well as their return values. This can be useful for understanding how a program interacts with its libraries, including functions like *strcmp*

<img width="663" height="114" alt="Bildschirmfoto vom 2025-09-29 15-45-58" src="https://github.com/user-attachments/assets/17a949f5-ae41-4f98-af8e-8966d0db26d4" />

By using *ltrace* I was able to observe how the program processes input and potentially uncover hardcoded values or passwords, which worked quite well for this example. I once again was able to avoid having to deal with Ghidra.

### Crackme5

For these binaries we have to find out what input we have to give to receive the output *Good game*.

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ chmod 777 crackme5
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ ./crackme5 
Enter your input:
test
Always dig deeper
```

Once again I tried using *ltrace* to check if there are some useful libraries being used

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ ltrace ./crackme5
__libc_start_main(0x400773, 1, 0x7ffc358401f8, 0x4008d0 <unfinished ...>
puts("Enter your input:"Enter your input:
)                        = 18
__isoc99_scanf(0x400966, 0x7ffc35840090, 1, 0x7b19d8b148f7test
) = 1
strlen("test")                                   = 4
strlen("test")                                   = 4
strlen("test")                                   = 4
strlen("test")                                   = 4
strlen("test")                                   = 4
strncmp("test", "OfdlDSA|3tXb32~X3tX@sX`4tXtz", 28) = 37
puts("Always dig deeper"Always dig deeper
)                        = 18
+++ exited (status 0) +++
```

It seems like some for-loop operation is taking place, which goes as long as the input string that we supply +1 additional character. After that we have the strncmp, which gets compared with some key. When we use the same key as input we receive the "Good game" output.

<img width="559" height="77" alt="Bildschirmfoto vom 2025-09-29 16-36-55" src="https://github.com/user-attachments/assets/00b03b4d-3ad5-4e4c-b67e-9545c4aa4969" />

### Crackme6

Everything still worked pretty easily. No real reverse engineering took place as of now, which is relieving but also quite disappointing.

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ ./crackme6
Usage : ./crackme6 password
Good luck, read the source
```

Seems like this will change now though. I started Ghidra and looked at the Decompiled code on our main. Checking that quickly makes it clear that we have to jump into a function *compare_pwd*, which passes the input from the user

<img width="714" height="240" alt="image" src="https://github.com/user-attachments/assets/0c997550-626d-4dce-9b33-fa297e60fc89" />

Having done that we have to jump into another function yet again, as an integer value gets saved into a variable and returns *"password ok"* if the value is 0. So we jump into *my_secure_test*, which passes the user input once again

<img width="714" height="286" alt="image" src="https://github.com/user-attachments/assets/230ccc92-9582-48a4-9abc-9f52f66416f0" />

This function is where all the magic happens

<img width="714" height="653" alt="image" src="https://github.com/user-attachments/assets/0e64054b-1940-4d4f-89d3-ccaa0e97f322" />

As we can clearly see from the Decompiler, there are several statements that check the passed parameter and instantiate the hexadecimal value 0xffffffff and return it to the *compare_pwd* function, which is the incorrect value. We need 0 as a return for everything to work. From the Decompiler we can quickly recognize the exact characters that need to be given in their specific positions of the character array for the returned value to finally be instantiated to 0 in the last else if statement. If we just take that logic we can quickly gather what our password is. We write it in our input.

<img width="635" height="44" alt="Bildschirmfoto vom 2025-09-29 17-13-08" src="https://github.com/user-attachments/assets/bfa75515-ec06-4042-be67-44106419d93a" />

With that we have solved this task too.

### Crackme 7

Now when running these binaries we get the following output

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ ./crackme7
Menu:

[1] Say hello
[2] Add numbers
[3] Quit

[>] 1
What is your name? Lorenzo
Hello, Lorenzo!
Menu:

[1] Say hello
[2] Add numbers
[3] Quit

[>] 2
Enter first number: 5
Enter second number: 100
5 + 100 = 105
Menu:

[1] Say hello
[2] Add numbers
[3] Quit

[>] 3
Goodbye!
```

No real hints or anything special that we can gather from running the binaries. We move on and analyze with Ghidra now.

Checking the main of the Decompiler makes us realize that the local variable *local_14*, which is used to check the user input for this program can have a secret fourth input choice, which retrieves a flag. It's hardcoded in hexadecimal.

<img width="718" height="640" alt="Bildschirmfoto vom 2025-09-29 17-34-31" src="https://github.com/user-attachments/assets/1610f9fc-bf57-49ef-8a14-e3c74c3e78dd" />

Bullseye! Let's convert that into decimal.

<img width="490" height="276" alt="image" src="https://github.com/user-attachments/assets/cdbd029e-3465-4aa3-8a4e-394a43383201" />

Now when we insert this in the running program we receive the flag.

<img width="556" height="188" alt="Bildschirmfoto vom 2025-09-29 17-39-16" src="https://github.com/user-attachments/assets/5c5b2df9-5afd-4de6-a4da-28dcbd972568" />

That takes care of that. Still pretty easy.

### Crackme 8

For this last binary we also have to find a password. *strings* and *ltrace* are not very helpful for this either so we move on to Ghidra.

Checking the Decompiler reveals that we have some sort of hexadecimal value *-0x35010ff3*. The minus sign indicates that the value is a signed integer.

<img width="719" height="442" alt="image" src="https://github.com/user-attachments/assets/6bcf6146-1d05-4f97-8cdf-9dc15804df94" />

We can convert that into it's decimal counterpart of course, which reveals the password.

<img width="486" height="358" alt="Bildschirmfoto vom 2025-09-29 17-50-47" src="https://github.com/user-attachments/assets/1f40f8e9-7112-4e84-811a-448ba6a36d0e" />

Now let's use that value to receive the flag, shall we?

<img width="655" height="60" alt="Bildschirmfoto vom 2025-09-29 17-52-12" src="https://github.com/user-attachments/assets/b4a0f809-d475-450d-bdad-8de2a4fe82dc" />

With this done, we solved all tasks. I'm still a little unsatisfied if I have to be honest. I'm sure that this was only supposed to be an easy introduction, as we were able to solve a lot of these tasks by only reading source code from the Decompiler or working with *strings* and *ltrace*. It definetely is a good starting point and very manageable to beat. Still I hoped to get more into the nitty-gritty of it all, so I hope that I will have the possibility to face more challenging tasks next time around. 
