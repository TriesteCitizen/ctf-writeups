# Challenge 017 – Order	

Difficulty: Easy (2/10)
Completed: ✔️ 02.09.2025

Yet again at it with a cryptography challenge. In here a message was intercepted that contains the next target 
```
1c1c01041963730f31352a3a386e24356b3d32392b6f6b0d323c22243f6373
1a0d0c302d3b2b1a292a3a38282c2f222d2a112d282c31202d2d2e24352e60
```
This message was encrypted using a repeating-key XOR cipher. But a huge mistake was made with it. Every message always starts with the header: 
```
ORDER:
```
Now we have to find out the encryption key, so we can hopefully decipher this text. For that we first need to turn the header message into its hexadecimal equivalent to then be able to XOR it with the intercepted message.

<img width="762" height="186" alt="image" src="https://github.com/user-attachments/assets/ff586886-fe60-4b5f-90d1-41a2a2530aa4" />

The output gives us 4f 52 44 45 52 3a, which we XOR with the first 12 values of our intercepted message. From Hex assures us that we are able to XOR with the bytes representation of said values.  Through that we get the key value „SNEAKY“, which is the ASCII representation of said bytes. Now the key could be longer than that. It could also be „SNEAKY123“ or even longer. But we also know that we are able to use the encryption key to XOR with the intercepted message and find out at least part of the message. Yet again we use „From Hex“ to turn the intercepted message into its byte representation and use UTF-8 for the byte representation of ASCII.

<img width="1475" height="271" alt="image" src="https://github.com/user-attachments/assets/f7956462-10e6-4943-9c2c-fef6f8852a38" />

After having done that we receive the Output. Cyberchef was a very valuable source to solve this task, but I can also advise people to write their own Python script for these sorts of challenges, as it will make the whole idea more intuitive.
The lesson we learn here is if a specific segment of the Plaintext message is known, the key might be able to be recovered and we only have to consider the order of when and were we XOR the key with the intercepted message. Hopefully all confusions with byte representations cleared off for me and I finally know when to use which format.
