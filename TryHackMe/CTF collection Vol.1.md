<h1 align="center">Challenge 027 - CTF collection Vol.1 </h1>
<p align="center">
  <img width="90" height="90" alt="Bildschirmfoto vom 2025-09-25 18-10-02" src="https://github.com/user-attachments/assets/c6ac29ba-2fdc-4275-a12d-de7ea44008ad" />
</p>
<p align="center"> <b>Difficulty</b>: 2/10 (Easy) <b>Completed</b>: ✔️ 26.09.2025  </p>

This is another very easy room that will probably not be that big of a hassle, which is exactly what I need right now. While these are 20 tasks, they all apparently are very easy. Let's go.

### Task 1 - What does the base said? 
We need to decode the following

```
VEhNe2p1NTdfZDNjMGQzXzdoM19iNDUzfQ==
```

This seems to be base64 encoded. 

<img width="659" height="595" alt="Bildschirmfoto vom 2025-09-25 18-17-34" src="https://github.com/user-attachments/assets/4e7cac42-cf20-4e75-8374-a7fa15e9405b" />

And I was right. Very good. Moving on.

### Task 2 - Meta

Now we have to download a task file containing the following picture

<img width="796" height="480" alt="image" src="https://github.com/user-attachments/assets/dc5bad84-6929-4b66-b2d3-c4da37742c4f" />

The steganography decoder didn't lead to any valuable insights. But StegOnline did. I checked for strings and immediately got some interesting results.

<img width="664" height="198" alt="Bildschirmfoto vom 2025-09-25 18-27-01" src="https://github.com/user-attachments/assets/3d4d282e-0f0e-4ffa-b5c8-3078b33da68b" />

### Task 3 - Mon, are we going to be okay?

Yet again another Steganography challenge, with this quite... dark picture

<img width="748" height="475" alt="Bildschirmfoto vom 2025-09-25 18-31-08" src="https://github.com/user-attachments/assets/13e3f06b-00ff-4029-b6ef-874a96dac200" />

☠️ I---

Anyways... I just used steghide for this one

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ steghide --extract -sf Extinction_1577976250757.jpg
Passwort eingeben: 
Extrahierte Daten wurden nach "Final_message.txt" geschrieben.
```

We can check out the message now, which is saved in *Final_message.txt*

<img width="395" height="70" alt="Bildschirmfoto vom 2025-09-25 18-35-20" src="https://github.com/user-attachments/assets/b4a291b4-fed9-4468-a8c0-cbea6b482376" />

☠️☠️☠️

### Task 4 - Erm......Magick

<img width="307" height="63" alt="Bildschirmfoto vom 2025-09-25 18-39-30" src="https://github.com/user-attachments/assets/48e9ee9b-8858-40f0-baf2-e7e783c514ab" />

We have some text that is covered in white. When highlighting it, it reveals the flag. The hint itself also mentioned how we could be able to check the html of this page, which is another neat way to solve this task. It's not particularly difficult in any case.

### Task 5 - QRrrrr

This time we have a QR-code. I'm sure most people know how to scan one of those with their smartphones.

<img width="347" height="185" alt="Bildschirmfoto vom 2025-09-25 18-43-45" src="https://github.com/user-attachments/assets/a2f74d25-aa87-4de3-849e-108bfeae5e64" />

### Task 6 - Reverse it or read it?

Now we receive some executable that we probably need to reverse engineer with Ghidra, but I will most definetely not go to those lengths, so I just used *strings* on it, which worked out

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ strings hello_1577977122465.hello
/lib64/ld-linux-x86-64.so.2
libc.so.6
puts
printf
__cxa_finalize
__libc_start_main
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
u/UH
[]A\A]A^A_
THM{****_****_****_**} <- THIS IS THE FLAG
Hello there, wish you have a nice day
;*3$"
GCC: (Debian 9.2.1-21) 9.2.1 20191130
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.7447
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
hello.c
__FRAME_END__
__init_array_end
_DYNAMIC
__init_array_start
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
skip
_ITM_deregisterTMCloneTable
puts@@GLIBC_2.2.5
_edata
printf@@GLIBC_2.2.5
__libc_start_main@@GLIBC_2.2.5
__data_start
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_csu_init
__bss_start
main
__TMC_END__
_ITM_registerTMCloneTable
__cxa_finalize@@GLIBC_2.2.5
.symtab
.strtab
.shstrtab
.interp
.note.gnu.build-id
.note.ABI-tag
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.dynamic
.got.plt
.data
.bss
.comment
```

### Task 7 - Another decoding stuff

```
3agrSy1CewF9v8ukcSkPSYm3oKUoByUpKG4L
```

I assume this is some other binary-to-text encoding scheme. Apparently it isn't base64 though, but it can't be base32 either. I'm seeing values but no 0's or capital i's, which is a huge hint for base58. Decoding time.

<img width="917" height="601" alt="Bildschirmfoto vom 2025-09-25 18-55-27" src="https://github.com/user-attachments/assets/fc772e52-23cf-425d-a96d-436d869a67da" />

And bye.

### Task 8 - Left or right

```
MAF{atbe_max_vtxltk}
```

Looks very much like shifting. The task itself already mentioned ROT, but said ROT13 would be too mainstream. Alright then.

<img width="1811" height="408" alt="Bildschirmfoto vom 2025-09-25 19-01-53" src="https://github.com/user-attachments/assets/2242578a-bc91-402d-860d-2764b66f82fe" />

Turns out it was Caesar cipher.

### Task 9 - Make a comment

This one was especially confusing to me at the beginning, as no downloadable file or ciphered or encoded text was given. Only the title gave it away to me, even though I took my time with this one. I checked the Inspector.

<img width="1851" height="496" alt="Bildschirmfoto vom 2025-09-25 19-22-09" src="https://github.com/user-attachments/assets/cce049ea-a42e-471b-8551-ca09b2e8a8d3" />

### Task 10 - Can you fix it?

Now we had a png that was not displaying a picture properly. The hint itself gave away that we would need to check the PNG file header. After some research I found out that a PNG file starts with an eight-byte signature: 

<img width="659" height="377" alt="image" src="https://github.com/user-attachments/assets/b62660f2-eaaf-4249-998e-e374f44f2d8d" />

To make sure that the hex values are aligning we use a Linux command to create a hexdump of said png file.

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ xxd -p spoil.png > newSpoil.png
```

The *-p* flag in the xxd command is used to output the data in a plain (continuous) hexadecimal format without any formatting such as line numbers or addresses. This is useful for creating a simple hexadecimal dump of a file or data stream.

Now we just change the first 8 bytes, to make the png work again.

If we insert that png into CyberChef now, we are able to render the image, which finally contains the flag that we are so desperately seeking for

<img width="1428" height="920" alt="Bildschirmfoto vom 2025-09-26 00-07-17" src="https://github.com/user-attachments/assets/f4bfc019-300b-4328-ab83-64d44e867007" />

### Task 11 - Read it

To be honest, I had difficulties finding the necessary social accounts. There probably was a faster way to get this flag, but I checked through twitter, discord and finally reddit. There I just wrote the name of the room into the searchbar and got the following result

<img width="805" height="871" alt="Bildschirmfoto vom 2025-09-25 19-44-37" src="https://github.com/user-attachments/assets/35dcef49-a730-4d21-b26d-aa497fa8a706" />

Maybe there is an easier way to do this, but it worked well enough, so whatever.

### Task 12 - Spin my head

Here we have this code snippet (?)

```
++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++++++++++++++.------------.+++++.>+++++++++++++++++++++++.<<++++++++++++++++++.>>-------------------.---------.++++++++++++++.++++++++++++.<++++++++++++++++++.+++++++++.<+++.+.>----.>++++.
```

After some thorough research I realized this is an esoteric programming language called "Brainfu*k". In this programming language a minimalistic set of commands, represented by eight symbolds is used. I will not bother trying to figure out how this language works... yet. I threw it into a decoder and got the flag.

<img width="1213" height="375" alt="Bildschirmfoto vom 2025-09-25 21-51-07" src="https://github.com/user-attachments/assets/8c7da7a8-714b-4276-94b3-17e6c4e46269" />

### Task 13 - An exclusive!

This time we have two separate strings

```
S1: 44585d6b2368737c65252166234f20626d
S2: 1010101010101010101010101010101010
```

If we XOR these, maybe we can find out some interesting output.

<img width="567" height="469" alt="Bildschirmfoto vom 2025-09-25 21-56-32" src="https://github.com/user-attachments/assets/f6b5bd49-9588-487e-9894-65f758bded4c" />

In more difficult tasks I would assume this could get tricky if we dont know the type of inputs we had, but as both were hexadecimal, we only had to convert the output into ascii.

### Task 14 - Binary walk

The downloaded file that we have to check is a jpg this time

<img width="1012" height="682" alt="Bildschirmfoto vom 2025-09-25 22-03-53" src="https://github.com/user-attachments/assets/db67ac0e-cef0-4eaf-8e04-310b97fad2da" />

It's called hell... okay then. There was nothing that I found through the Stegano Decoder or StegOnline, so it was time to make use of binwalk.

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ binwalk -e "hell.jpg"

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.02
30            0x1E            TIFF image data, big-endian, offset of first image directory: 8
265845        0x40E75         Zip archive data, at least v2.0 to extract, uncompressed size: 69, name: hello_there.txt
266099        0x40F73         End of Zip archive, footer length: 22
```

A zip file was exfiltrated succesfully after analyzing the binary file. Checking it out reveals a txt file.

<img width="735" height="469" alt="Bildschirmfoto vom 2025-09-25 22-09-00" src="https://github.com/user-attachments/assets/2cea847b-190f-48b8-9616-e47c05a8a35c" />

### Task 15 - Darkness

The downloadable file contains a picture of something that is presumably just black.

<img width="1010" height="347" alt="image" src="https://github.com/user-attachments/assets/92fb326c-e775-41ea-b881-fa1d7549bfe9" />

But nothing is as it seems. Let's prove it with StegOnline. When we decide to use LSB Half we can see a hidden flag. In this method, the least significant bits of the color values (such as RGB) of pixels are manipulated to encode hidden information, such as text or other data.

<img width="1018" height="775" alt="Bildschirmfoto vom 2025-09-25 22-13-51" src="https://github.com/user-attachments/assets/bb4a388a-d7bd-4bd6-9fef-d5f8cab7ee12" />

 ### Task 16 - A sounding QR

 Once again we are confronted with a QR-code. This time a bot is saying out loud the flag and we have to comprehend what exactly is being said. I had a lot of difficulties understanding what exactly was being said. Thankfully one commenter gave it away or else I would have struggled with this one for much longer or even tried some other bot recognition tool. 

 <img width="1199" height="375" alt="image" src="https://github.com/user-attachments/assets/dd51927c-6401-4a5d-a250-2be7eee94808" />

### Task 17 - Dig up the past

This time we make use of the Wayback machine to retrieve a flag. We are given a targetted website and the targetted time to dig in the past

```
Targetted website: https://www.embeddedhacker.com/
Targetted time: 2 January 2020
```

<img width="1778" height="799" alt="image" src="https://github.com/user-attachments/assets/c0352e8c-c589-4d3d-b3bc-6be21e052d4a" />

That seemed to have worked out. After hovering through that page we can also see an interesting flag

<img width="742" height="250" alt="Bildschirmfoto vom 2025-09-25 22-45-22" src="https://github.com/user-attachments/assets/398c8f7e-e05f-4db6-a7a6-18724d5d7c03" />

Perfect.

### Task 18 - Uncrackable

We are given a Ciphertext this time around and need to figure out the right key, to receive the deciphered text. The encrypted alphabetic text is

```
MYKAHODTQ{RVG_YVGGK_FAL_WXF}
```

Through polyalphabetic substitution this Ciphertext could have been produced by Vigenère Cipher. With *dcode.fr* we were able to get an overview with many different possible key values.

<img width="790" height="694" alt="Bildschirmfoto vom 2025-09-25 22-56-30" src="https://github.com/user-attachments/assets/0c5c7f0b-70b5-471a-9c09-3e104cc70b09" />

The right key was THM. Figures.

### Task 19 - Small bases

Yet again another base encrypted value.

```
581695969015253365094191591547859387620042736036246486373595515576333693
```

Now for this one we had to do several convertings to get to the result we wanted. First we go from decimal to hex and from hex then finally to ascii. The reason as to why we have to do that is because hexadecimal representation aligns more closely with how data is structured and stored in memory. This process helps ensure that data is accurately interpreted and manipulated, especially when dealing with binary files or low-level data formats.

1. Decimal to Hex

<img width="508" height="410" alt="Bildschirmfoto vom 2025-09-25 23-12-42" src="https://github.com/user-attachments/assets/48a3c35d-5f5e-47a2-a4f4-e06fd0f1d718" />

2. Hex to ASCII

<img width="616" height="668" alt="Bildschirmfoto vom 2025-09-25 23-13-59" src="https://github.com/user-attachments/assets/7ecd2921-d05b-4638-8be1-c783ba0884f6" />

### Task 20 - Read the packet

Now for this final flag we need to check out some capture packets. For now we tried to filter the packets to *http.request.method=="GET"*, which allows for isolating and analyzing only the GET requests made during the communication. This is useful because GET requests are often used to retrieve data, such as web pages or resources, and are likely to contain valuable information, including the potential flag. And if we check the only packet that is revealed after the filtering 

<img width="1850" height="88" alt="Bildschirmfoto vom 2025-09-25 23-41-58" src="https://github.com/user-attachments/assets/9fb12cc8-498b-4d72-9064-b5f370cf3c7d" />

Now when checking the HTTP stream, the flag is immediately revealed to us.

<img width="923" height="582" alt="Bildschirmfoto vom 2025-09-25 23-45-02" src="https://github.com/user-attachments/assets/1a5985d1-78d8-4f3f-91d7-faad0155cf2a" />

This marks the final task of this challenge. It was very entertaining and valuable at the same time. I can only hope that I will soon be able to make use of what I learned today.
