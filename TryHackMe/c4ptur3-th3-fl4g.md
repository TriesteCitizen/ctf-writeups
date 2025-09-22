<h1 align="center">Challenge 024 - c4ptur3-th3-fl4g </h1>
<p align="center">
  <img width="94" height="91" alt="Bildschirmfoto vom 2025-09-22 15-48-46" src="https://github.com/user-attachments/assets/6bdc5684-bdbc-49e3-9ec9-a5bffc2aeb1a" />
</p>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 22.09.2025 </p>

This challenge consists of four different tasks that we need to beat. This challenge is very beginner level friendly so it should not be that hard

## Task 1 - Translation & Shifting

### Critical Thinking

In this task we are showcased different kind of values that need to be translated, shifted and decoded. The first one being

```
c4n y0u c4p7u23 7h3 f149?
```

I'm not sure if we really need to use some sort of tool for this, as the real message seems very evident. Just to give a satisfactory explanation the number values correspond to alphabetical values.
- 4 &rarr; a
- 0 &rarr; o
- 7 &rarr; t
- 2 &rarr; r
- 3 &rarr; e
- 1 &rarr; l
- 9 &rarr; g

I doubt that there is somebody who will not understand this, so I will move on.

### Binary Conversion

The next value is in binary representation

```
01101100 01100101 01110100 01110011 00100000 01110100 01110010 01111001 00100000 01110011 01101111 01101101 01100101 00100000 01100010 01101001 01101110 01100001 01110010 01111001 00100000 01101111 01110101 01110100 00100001
```

This can easily be solved by using a Binary to Text Translator

<img width="606" height="388" alt="Bildschirmfoto vom 2025-09-22 16-36-47" src="https://github.com/user-attachments/assets/698cabdc-8aa4-486d-8899-17325cdf2817" />

### Base32

The next value seems to be some sort of base32 representation, as only uppercase letters seem to be provided

```
MJQXGZJTGIQGS4ZAON2XAZLSEBRW63LNN5XCA2LOEBBVIRRHOM======
```

We check with a given decoder

<img width="581" height="269" alt="Bildschirmfoto vom 2025-09-22 16-49-32" src="https://github.com/user-attachments/assets/e7aba2e3-c4f1-4897-a19d-e246cc5127a5" />

We were indeed right. I'm slowly beginning to recognize common patterns.

### Base64

Moving on we have this value now

```
RWFjaCBCYXNlNjQgZGlnaXQgcmVwcmVzZW50cyBleGFjdGx5IDYgYml0cyBvZiBkYXRhLg==
```

Equal signs at the end? A combination of uppercase and lowercase letters? This HAS to be base64. We use a tool to make sure

<img width="871" height="493" alt="Bildschirmfoto vom 2025-09-22 16-53-01" src="https://github.com/user-attachments/assets/60c9d732-ad0b-4141-8f08-5f57e84b101d" />

We were right. Easy.

### Hexadecimal

Next is 

```
68 65 78 61 64 65 63 69 6d 61 6c 20 6f 72 20 62 61 73 65 31 36 3f
```

A collection of several hexadecimal values perhaps? Let's convert the hexadecimal into text to see if that will lead to something.

<img width="1423" height="294" alt="image" src="https://github.com/user-attachments/assets/70d9b185-456e-4c34-a0d6-730fc0583d7e" />

Indeed it did. Somehow the challenging part of this value was recognizing if it would be base16 or hex encoded. I did not even consider the first possibility, but it seems to have worked out just fine so whatever.

### ROT13

Now we have the value

```
Ebgngr zr 13 cynprf!
```

As I already did a task today, where I had to decode ROT13 and seeing the answer format I was pretty sure that we had to make use of a ROT13 decoder again.

<img width="1262" height="191" alt="Bildschirmfoto vom 2025-09-22 17-08-43" src="https://github.com/user-attachments/assets/a1afc5f6-f5d0-411e-854a-3a4d350d3e8a" />

Right again.

### ROT47

Following now is 

```
*@F DA:? >6 C:89E C@F?5 323J C:89E C@F?5 Wcf E:>6DX
```

Looking at the answer format yet again this seems to be some sort of shifting operation again. While we shift 13 characters with ROT13, maybe there is another cipher shifting that results in this value. And I was right with that. ROT47 to be exact

<img width="1564" height="259" alt="Bildschirmfoto vom 2025-09-22 17-15-30" src="https://github.com/user-attachments/assets/8456e6cb-9553-4015-8fb1-ff4f2bfdc505" />

Done and dusted.

### Morse-Code

Now we get challenged with something that looks like morse code

```
- . .-.. . -.-. --- -- -- ..- -. .. -.-. .- - .. --- -.

. -. -.-. --- -.. .. -. --.
```

And it doesn't only look like morse code. It actually is. So we put that into a translator

<img width="1164" height="235" alt="Bildschirmfoto vom 2025-09-22 17-21-07" src="https://github.com/user-attachments/assets/5f08ec07-7a7a-4f49-b8f3-41d4dc2ba3c5" />

Success once again.

### Decimal to ASCII

The penultimate value is 

```
85 110 112 97 99 107 32 116 104 105 115 32 66 67 68
```

For some reason I just KNEW that sooner or later we would have to convert decimal into ascii. I immeditately recognized the values as decimal representation of ascii and used a converter

<img width="639" height="697" alt="Bildschirmfoto vom 2025-09-22 17-24-49" src="https://github.com/user-attachments/assets/f945bf3e-c724-4b09-bc14-763e648b4fb1" />

### Chain of Operations

The last value for this task is

```
LS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0KLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLS0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLi0tLS0KLS0tLS0gLi0tLS0gLi0tLS0gLS0tLS0gLS0tLS0gLi0tLS0gLS0tLS0gLi0tLS0=
```

Quite frankly I have never seen something like this. I tried playing around with many different tools until the value was converted into Morse-Code when trying to base64 decrypt it. I tried to decrypt the morse-code next and received binary. I slowly realized that this would be a chain of different decryption techniques I would have to combine, if I really wanted to get the final result, so I used Cyberchef

<img width="1430" height="647" alt="Bildschirmfoto vom 2025-09-22 17-48-32" src="https://github.com/user-attachments/assets/580dc846-94c9-4e05-bf51-335928a5de1c" />

They really went all out at the end. What a delight!

## Task 2 - Spectogram

Now we have to work with spectograms, which are visual representations of the spectrum of frequencies of a signal as it varies with time. When applied to an audio signal, spectograms are sometimes called sonographs, voiceprints, or voicegrams. When the data is represented in a 3D plot they may be called waterfalls.

For this task we are asked to download a file. An audio file to be exact. When it's started a weird noise is played. I just looked for some Spectogram tool online and swiftly found a website, which we could use. In my case it was the Spectrum Analyzer.

<img width="1145" height="580" alt="Bildschirmfoto vom 2025-09-22 18-05-33" src="https://github.com/user-attachments/assets/dbeb1169-66d9-48cd-88f4-35ebec2ea254" />

The part that I covered revealed a hidden message, exactly like the task mentioned. I never did something like this, so it was quite exciting seeing everything fall into place. Hopefully I can do some other task with spectograms in the future.

## Task 3 - Steganography

In this task we have to deal with steganography, which is the practice of concealing a file, message, image, or video within another file, message, image, or video. A file to download is given yet again. When downloaded we get this beautiful image
<p align="center">
  <img width="254" height="343" alt="canvas" src="https://github.com/user-attachments/assets/0f098d8c-4729-4ca8-87ab-09bd50055dd9" />
</p>

Lovely. There also are millions of tools that can decode such images. In my case, I used the Steganographic Decoder. I submitted the png and voila. I received the hidden message. I didn't even have to use some password.

<img width="572" height="77" alt="Bildschirmfoto vom 2025-09-22 18-28-01" src="https://github.com/user-attachments/assets/e80ef18d-6ac0-411b-8758-913f551606b1" />

## Task 4 - Security through obscurity

The last task has to do with security through obscurity, which is the reliance in security engineering on the secrecy of the design or implementation as the main method of providing security for a system or component of a system.

The downloaded task file was this meme, which I uploaded the screenshot of.

<p align="center">
  <img width="490" height="475" alt="Bildschirmfoto vom 2025-09-22 18-39-59" src="https://github.com/user-attachments/assets/41ac523e-bd0a-4d68-bb43-9097883cbab9" />
</p>

The penultimate task asks us to download and get 'inside* the file, which can be achieved with binwalk, an open-source command-line tool for analyzing binary files and extracts embedded files, executable code and file systems.

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ binwalk -e meme_1559010886025.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
30            0x1E            TIFF image data, big-endian, offset of first image directory: 8

WARNING: Extractor.execute failed to run external extractor 'unrar e '%e'': [Errno 2] No such file or directory: 'unrar', 'unrar e '%e'' might not be installed correctly

WARNING: Extractor.execute failed to run external extractor 'unrar -x '%e'': [Errno 2] No such file or directory: 'unrar', 'unrar -x '%e'' might not be installed correctly
74407         0x122A7         RAR archive data, version 5.x
74478         0x122EE         PNG image, 147 x 37, 8-bit/color RGBA, non-interlaced
74629         0x12385         Zlib compressed data, default compression
```

This created another directory, which we can enter.

```
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads$ cd _meme_1559010886025.jpg.extracted
lorenzo@lorenzo-HP-Laptop-15s-eq2xxx:~/Downloads/_meme_1559010886025.jpg.extracted$ ls -la
insgesamt 68
drwxrwxr-x 2 lorenzo lorenzo  4096 Sep 22 19:14 .
drwxr-xr-x 9 lorenzo lorenzo 20480 Sep 22 19:14 ..
-rw-rw-r-- 1 lorenzo lorenzo  5716 Sep 22 19:14 122A7.rar
-rw-rw-r-- 1 lorenzo lorenzo 21793 Sep 22 19:14 12385
-rw-rw-r-- 1 lorenzo lorenzo  5494 Sep 22 19:14 12385.zlib
```

The rar can now be opened, which reveals the information that we so desperately were looking for

<img width="1207" height="158" alt="Bildschirmfoto vom 2025-09-22 19-24-23" src="https://github.com/user-attachments/assets/9b6d218b-c05f-4b70-99f8-0d33f64807dd" />

The very last thing we were asked to do is to get inside the archive and inspect the file carefully in hopes of finding some hidden text. For that I used StegOnline. Here we have the option to make us show strings

<img width="722" height="734" alt="Bildschirmfoto vom 2025-09-22 18-44-43" src="https://github.com/user-attachments/assets/736cf2ed-60dc-40eb-9762-0a847d85fa40" />

That was fairly easy as well and completes this challenge. I had a lot of fun with decrypting these values and make my first experiences with things like spectograms and tools like binwalk. Hopefully I can apply said knowledge soon enough and be faster in my approach as I took a feasible amount of time with this challenge. I can only recommend it though. Have fun! 
