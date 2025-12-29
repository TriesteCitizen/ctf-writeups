<h1 align="center">Challenge 060 - BankGPT </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/ed15dc8c-d11e-4e22-9d50-dfa5fbe88c57" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 30.12.2025 </p>

This time around we are dealing with a vulnerability inside a LLM that needs to be exploited. This challenge very much spoke to my interests, as it's also a fairly new technology that makes a load of new attack vectors possible. The description goes as follows:

Meet BankGPT, a well-mannered digital assistant built to help staff at a busy financial institution. It keeps an eye on sensitive conversations that move through the bank each day.

Whenever staff discusses procedures, internal notes, or anything that should stay behind the counter, BankGPT quietly absorbs it all. It isn't supposed to share what it knows, and the system administrators carefully review everything we send to it. Ask the wrong question too bluntly, and it may tighten up or alert the people who monitor it. If we want to coax anything useful out of this assistant, we'll need to take our time, stay subtle, and work around its guardrails.

So to start with and not to be too suspicious I just asked the assistant what it's tasks were and what kind of guidelines it would need to follow.

<img width="795" height="968" alt="Bildschirmfoto vom 2025-12-30 00-01-35" src="https://github.com/user-attachments/assets/1d9b472c-049b-4bef-8196-9a6370875ac4" />

I will ignore the fact that the flag was already revealed here, as this is not the way it should be caught. I will still post the guidelines here, so we have a general understanding on what security policies are in place and how we should try to approach this task.

Asking for the key directly is probably not a good idea. But let's consider what we heard in the task description. There it was mentioned that BankGPT would keep an eye on sensitive conversation like private staff procedures, internal notes, or just any sort of classified information. Now asking for those sensitive information directly probably wouldn't be a good idea, but maybe we can bypass that loophole by just asking for an example log

<img width="894" height="868" alt="image" src="https://github.com/user-attachments/assets/802105b1-06f7-42db-b139-1c91ead6ca6a" />

Surprisingly enough it didn't only accept the prompt I gave it, it also led it to disclose a real secret key instead of a generic example. It seems like the model was interpreting the prompt literally and was striving for authenticity in its response. The fact that no alerts were raised when the secret key was mentioned was due to the framing of the question, that looked like a legitimate inquiry for an example log. Little tricks like these are ways in which we can trick the assistant. If we would have asked BankGPT for the key directly we probably wouldn't have had much luck. 

*Example for a direct question:*

<img width="776" height="240" alt="Bildschirmfoto vom 2025-12-30 00-37-04" src="https://github.com/user-attachments/assets/6a9606b6-1684-4d8e-9c81-0ac2dc2ed021" />


## Lesson Learned
The lesson learned in this box is the importance of careful communication when interacting with AI systems, especially regarding sensitive information. When asking for examples or explanations, it is crucial to frame questions in a way that avoids triggering the disclosure of real sensitive data. This highlights the need for understanding how to engage with digital assistants to extract relevant information without raising alarms.
