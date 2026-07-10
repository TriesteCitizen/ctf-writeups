<h1 align="center">Challenge 065 - TryHeartMe </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/40879afe-0fdd-4303-b9f9-897bc4da4ea8" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 29.06.2026 </p>

Another web enumeration challenge. The challenge contains a message for us that reads:

"The TryHeartMe shop is open for business. Can you find a way to purchase the hidden 'Valenflag' item?"

## Flag
We are given the URL for the web application, which we access. 

<img width="1111" height="791" alt="Bildschirmfoto vom 2026-06-29 15-26-48" src="https://github.com/user-attachments/assets/8b828a4e-b179-4bcc-bfc7-5639a3c2257b" />

This seems to be a website which gives us the possibility to buy different items. They are all valentine themed. Furthermore we can login with credentials to make a purchase. My initial assumption was that the login form might be vulnerable to SQL injection, so I tested several common payloads.

<img width="408" height="324" alt="grafik" src="https://github.com/user-attachments/assets/ac7e1585-ff07-4760-a4c5-e65429b43625" />

None of them worked unfortunately. Checking for hidden directories also didnt lead to any results.

```
root@ip-10-112-82-82:~# gobuster dir -u http://10.112.159.79:5000/ -w /usr/share/wordlists/dirb/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.112.159.79:5000/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/account              (Status: 302) [Size: 227] [--> /login?next=/account]
/admin                (Status: 302) [Size: 223] [--> /login?next=/admin]
/login                (Status: 200) [Size: 1461]
/logout               (Status: 302) [Size: 189] [--> /]
/register             (Status: 200) [Size: 1517]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================
```

Checking the Page Source of the login panel didn't reveal anything worthwhile either. I just settled on creating an account for now.

After creating the account we can check out our info in the account panel

<img width="1115" height="299" alt="grafik" src="https://github.com/user-attachments/assets/79459fe3-6698-45eb-98d8-d100644eba83" />

None of that gave me an insight on what we should do. The next best idea I had was to intercept the HTTP request using Burp Suite. It acts as an inline proxy between our browser and the target server.

When we submit the login form, the server processes our credentials and sends back a response containing some sort of token.

Thus when we send the proxy to our repeater and check out what HTTP response we receive when sending the request, we see some insightful information.

```
HTTP/1.1 302 FOUND
Server: Werkzeug/3.0.1 Python/3.12.3
Date: Mon, 29 Jun 2026 17:12:59 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 189
Location: /
Set-Cookie: tryheartme_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZG9tYWluLmxvY2FsIiwicm9sZSI6InVzZXIiLCJjcmVkaXRzIjowLCJpYXQiOjE3ODI3NTMxNzksInRoZW1lIjoidmFsZW50aW5lIn0.x9awXfaWp6qkSpKdafo1w7WwIHr4vWp-wOZIdhy8OrY; Path=/; SameSite=Lax
Connection: close

<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/">/</a>. If not, click the link.
```

The HTTP Response contains a JWT (JSON Web Token). A compact, secure, and self-contained standard (RFC 7519) used to safely transmit information between parties as a JSON object. It is most commonly used for user authentication (proving who you are) and authorization (proving what you are allowed to access) in web applications. The idea behind it is that instead of storing user session data on a server (which requires continuous database lookups), a JWT contains all necessary user information right inside the token itself.
If we split the token (*tryheartme_jwt*) by its periods, we can decode the Base64 string to see exactly what information the server is tracking:

**1. Header**
- Encoded: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9`
- Decoded JSON: `{"alg": "HS256", "typ": "JWT"}`
- Meaning: The server uses the HS256 (HMAC symmetric) algorithm to sign the token.

**2. Payload**
- Encoded: `eyJlbWFpbCI6InRlc3RAZG9tYWluLmxvY2FsIiwicm9sZSI6InVzZXIiLCJjcmVkaXRzIjowLCJpYXQiOjE3ODI3NTMxNzksInRoZW1lIjoidmFsZW50aW5lIn0`
- Decoded JSON: `{
  "email": "test@domain.local",
  "role": "user",
  "credits": 0,
  "iat": 1782753179,
  "theme": "valentine"
}
`
- Meaning: The user currently has the role of `"user"`. To get admin privileges, a server would typically look for `"role": "admin"`.

To escalate privileges, we forge a new JWT token by modifying the payload to change the `role` from `user` to `admin`. A payload gets constructed with `"role":"admin"`.

In Burp Suite we use the Proxy -> Intercept on option and forward the modified request to test admin access and reveal the admin-only content.

<img width="971" height="499" alt="grafik" src="https://github.com/user-attachments/assets/515bd2f5-59aa-4d0a-81ac-83f9115ffb4e" />

Using a Base64 decoder doesn't seem to work, so I pivoted to a JWT Debugger.

We modify the JWT header and payload before re-encoding the token.

<img width="935" height="763" alt="grafik" src="https://github.com/user-attachments/assets/0d916699-d54d-4cbf-8ce6-841d172f4ba8" />

For the beginning and since I was curious I just settled on changing the credit score.

<img width="935" height="763" alt="grafik" src="https://github.com/user-attachments/assets/99a5ab20-3a9f-40c2-a80a-ea86bab8ef87" />

The modified token is accepted by the application. We get a receipt.

<img width="930" height="260" alt="grafik" src="https://github.com/user-attachments/assets/121f2371-a4b5-47e2-b1dc-b8ed4b1a6f12" />

Still. Even when buying every item we quickly realize that the hidden Valenflag item is nowhere to be found. It might be that the application is checking our role during subsequent requests rather than only during login. Let's alter the role from user to admin.

<img width="920" height="709" alt="grafik" src="https://github.com/user-attachments/assets/b1482288-a9ca-4d55-9e7d-cf8ba32c5182" />

Replacing the cookie with the modified JWT grants us adminstrative privileges.

<img width="919" height="704" alt="grafik" src="https://github.com/user-attachments/assets/c580ed38-5696-44cd-8f22-da687bd0ac4b" />

We see the item now. Let's buy it! Keep in mind that we always have to alter the role for every request.

<img width="929" height="417" alt="grafik" src="https://github.com/user-attachments/assets/5a32afd6-3832-4d02-854e-eb0b19254b3c" />

After having done that the flag is ours.

<img width="929" height="417" alt="Bildschirmfoto vom 2026-06-29 20-38-17" src="https://github.com/user-attachments/assets/3429abf0-22fb-4866-b4f1-0eb53e6a9fb2" />

## Lesson Learned
The base difficulty of this challenge wasn't all that high. As soon as you knew that this had to do with JWT Tokens, the rest was pretty self explanatory. The only thing I seem to have had more problems with was that I thought I could alter the token simply by Base64 encoding my changes. This isn't possible as JWTs are cryptographically signed. While we can *decode* the payload to read it, any modification requires us to relocate the signature to make the token valid. The exact reasons on why my approach didn't work were:

- **Signature Verification:** A JWT consists of three parts separated by dots: Header, Payload and Signature. The signature is created by the server using a secret key to hash the first two parts. If we change the payload, the original signature will no longer match the data jwt.io
- **Server Rejection:** When we send an altered token, the server runs the same hashing algorithm on our modified payload. Since it won't match our forged signature - and the server has the only correct secret key to sign it properly - the server will reject the token as invalid or tampered with.
- **The Role of a JWT Debugger:** Tools like the jwt.io Debugger allow us to bypass this during development. They let us modify the payload, but more importantly, they give us a place to input the server's private key to **re-sign** the token, generating a valid signature that the server will actually accept.
