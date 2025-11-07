<h1 align="center">Challenge 049 - Ninja Skills </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/5f0c4466-0d63-4da5-b7d6-77c6a7c5c48c" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

This is a box where we will have the opportunity to practice our Linux skills. The following files will be important for the following task

 - 8V2L
 - bny0
 - c4ZX
 - D8B3
 - FHl1
 - oiMO
 - PFbD
 - rmfX
 - SRSq
 - uqyw
 - v2Vb
 - X1Uy

So before we start we deploy the machine 

<img width="879" height="187" alt="grafik" src="https://github.com/user-attachments/assets/4f475cad-a2fc-4651-a5cc-d5841857c344" />

and proceed to check out the files directory that we can see when ls'ing.

<img width="544" height="139" alt="grafik" src="https://github.com/user-attachments/assets/3a58bfe5-26a7-4510-b008-62e1c7d206a9" />

As we can see the files don't seem to reside at the right place, so we look up the current location of the first file

```
[new-user@ip-10-10-215-87 ~]$ find / -name 8V2L 2>/dev/null
/etc/8V2L
```

Target spotted. I thought analyzing it thoroughly would be efficient but after some time I realized that using find with the combination of the group flag would help better in answering the first question.

```
[new-user@ip-10-10-215-87 ~]$ find / -group best-group 2>/dev/null
/mnt/D8B3
/home/v2Vb
```

For the next one we had to find out which of the files contained IP-addresses. There may be a way to automatate that whole process but my regex skills are not that good, so I just pivoted to find the locations of all files to then check them all out. Don't judge.
After having done that I can note down that the following files reside in these locations:

```
/etc/8V2L
/mnt/c4ZX
/var/FHl1
/opt/oiMO
/opt/PFbD
/media/rmfX
/etc/ssh/SRSq
/var/log/uqyw
/home/v2Vb
/X1Uy
```

I unfortuantely was not able to find the bny0 file. I doubt that I did any typos so this is peculiar. Having said that let's still try to cat these files in hopes of finding some sort of IP-Address.

After a while this felt very inefficient and I just googled around to figure out the right regex and write a script that would cat the names of the files through a loop and find the corresponding one at the end.

```
[new-user@ip-10-10-13-13 files]$ for i in $(cat filenames); do find / -name "$i" -exec grep -loE "([0-9]{1,3}\.){3}[0-9]{1,3}" '{}' \; 2>/dev/null; done
```

Which spat out the right answer immediately. Sweet.

The next question 

