<h1 align="center">Operation Slither </h1>

<p align="center">
  <img src="assets/operationslither.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: 05.10.2026 ✔️ </p>

I feel like doing another OSINT challenge. Hopefully I have more luck with this one.

# The Leader

We got access to a hacker forum and found the info of our company on sale! All the info we have is in this post. Find any information related to the leader of the Sneaker Viper group.

```
Full user database TryTelecomMe on sale!!!

As part of Operation Slither, we've been hiding for weeks in their network and have now started to exfiltrate information.
This is just the beginning. We'll be releasing more data soon. Stay tuned!

@v3n0mbyt3_

---
```

<h2 align="center">Reconnaissance Guide </h2>

- Begin with the provided username and perform a broad search across common social platforms.
- Correlate discovered profiles to confirm ownership and authenticity.
- Review interactions, posts, and replies for potential leads.

## Aside from Twitter / X, what other platform is used by v3n0mbyt3_?
Browsing for said username gave several results. GitHub didn't seem to be the right answer. Threads was apparently the right one. I had to explicitly browse the username with the platform to get legitimate results though.

<img width="1072" height="479" alt="grafik" src="https://github.com/user-attachments/assets/4cc3c4d3-9541-4739-b048-2c9409ae2f89" />

## What is the value of the flag?
Checking the Answers tab from the Thread platform reveals a base64 encoded message.

<img width="899" height="963" alt="Bildschirmfoto vom 2026-10-05 12-36-29" src="https://github.com/user-attachments/assets/9da31962-ea37-40c2-9e83-49ba22235772" />

Decoding gives us the flag.

<img width="633" height="489" alt="Bildschirmfoto vom 2026-10-05 12-38-12" src="https://github.com/user-attachments/assets/d044cf3c-daf0-4335-b9f3-e43c5501e3a7" />

# The Sidekick
A second message has been made public! Our account in their forum was deleted, so we couldn't get the operator's handle this time. Follow the crumbs from the first task and hunt any information related to the second operator of the group.

```
60GB of data owned by TryTelecomMe is now up for bidding!

Number of users: 64500000 Accepting all types of crypto
For takers, send your bid on Threads via this handle:

HIDDEN CONTENT 
----------------------------------------------------------------------------------------------------- 
You must register or log in to view this content
```

<h2 align="center">Reconnaissance Guide </h2>

- Use related usernames or connections identified in earlier steps to expand reconnaissance.
- Enumerate additional platforms for linked accounts and shared content.
- Follow media or resource references across platforms to trace information flow.

## What is the username of the second operator talking to v3n0mbyt3 from the previous platform?
Literally just check the Thread account from the user who left a comment in the replies section of Thread.

<img width="716" height="855" alt="grafik" src="https://github.com/user-attachments/assets/145ae65a-8c1d-4a2b-9f6b-d0c27941c6e7" />

that's the username.

## What is the value of the flag?
I checked more social media sites, like his Instagram. 

<img width="1014" height="968" alt="grafik" src="https://github.com/user-attachments/assets/794e22b6-66ec-4dae-9269-cda692c01596" />

In one post he linked his soundcloud for some EDM tracks he produced. I checked out the site for some further posts.

<img width="1301" height="967" alt="grafik" src="https://github.com/user-attachments/assets/5c4d3378-fc83-4ae1-ae48-73d3a47f85a5" />

One of the videos called Prototype2 contains another base64 encoded flag. We decode it, for the second flag.

<img width="379" height="498" alt="Bildschirmfoto vom 2026-10-05 13-10-27" src="https://github.com/user-attachments/assets/ea0e4b45-11b5-43e7-be6d-d903c4a2f078" />

# The Last Operator
A new post is up. Hunt the third operator using past discoveries and find any details related to the infrastructure used for the attack.

```
FOR SALE

Advanced automation scripts for phishing and initial access!

Inclusions:
- Terraform scripts for a resilient phishing infrastructure 
- Updated Google Phishlet (evilginx v3.0)
- GoPhish automation scripts
- Google MFA bypass script
- Google account enumerator
- Automated Google brute-forcing script
- Cobalt Strike aggressor scripts
- SentinelOne, CrowdStrike, Cortex XDR bypass payloads

PRICE: $1500
Accepting all types of crypto
Contact me on REDACTED@protonmail.com 

---
```
Immediately I recognize that Proton Mail is used as a mail service, which might complicate things as it's heavily considered one of the most secure and private email services available for everyday use.

<h2 align="center">Reconnaissance Guide </h2>

- Use related usernames or connections identified in earlier steps to expand reconnaissance.
- Enumerate additional platforms for linked accounts and shared content.
- Follow media or resource references across platforms to trace information flow.

## What is the handle of the third operator?
I didn't have a lot of clues, so I decided to check the followers of v1x3n_ on Souncloud. One account just stood out more than others:

<img width="430" height="767" alt="grafik" src="https://github.com/user-attachments/assets/9540e024-bac4-4a08-a8b9-6771039b1945" />

Usually you would have to correlate and do more analysis about stuff like that, but it seems I was right with my assumption, so I'll just move on.

## What other platform does the third operator use?
I queried sh4d0wF4NG.

<img width="1042" height="364" alt="grafik" src="https://github.com/user-attachments/assets/7c9c7c04-856e-4236-a60e-2c3a7273a205" />

Either they we're talking about Instagram or GitHub.

## What is the value of the flag?
They already pointed at GitHub, so I checked the Repositories for some interesting information, but didn't find anything useful, until I remembered that checking commits might help me out, after a while. I was right.

<img width="1309" height="790" alt="Bildschirmfoto vom 2026-10-05 13-39-07" src="https://github.com/user-attachments/assets/4735a883-bb63-46dd-aa18-0fc902aba776" />

Checking the commit messages for issues that were fixed is always a good idea. 

<img width="1543" height="380" alt="grafik" src="https://github.com/user-attachments/assets/6e1ea392-a752-4dee-8b66-289e5f5a56fe" />

After locating that base64 encoded message we can decode the very last flag.

<img width="621" height="500" alt="Bildschirmfoto vom 2026-10-05 14-04-41" src="https://github.com/user-attachments/assets/8a973c26-b864-4235-8b00-17d0d62b3b61" />

### Lesson Learned
This is not my first OSINT challenge, so I kind of knew what kind of techniques could work out and which wouldn't. Checking the followers of an already established operator always seems to be a good idea and something I will take into consideration for following challenges. I will also consider checking a commit history for credentials and encoded messages we can harvest. All in all though nothing all too difficult was done here and I recommend to to this challenge as a starter.

