<h1 align="center">Letter </h1>

<p align="center">
  <img src="assets/letter.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: 2/10 (Easy) <b>Completed</b>: ✔️ 26.08.2026 </p>

This is another OSINT challenge yet again, which are always fun. 

## OSINT time
It's just another Monday morning on our mail delivery route when an unusual letter catches our eye. The envelope is battered, riddled with holes as if it's been through a storm. The address is barely legible and our coworkers at the post office wave it off as a lost cause.

But something about it nags us.

We carefully open the damp envelope. Inside we find a faded newspaper clipping and a short handwritten note. The clipping is torn and water-damaged, with key sections missing. The note is personal, clearly not meant for our eyes, but the fragments we can read hint at a story buried in time.

**Objective**: We have to use the clues provided in the zip file to uncover the full name and age of the person mentioned in the note.

### What is the postal code of the delivery address on the envelope?
After opening the zip file we can see a text file that was written in french.

```
Mon cher Édouard,

Aujourd'hui, en rangeant le grenier chez mes grands-parents, je suis tombée sur cette vieille coupure de journal. Ton arrière-grand-père n'avait même pas l'âge de passer le permis quand il s'est distingué ce jour-là. Le benjamin de l'équipe, et certainement pas le moins courageux.

Il serait si fier de te voir sur l'eau à ton tour.

Avec toute mon affection,
Audette
```

My first approach would be to translate the message. My french isn't that good so I translated it.

```
My dear Édouard,

Today, while cleaning out the attic at my grandparents' house, I stumbled upon this old newspaper clipping. Your great-grandfather wasn't even old enough to get his driver's license when he distinguished himself that day. The youngest of the team, and certainly not the least courageous.

He would be so proud to see you out on the water in your turn.

With all my affection,
Audette
```

The zip file also contains the mentioned newspaper clipping.

<img width="1020" height="397" alt="Bildschirmfoto vom 2026-08-26 12-27-19" src="https://github.com/user-attachments/assets/8ecb58f6-75ab-4f33-84b7-2be533197fc5" />

We also have a png file of the letter itself, which as the description already mentioned, seems very battered and water-damaged.

<img width="1336" height="901" alt="Bildschirmfoto vom 2026-08-26 12-31-05" src="https://github.com/user-attachments/assets/3235a126-7bd2-470e-9665-8d92034fd7ce" />

On the left side there are green symbols for France, a maximum weight of 20 grams as well as the mention  "Délai 3 jours". Below we can see an orange barcode.

In the middle we can assume that "Édouard G." and "SNSM" (Société Nationale de Sauvetage en Mer) is written.

The primary detail we should focus on is the orange barcode. Instead of relying on machines to repeatedly read messy human handwriting at every single transit hub, the first machine prints the barcode. From this point on, laser scanners process the letter in milliseconds, sorting thousands of letters per minute. It's a metadata trail that leaks the exact location we are hunting for.

This internal sorting code applied by the French postal service (La Poste) encodes the exact recipient address (postal code, street and house number).

The code uses a special proprietary system where each digit is represented by a specific combination of long (tall) and short (short) bars. Below an image that clarifies the idea.

<img width="1256" height="102" alt="grafik" src="https://github.com/user-attachments/assets/5073c03d-709e-4240-8cd1-dfcf189cc412" />

Given this information, we can easily deduce the postal code number now. Always consider, that the postal code is read right to left: 29760.

The answer is correct, at the same time the last 0 digit seems to consist of a combination of 7 instead of just 6 bars. The reason for the 7 bars when analyzing the 0 comes down to a technical quirk of the French postal barcode system.

That being that in the French postal barcode, every single digit (when read from right to left) is always preceded by a fixed first bar (lead bar). This serves as a clock pulse generator for the sorting machine, allowing it to reliably detect characters as the letters rush past at extreme speeds. If we visually count this mechanical helper bar along with the actual data bits, we quickly end up with one extra bar for that digit.

### What is the flag?
The flag format is supposed to be THM{Name_Surname_age}. As the letter already reveals the name of recipient we only have to figure out the surname and age now.

As we figured out the postal code we can track it down to the corresponding commune: Penmarch

<img width="1012" height="861" alt="Bildschirmfoto vom 2026-08-26 13-29-22" src="https://github.com/user-attachments/assets/af944e55-6d19-4ae6-ac1e-ae2fa850dc24" />

As the envelope already mentioned Édouard must be in the SNSM station in Penmarch then.

Furthermore the newspaper mentioned some sort of tragedy. We can't really decipher what it's really referring to, so I queried the newspaper for any sort of catastrophes in Penmarch and thankfully found a webpage that gave a lot of insight that might be interesting to us, as it also is referencing the same newspaper.

<img width="1012" height="861" alt="Bildschirmfoto vom 2026-08-26 13-51-47" src="https://github.com/user-attachments/assets/60563831-92b0-46c5-87a4-aa981c4be3d0" />

While reading we were able to get insight about a catastrophic event in Penmarch. A maritime shipwreck and rescues disaster that occurred on Saturday, May 23, 1925, when a violent storm struck the local fishing fleet and subsequently capsized two rescue lifeboats attempting a rescue. In Penmarc'h and across Britanny, it is historically referred to as "La catastrophe du 23 mai 1925" claiming 27 lives, those being:

Crew of the Berceau-de-Saint-Pierre — 7 dead

- Vincent Larnicol
- Pierre Larnicol
- Jacques Biger
- Nona Salaün
- Pierre Stéphan
- Jean Guichaoua
- Jacques Gégou

Crew of the Saint-Louis — 5 dead

- Julien Dupuis, patron
- Jacob Corentin
- Pierre Le Lay
- Henri Tanter
- Pierre Le Floch

Kérity lifeboat, Comte-et-Comtesse-Foucher — 7 dead

- François-Eugène Le Gars
- Thomas Cloarec
- Henri-Marie Jézégabel
- Laurent Coupa
- Henri Kerloch
- Yves-Marie Stéphan
- Pierre-Marie Tanniou

Saint-Pierre lifeboat, Léon-Dufour — 8 dead

- Jean-Marie Berrou, patron
- Vincent-Marie Tanniou
- Pierre Carval
- Jean L'Helgouarch
- Jean Larnicol
- Alain-Marie Calvez
- Laurent Calvez
- Guillaume Cossec

None of them have a surname that starts with 'G' and contains 10 letters. So I moved on to a segment of the article that mentioned the survivors and heroes of this great tragedy.

<img width="1023" height="814" alt="Bildschirmfoto vom 2026-08-26 14-43-18" src="https://github.com/user-attachments/assets/da665859-972e-4a87-87cc-4610c070054d" />

One name in particular seems interesting: Gourlaouen. A perfect fit for our conditions. To find out his age I kept on further browsing the website for other clues and found an article that talked about honoring and rewarding the rescuers who went to save the fishermen.

<img width="1024" height="706" alt="Bildschirmfoto vom 2026-08-26 14-55-28" src="https://github.com/user-attachments/assets/0552a998-5e9d-41ae-9e1b-ca240c5136a0" />

One of them seems to be especially young. Only 15 years of age. This fits perfectly with the information that were mentioned in the letter thus making the name of the flag evident: 
- Name: Yves-Marie
- Surname: Gourlaouen 
- Age: 15 

### Lesson Learned
I learned to look through archives and articles. Keywords that describe great historical disasters and pinpointing a list of actors was very important when trying to figure out the grand scheme of things. I hope to be more efficient next time I have to browse through articles. Furthermore I learned how to decode post barcode from France. It's generally always good to look out for metadata in documents that may be damaged to get other insights.
