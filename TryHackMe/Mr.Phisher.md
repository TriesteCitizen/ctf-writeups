<h1 align="center">Challenge 044 - Mr.Phisher </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/03145d99-3600-44f5-b431-8aa11cdc7232" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 22.10.2025 </p>

In this challenge we receive a suspicious email with a weird-looking attachment. It asks us to "enable macros". Sequences of instructions that automate repetitive tasks in applications, particularly in programs like Word or Excel. Users can create them to perform tasks like formatting documents, generating reports, or processing data automatically. They can enhance productivity but also be a security risk if we have to deal with harmful code.

Once we deploy the machine, we can clearly see some doc file which we can look at.

<img width="465" height="344" alt="image" src="https://github.com/user-attachments/assets/15b840d7-0dda-4673-80c2-747e2f2f7629" />

Opening the file shows us the following message.

<img width="759" height="346" alt="image" src="https://github.com/user-attachments/assets/44b29bfe-5f2e-4d5a-85ad-d77b2021ea22" />

Interesting. Seems like somebody really wants to do us harm here. Let's just go with the flow and confirm the alert to see what the doc contains for now.

<img width="973" height="904" alt="image" src="https://github.com/user-attachments/assets/b77950e9-1f45-4196-b15e-53efba18a9f2" />

It doesn't seem to give us more hints than necessary. I really am interested for those macros. So I just checked them out under Tools > Macros > Edit Macros to see what we were even dealing with.

<img width="896" height="410" alt="Bildschirmfoto vom 2025-10-22 15-50-11" src="https://github.com/user-attachments/assets/e75fa1d1-fecd-4647-a16a-193dce126c99" />

This seems like some very interesting instructions. It would be better if we could execute those in a save environment. They may contain the flag which we are looking for. I tried to convert this Visual Basics (VB) into Python to maybe run this in an editor after that.

<img width="1482" height="438" alt="image" src="https://github.com/user-attachments/assets/c3237810-4a3d-49b0-b024-e11ddf32a423" />

Now after having done that I just copied the source code and ran them in an online Python IDE. I just appended a main, which would call the created format() function and print the information of the b variable after everything was said and done and that worked out perfectly it seems.

<img width="1616" height="307" alt="Bildschirmfoto vom 2025-10-22 16-30-41" src="https://github.com/user-attachments/assets/e6744ff9-eaec-43fd-b81e-18972c119e9d" />

We received the flag and also learned something about macros, their potential dangers in documents, and how they may be used to run malicious code. This challenge emphasized the importance of being cautious when enabling macros, ESPECIALLY if they are contained in suspicious emails or attachments, which is huge evidence for phishing. It's another way for us to learn how to analyze and interact with macro-enabled documents to uncover hidden information, while maintaining security awareness. I never even was aware that we had the option to automate specific commands in our word documents and gives me the motivation to play around with VB instructions and get some exercise in. A CTF I recommend for a small appetizer.

