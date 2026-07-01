<h1 align="center">Challenge 067 - Digital Footprint </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/7f0e05fa-6793-4dcc-a58c-c29b6f354df3" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

I just can't get enough from OSINT challenges. I'm on a roll so let's just go for another one of them.

### The Leaked Photo
An ACME Jet Solutions employee uploaded a photo of a residential property believed to be linked to ACME Jet's early operations. Can you figure out where the picture was taken to confirm or debunk the rumour? 

Here a look at the reference picture

<img width="1302" height="831" alt="grafik" src="https://github.com/user-attachments/assets/c2be6e84-8ab7-4e5b-a6af-ad62a5dca763" />

We make another Reverse Image Search.

Initially I relied on the AI answer, which assured me this was Bathurst, Eastern Cape, South Africa. That wasn't the case though.

<img width="692" height="632" alt="grafik" src="https://github.com/user-attachments/assets/9fef22d8-8355-4590-a374-4ba723363337" />

Apparently the AI combined the small plaque text ("The Rectory") with the South African visual markers and hallucinated an association with a different historical building in Bathurst. 

We might be able to figure out the exact coordinates via a metadata tool like the exiftool.

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ exiftool edited-house-1763031553617.jpg
ExifTool Version Number         : 12.40
File Name                       : edited-house-1763031553617.jpg
Directory                       : .
File Size                       : 774 KiB
File Modification Date/Time     : 2026:06:30 18:41:31+02:00
File Access Date/Time           : 2026:06:30 18:42:03+02:00
File Inode Change Date/Time     : 2026:06:30 18:41:31+02:00
File Permissions                : -rw-rw-r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
Exif Byte Order                 : Big-endian (Motorola, MM)
GPS Latitude                    : 26 deg 12' 14.76"
GPS Longitude                   : 28 deg 2' 50.28"
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Image Width                     : 1306
Image Height                    : 837
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:4:4 (1 1)
Image Size                      : 1306x837
Megapixels                      : 1.1
GPS Position                    : 26 deg 12' 14.76", 28 deg 2' 50.28"
```

Now when we convert Degrees, Minutes, Seconds (DMS) into Decimal Degrees (DD) we are able to use those coordinates to figure out the possible destination. 
- Option 1: North & East: The middle of the desert in Saudi Arabia. There are no residencial properties or "ACME Jet" corporate operations there.
- Option 2: North & West: The middle of the North Atlantic Ocean (thousands of miles away from any land).
- Option 3: South & West: The middle of the South Atlantic Ocean (completely underwater).
- Option 4: South & East: Downtown Johannesburg, South Africa.

<img width="1204" height="809" alt="Bildschirmfoto vom 2026-07-01 10-17-42" src="https://github.com/user-attachments/assets/754f7327-d12d-4e46-b4c5-765d063d4d47" />

Directly on top of a major skyscraper and commercial district.

<img width="1292" height="961" alt="grafik" src="https://github.com/user-attachments/assets/ba3e38c3-ff35-499f-ab22-c289dcb7c19d" />

That is my best guess and it seems I was right.

### Archived Company Website
ACME Jet Solutions (warc-acme.com/jef/), is all over social meda claiming they were founded in 2025 and that they're the fastest-growing data company in Africa.
But something doesn't add up, one of their ex-employees ensures you that the company existed long before that.

Your job as an investigator is to verify their founding date using only public information.

