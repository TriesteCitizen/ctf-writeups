<h1 align="center">Challenge 053 - Confidential </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/62aad423-1e01-4a9a-957b-a0d6c8dacfcb" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 18.11.2025 </p>

We got our hands on a confidential case file from some self-declared "black hat hackers"... it looks like they have a secret invite code available within a QR code, but it's covered by some image in the PDF! If we want to thwart whatever it is they are planning, we need to help to uncover what the QR code says! And indeed when starting the machine we can see the following document:

<img width="786" height="845" alt="grafik" src="https://github.com/user-attachments/assets/691d9c2b-f6b3-4e31-ae06-e2f97c7309e2" />

There needs to be a way to remove the image. At first I thought of using PDF editing tools to remove or hide images in a PDF file. Software like Adobe Acrobat or free tools like PDFsam could help with that, but it was evident pretty quickly that the virtual machine would only have a limited amount of resources as Firefox was not working here. I instead settled on opening the document with the LibreOfficeDraw software and was quickly able to remove the image from the QR code.

<img width="316" height="498" alt="grafik" src="https://github.com/user-attachments/assets/aae06e9d-5607-4d35-bf49-c706ecc26aa7" />

Now I just needed to scan the QR code with my phone and I would successfully receive the flag.

<img width="356" height="237" alt="Bildschirmfoto vom 2025-11-18 10-59-03" src="https://github.com/user-attachments/assets/bba1a5c1-5e7c-400f-835a-5692e9661e61" />

And with only that we got the solution. It wasn't that hard. I'm sure there are several other ways we can solve this problem. Maybe I can get back to this if I ever get another idea on how we could fix this.

## Lesson Learned
We learned how to focus on manipulating PDF documents to reveal obscured elements like QR codes. This involves using PDF editing tools - like in this case LibreOfficeDraw - and understanding how to analyze file layers effectively.
