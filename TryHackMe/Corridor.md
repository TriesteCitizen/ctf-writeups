<h1 align="center">Challenge 002 - Corridor </h1>
<p align="center">
  <img width="90" height="90" alt="Bildschirmfoto vom 2025-09-18 18-06-37" src="https://github.com/user-attachments/assets/a79dbef4-79b9-4df7-8af4-03ffe8a91445" />
</p>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 16.08.2025 </p>

This time we have the following challenge:

<img width="1069" height="134" alt="grafik" src="https://github.com/user-attachments/assets/248ecc7a-888c-44b2-a980-3338e4dc2155" />

This task has to do with IDORs so I assume that there will be some sort of encrypted Hash in the URL or Page Source, which we have to decode with some tools. So to start we just write the target IP Address in the URL. The website itself interestingly only consists of a corridor picture.

<img width="1339" height="901" alt="grafik" src="https://github.com/user-attachments/assets/db3834da-3f78-42e1-9b3b-edfd9a4e4ee2" />

When clicking on one of the doors it displays another static page, that displays an empty room this time around. All of the doors are empty and display the same picture when clicking on them, but they all append some sort of hash on the URL, which immediately shows a vulnerability that we can abuse.

<img width="1345" height="908" alt="grafik" src="https://github.com/user-attachments/assets/e0397b96-0bd7-48a0-85a2-c6c9072055e3" />


I wanted to check the Page Source, but I did not even need to do that. I just took the hash and threw it into a decoder to see if it could recognize if this maybe was some sort of base64 encoding.
It wasn’t, but it was an md5 hashing algorithm, so I immediately checked what value these hashes could correspond to by visiting 10015.io.

<img width="1345" height="908" alt="grafik" src="https://github.com/user-attachments/assets/7552e30c-acaf-4fdd-8dd9-8a3542c00493" />

One of the rooms corresponded the value 8. So I just experimented what would happen if I would try to encrypt value 1 or even 0 and append it to the URL. Encrypting 1 didn’t lead to any worthwhile results. 0 on the other hand was the solution that lead me to the flag. 

<img width="1345" height="908" alt="grafik" src="https://github.com/user-attachments/assets/a91c38e0-ea9d-41f7-bd2c-92c678523eb7" />

Surprinsingly this was the fastest flag I received as of now. This time I really only took around 5 minutes, so this is a win for me.

What did I learn from this? Unfortunately not much. IDOR vulnerabilities are very straightforward and are easily spottable. If some industry uses them. Run. Obviously I realized how vulnerable md5-hashed IDs are, and that you should think twice before using them for your website. I guess I need to try to tackle more challenging tasks next time around to really have some learning effect.
