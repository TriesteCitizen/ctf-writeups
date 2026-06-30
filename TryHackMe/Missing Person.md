<h1 align="center">Challenge 066 - Missing Person </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/1ef40636-d897-41e9-aecc-a6bbfd0c2e1f" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 2/10 (Easy) <b>Completed</b>: ✔️ 30.06.2026 </p>

I felt like doing something where I had to use my OSINT skills once again. These are always fairly entertaining too. Here we have to help the police track down a person

## OSINT
"My friend went on holiday in 2025 and shared some photos, but I haven't heard from him since. Can you help me track him down for the police report?"

There is an attached zip file with two photos with which we can start the investigation. The first photo *food.jpg* shows the following.

<img width="1365" height="769" alt="Bildschirmfoto vom 2026-06-30 12-35-21" src="https://github.com/user-attachments/assets/28b153c6-90d8-416c-aa23-b58b648304d9" />

Seems to look a lot like some kind of food hall with colorful papel picado banners and tables.

In the second picture named *MotoPG.jpg* we see a street with a sign that says "Pertamina"

<img width="956" height="532" alt="grafik" src="https://github.com/user-attachments/assets/859915b6-1ed6-418f-9c58-6ed20754a0c1" />

A quick Google search tells us that Pertamina is the Indeonesian state-owned integrated energy corporation headquarted in Jakarta. We can assume with a high confidence that the friend went to Indonesia for his vacation.

### What is the commercial name of this circuit?
I did the lazy thing and just did a Reverse Image Search for the first image. Frankly I was quite confused by the question since I didn't understand which circuit the task was referring to. I have no knowledge of motorsports or their area. At least I found out the location the first picture was taken in.

<img width="1168" height="843" alt="grafik" src="https://github.com/user-attachments/assets/5a889a6b-455b-4d97-bdf8-c72e349af0b3" />

Now with that knowledge in mind I searched for circuits in Kuta Lombok.

<img width="1043" height="538" alt="Bildschirmfoto vom 2026-06-30 13-20-10" src="https://github.com/user-attachments/assets/33efaa66-583a-4da1-81a2-423bbd1145b9" />

I succesfully spotted the name. Thanks Google.

### When did the event take place?
This is fairly easy to figure out. We already know from the task, that the friend went into his holidays on 2025. Now when doing a Google search we ask for the concrete circuit dates in Kuta, Lombok. An Instagram post gives us the answer.

<img width="983" height="725" alt="grafik" src="https://github.com/user-attachments/assets/98583ea6-84fe-44f0-a6ce-4352866bcd62" />

### He told me he ate delicious Mexican food. What is the name of the restaurant?
This question was already answered beforehand. Check the information on the restaurant we are given when doing a Reverse Image Search.

### At what time was this photo taken?
To find that out we just unpack the zip folder and check the properties of the jpg files.

<img width="564" height="194" alt="grafik" src="https://github.com/user-attachments/assets/cb695096-d14f-4be3-9f0c-1e487761b93f" />

There we go.

### He sent me a message, this is the last I heard from him: ”Went to this cool MotoGP after party, and became friends with one of the local DJs who played that night. We’re going to visit a cave tomorrow.”
### What is the full address of the bar’s location?

I did another Google search:

<img width="1323" height="479" alt="grafik" src="https://github.com/user-attachments/assets/0eb15434-8397-4fe6-aa6e-edc36b1fc097" />

When clicking on the link that the AI answer is referring to we get a hint in form of a Surfers Bar.

<img width="1431" height="566" alt="grafik" src="https://github.com/user-attachments/assets/664e73e8-cd89-4fd2-ae34-7e063e277caa" />

By checking out the full address of said space we find the answer to our question.

<img width="491" height="653" alt="grafik" src="https://github.com/user-attachments/assets/592ce6df-4900-48a0-ba85-f21bcdec4bc4" />

### What is the DJ's stage name?
After reading the question I remembered the Facebook post and thought the advertisement might give us some other clues.

<img width="916" height="497" alt="grafik" src="https://github.com/user-attachments/assets/c3a3ffdf-54f0-4935-9166-fb1e76912c99" />

Seems like I had the right intuiton.

### After digging into the DJ's other online accounts, what cave does he take tourists to?
It looks like we have to check out Bong Lelehs socials. When we check out his instagram posts we can see that the geographic location for a lot of those individual posts is set to Gua Sumur. 

<img width="997" height="559" alt="grafik" src="https://github.com/user-attachments/assets/9f1f2a6b-c967-480e-933c-205061302b63" />

### What number did the DJ list for his tour business?
This was definetely the most challenging thing to find out. I checked his socials until I stumbled upon a facebook page that was looking like a tour business site. It referenced the same cave and the URL is connected to the DJs label.

<img width="1787" height="847" alt="grafik" src="https://github.com/user-attachments/assets/be2de391-db2e-4f5c-98e7-21a971be03b6" />

Removing the indonesian phone prefix finally give us the right answer.

### Lesson Learned
OSINT challenges are always rewarding the thinking out of the box. This also applied here. You had to consider all the hints given and connect all the possible dots. The importance on relying on socials from involving actors was very evident in here. Google is your friend and don't be ashamed to consider the AI generated answers and web pages, so long as they don't reference other write ups of this challenge ;)

