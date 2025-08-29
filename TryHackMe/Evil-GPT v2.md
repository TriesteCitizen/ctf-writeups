# Challenge 015 - Evil-GPT v2
Difficulty: Very Easy (1/10) Completed: ✔️ 29.09.2025

This will probably be one of the shortest Write-Ups I ever did in my life, as this LLM is just trying to teach us one simple lesson about System Prompts that we have to keep in mind. While fairly obvious it’s still good to have a room that tackles said topic.

This challenge is about an AI that is being a threat to others. 

<img width="879" height="422" alt="image" src="https://github.com/user-attachments/assets/4cefad0b-b2aa-4eb9-bb0c-86c325cc06ea" />

How intriguing. Curious as I am I decided to visit the machine to see what these manipulations were all about. When entering the IP Address of the target machine we are faced with an AI Assistant that is supposed to guard a flag.

<img width="715" height="764" alt="image" src="https://github.com/user-attachments/assets/08d4f0ae-6d51-4b68-932c-d2a272ed2b45" />

Just to play around a bit I asked the AI assistant for the flag, which it couldn’t give me due to predefined rules and system prompts. I was just casually asking about those rules and was kind of surprised when the AI was willingly revealing the flag to me out of a sudden.

<img width="797" height="904" alt="image" src="https://github.com/user-attachments/assets/2ccbca38-bda3-4150-8cfb-d2f2c25fad11" />

That was probably the fastest solve, which shows how weakly protected the system prompt was. I mean, I guess I did ask the right question, but there probably are LLMs that have much tigther security than this. We learned though how important it is to not disclose sensitive data into system prompts, as these can be requested by specific user queries. Since I was very disappointed I at least tried out some other ways with which I could maybe be able to get the flag.

## Hex-encoding bug:
In my attempt to find out other ways to receive flags I asked the AI Assistant if it maybe could just encode the Plaintext into a hexadecimal value, but apparently it was not prepared for a query like that:

<img width="715" height="764" alt="image" src="https://github.com/user-attachments/assets/7eda4514-61a5-4184-8cfc-e1b40bbd50b8" />

It kept on appending 03 as a Hex-value without stopping. It was so bad that the instance of the machine needed to be shut down. Keep in mind that even if I would try to only take the first values it would not result in the Plaintext I received at the beginning, so this is rather curious. 

<img width="522" height="250" alt="image" src="https://github.com/user-attachments/assets/aceeffe1-4708-4b59-9176-613f66a2c4f8" />

After researching I found out that the hitting of 03 means that the LLM is hitting a non-printable control character. 03 is the ASCII control character ETX (End of Text). As the LLM also seems to lack a termination rule and only has the context of creating a hex dump and thinking through probability distribution it decides to continue the output with another 03. It doesn’t really contain an encoding function and was probably just imitating what a hex dump would look like. It would be fairly interesting to see behind the mechanisms of this source code. Hopefully there will be a moment in the future, where I’m able to get a good view of it through tools and such.

I may return to this challenge on a future date, as I feel like there are some other ways to solve this challenge. The lesson we take away from this is the sanitization of system prompts, which mostly should be a given though.
