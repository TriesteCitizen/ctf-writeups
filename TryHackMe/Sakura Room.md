<h1 align="center">Challenge 030 - Sakura Room </h1>
<p align="center">
  <img width="90" height="90" alt="Bildschirmfoto vom 2025-09-30 18-58-37" src="https://github.com/user-attachments/assets/3b2b2e0a-64f4-478b-8496-47e6a4daa3b4" />
</p>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️  </p>

This room is specialized to train our OSINT (Open Source Intelligence) techniques. Most beginners are apparently able to solve these challenges. For this a sample OSINT investigation will take place in which we will be asked to identify a number of identifiers and other pieces of information in order to help catch a cybercriminal. Without further ado I will get started

### TIP - OFF
The background is that the OSINT Dojo found themselves victims of a cyber attack. While there were no clear indications of major damages or indicators of compromise on any of their systems, forensic analysis found an image left behind by the cybercriminals. It looks like this

<img width="429" height="647" alt="Bildschirmfoto vom 2025-09-30 19-11-22" src="https://github.com/user-attachments/assets/f81025d7-a2e8-479e-979a-49b766495334" />

We are adviced to analyze the metadata to get a hold of the username of the attacker. When inspecting the picture of the .svg (Scalable Vector Graphic) we are able to copy the binaries that are displayed on the picture. 

<img width="1147" height="174" alt="Bildschirmfoto vom 2025-09-30 20-58-36" src="https://github.com/user-attachments/assets/7592eb4d-557b-485c-a9a7-e82030dc9d70" />

When putting them into a Binary-to-Text Converter we receive the following message.

<img width="601" height="657" alt="Bildschirmfoto vom 2025-09-30 21-00-30" src="https://github.com/user-attachments/assets/4379ed52-dae5-40c1-90d6-1f61329f7149" />

True that. This doesn't really help us get the information of the attacker though. Further inspecting clearly shows us the username though. We can alternatively use *metadata2go* as a tool to analyze the URL, which leads to the same results. Just insert the URL in the search bar

<img width="1147" height="536" alt="Bildschirmfoto vom 2025-09-30 21-48-01" src="https://github.com/user-attachments/assets/1ca6f6f0-4663-4879-851c-9912386f7590" />

After a little bit of time we are able to see the owner of this picture under the label *export-filename*

<img width="659" height="58" alt="Bildschirmfoto vom 2025-09-30 21-49-22" src="https://github.com/user-attachments/assets/d9821705-dc93-4f46-a100-8233fb2da830" />

### RECONNAISSANCE

In the second task we get informed that the attacker made the mistake of reusing his username in different social media platforms. Additional information can be gathered that way and indeed, when searching for his username we promptly get a hold of his Twitter, Instagram and GitHub. In his Twitter we also get the possibility of finding out his real name

<img width="607" height="139" alt="Bildschirmfoto vom 2025-10-01 10-46-30" src="https://github.com/user-attachments/assets/7ab7b532-0f9c-4c94-993e-c7ae1cae7cee" />

For the information of his email we have to dig a bit deeper. In his Github account we spot a repository called pgp keys

<img width="1289" height="528" alt="Bildschirmfoto vom 2025-10-01 11-21-52" src="https://github.com/user-attachments/assets/fa9c9ecc-4e76-4298-9139-54a5ca74bcc0" />

Could be a clue. In here we have encrypted messages, which can easyily be decrypted with the right tools

<img width="1175" height="894" alt="Bildschirmfoto vom 2025-10-01 11-25-22" src="https://github.com/user-attachments/assets/035d6385-3791-444a-849d-8680baa7db10" />

There is the email. Very good.

### UNVEIL

Now the cybercriminal is on to us. As we are investigating his GitHub account indicators are observed, where the account owner had begun editing and deleting information in order to throw us off his trail. He likely removed those information because it contained some sort of data that would add to our investigation. Is there a way to retrieve those information? The answer is yes. With the Wayback machine we can take care of all these problems.

<img width="1847" height="945" alt="image" src="https://github.com/user-attachments/assets/28023744-5aec-4b62-ac85-7d8c071a3b71" />

After jumping to a prior state of the site we see that he has a digital (ETH) wallet to store, send and receive Ethereum, which answers the first question.

For the second question, which asks us to find out the attackers cryptocurrency wallet address the number of Commits for his ETH wallet turn interesting. After checking out the first commit, we find the necessary information

<img width="1831" height="407" alt="Bildschirmfoto vom 2025-10-01 12-33-14" src="https://github.com/user-attachments/assets/e4432911-16db-45b9-aeb3-3abc83565750" />

In the next question we are asked what mining pool the attacker received the payments from on January 23, 2021 UTC. For that we just need to insert the blockchain address to the URL and click on the first link, which is a website for tracking all Ethereum related traffic.

<img width="874" height="607" alt="image" src="https://github.com/user-attachments/assets/36fba7ee-1f2e-45ac-9f95-5f928440556d" />

Now we check for the right date and voila

<img width="1352" height="68" alt="image" src="https://github.com/user-attachments/assets/7b2235b5-39ba-42ee-934d-a30d2fb09a8e" />

We found the right transaction. Now we check for further information and find out the mining pool the attacker received payments from.

<img width="900" height="610" alt="Bildschirmfoto vom 2025-10-01 13-02-11" src="https://github.com/user-attachments/assets/e3969a32-aebc-4d87-b314-742b426361c5" />

Now when checking the other transactions we quickly see that the attacker used another cryptocurrency for exchanges.

<img width="1355" height="48" alt="Bildschirmfoto vom 2025-10-01 13-09-34" src="https://github.com/user-attachments/assets/c8e0659f-140c-4378-a1e8-21cc9fe1bddd" />

Settled and done.

### TAUNT

It seems like the cybercriminal is fully aware that informations are gathered about him after the attack. 

<img width="441" height="309" alt="Bildschirmfoto vom 2025-10-01 13-15-15" src="https://github.com/user-attachments/assets/e0639ed4-c8d1-45d8-9c50-eaf77aa89d6c" />

He mad. As he should honestly.

In the instructions we are informed about the fact that users sometimes can have alternative accounts that they keep entirely separate. There could be some additional infos that we may were not able to see before. Something to keep in mind.

At the same time the first question still is very straightforward as we are asked about the attacker's current Twitter handle. I'm pretty sure we saw that one before, but here we go again.

<img width="599" height="291" alt="Bildschirmfoto vom 2025-10-01 13-39-09" src="https://github.com/user-attachments/assets/47c5911d-5bf1-4914-acc6-6388a9980139" />

The next question was to find out what the BSSID (Basic Service Set Identifier) for the attacker's home wifi is. For that we had to keep checking the twitter account to see the following tweet

<img width="599" height="341" alt="image" src="https://github.com/user-attachments/assets/888578d6-cc52-424d-a670-e7480d31b7e6" />

Another tweet further hints at what kind of tool can be used to find the BSSID.

<img width="599" height="181" alt="image" src="https://github.com/user-attachments/assets/688712f2-37f9-4696-ba08-c34ee2155e22" />

The capitalized words might be a hint. We check for Deep Paste
