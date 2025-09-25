<h1 align="center">Challenge 027 - CTF collection Vol.1 </h1>
<p align="center">
  <img width="90" height="90" alt="Bildschirmfoto vom 2025-09-25 18-10-02" src="https://github.com/user-attachments/assets/c6ac29ba-2fdc-4275-a12d-de7ea44008ad" />
</p>
<p align="center"> <b>Difficulty</b>: ???/10 <b>Completed</b>: ✔️  </p>

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

Now we had a png that was not displaying a picture properly. 

### Task 11 - Read it

To be honest, I had difficulties finding the necessary social accounts. There probably was a faster way to get this flag, but I checked through twitter, discord and finally reddit. There I just wrote the name of the room into the searchbar and got the following result

<img width="805" height="871" alt="Bildschirmfoto vom 2025-09-25 19-44-37" src="https://github.com/user-attachments/assets/35dcef49-a730-4d21-b26d-aa497fa8a706" />

Maybe there is an easier way to do this, but it worked well enough, so whatever.

