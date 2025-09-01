# Challenge 016 - Cipher's Secret Message
Difficulty: Very Easy (1/10) Completed: ✔️ 30.08.2025 

I did another Cryptography challenge as I felt like I could really improve when it comes to reading Python script in general. So for this task we analyzed source code to figure out how an encryption algorithm worked. We also had a secret message, which needed to be decoded. 
```
Message : a_up4qr_kaiaf0_bujktaz_qm_su4ux_cpbq_ETZ_rhrudm
```
The encryption algorithm looks as follow:

<img width="805" height="297" alt="cypher2" src="https://github.com/user-attachments/assets/129f3746-ac65-4489-8a23-a11e8661a001" />
 
Yet again, I'm still getting started with Cryptography so I actually started writing down notes manually without attempting to write my own script, which in hinsight, maybe would have been for the best and is a skill that I should try to achieve, as it automates the whole process. I was scribbling around, trying to stay concentrated and hoping that I would not have a little mishap while doing the operations (which I did). I WAS able to find out the decrypted message, but the goal in source code analyzing should always be to tamper around with operators, see how the total value changes and get a feel on what influences the source code.
In the script you can see that the source code is going through a chain of operations. Through a for loop we are iterating through every character of our message string. In every step the given character gets turned into the unicode representation of the specified character, which also gets subtracted by a base value, which is the unicode representation of two different characters given two specific conditions.

- If the character we are iterating through is uppercase, we return the value 65
- If the character we are iterating through is lowercase, we return the value 97

We can refer to the ASCII Table to make the connection what unicode represents a specific character.

![desktop_f5d2d27d-6d7f-435e-9bb1-14585db0f16b](https://github.com/user-attachments/assets/09f32ec4-78d6-40c3-b8b3-bfc8b41c5c5c)
 
After that we modulo the result 26 in case the value is out-of-bounds from the albhabet range. Lastly we will add the base value again, which can either be 65 or 97, depending on the upper condition. All these operations will only happen, if the character we are dealing with is in fact in the alphabet range. If it isn't we leave it unchanged and move on to the next character. 
Now, if you are me, and don't do a lot of cryptography you might have been a little overwhelmed, when looking at this source code the first time. I was at least. To put everything into perspective I really tried to note down every little detail and understand what I even was dealing with. On hinsight it feels kind of silly that I even made that much of an effort, as Cryptography should be more about finding the basic pattern and trying to modify the code in a way that reverses the procedure. But I wasn't understanding anything, so I thought getting a little overview would be good.

<img width="1467" height="824" alt="cypher3" src="https://github.com/user-attachments/assets/349b8ab1-e68d-4a5d-9345-2561c0d4ef2e" />
 
Maybe you can even see some strategy where I was trying to deduce the base value, by looking at the character we had in our encrypted message, and what value needed to be put, so the result of the modulo operation would be able to add a value big enough to get to the solution. It was only there that I understood that if the encrypted character message would be lowercase, the original one would be as well. I also (partly!) understood that the i-value would be the relevant denominator to influence how our message would get encrypted, as I hovered across the alphabet table with my finger, counting the iterations, to get to our original message. Not once thinking about how smart it could maybe be, if we could just take the encrypted message and change the arithmetic operation to a minus, to reverse the whole process.



As you can see by doing that we get the message much faster and are able to get a better understanding of the principles of cryptography, specificially how different operations can affect message integrity and encoding. By manipulating operators and understanding modular arithmetic, we can learn how to effectively encode and decode messages while preserving their essential characteristics. Next time I will immediately start scripting instead of doing a 
