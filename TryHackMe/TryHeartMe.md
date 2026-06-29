<h1 align="center">Challenge 065 - TryHeartMe </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/40879afe-0fdd-4303-b9f9-897bc4da4ea8" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

Another web enumeration challenge. The challenge contains a message for us that reads:

"The TryHeartMe shop is open for business. Can you find a way to purchase the hidden 'Valenflag' item?"

## Flag
We are given the URL for the web application, which we access. 

<img width="1111" height="791" alt="Bildschirmfoto vom 2026-06-29 15-26-48" src="https://github.com/user-attachments/assets/8b828a4e-b179-4bcc-bfc7-5639a3c2257b" />

This seems to be a website which gives us the possibility to buy different items. They are all valentine themed. Furthermore we can login with credentials to make a purchase. My first assumptions are the classic SQL Injection.

<img width="408" height="324" alt="grafik" src="https://github.com/user-attachments/assets/ac7e1585-ff07-4760-a4c5-e65429b43625" />

SQLi doesn't work as well as directory enumeration

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

In the next step I tried checking the source code of the login directory.

```
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Login — TryHeartMe</title>
  <link rel="stylesheet" href="/static/css/style.css">
  <script defer src="/static/js/app.js"></script>
</head>
<body>
<header class="topbar">
  <a class="brand" href="/">
    <img class="brand-mark" src="/static/img/logo.png" alt="TryHeartMe">
  </a>

    <nav class="nav">
      <a href="/" class="navlink">Shop</a>
      
        <a href="/login" class="navbtn navbtn--pill">Login</a>
        <a href="/register" class="navbtn navbtn--primary navbtn--pill">Sign up</a>
      
    </nav>
  </header>

  <main class="container">
    
      
    
    
<section class="auth">
  <div class="card auth-card">
    <h1 class="page-title" style="font-size:22px; margin:0">Login</h1>
    <p class="page-sub" style="margin-top:6px">Log in to continue.</p>
    <form class="form" method="post" action="/login">
      <input type="hidden" name="next" value="/admin">
      <label>Email</label>
      <input name="email" type="email" placeholder="you@domain.local" required>
      <label>Password</label>
      <input name="password" type="password" placeholder="••••••••" required>
      <button class="btn btn--primary" type="submit">Log in</button>
      <a class="btn btn--ghost" href="/register?next=/admin">Create account</a>
    </form>
  </div>
</section>

  </main>

</body>
</html>
```

When looking at the bottom of the form:

```
<a class="btn btn--ghost" href="/register?next=/admin">Create account</a>
```

we can see the site allows us to register our own account, and it passes the ?next=/admin parameter to the registration page.

As an exploit we can try clicking the link or go directly to */register*. We register a brand new account using the expected email format (e.g., test@domain.local). Because of the next=/admin parameter, once we successfully register and the system logs us in automatically, it might redirect our new account straight into the /admin panel, bypassing the need to guess the admin's password.

After creating the account we can check out our info in the account panel

<img width="1115" height="299" alt="grafik" src="https://github.com/user-attachments/assets/79459fe3-6698-45eb-98d8-d100644eba83" />

None of that helps, but after playing around with the login oage for a bit I had the realization that the server could save a JWT (JSON Web Token), a compact, secure, and self-contained standard (RFC 7519) used to safely transmit information between parties as a JSON object. It is most commonly used for user authentication (proving who you are) and authorization (proving what you are allowed to access) in web applications. The idea behind it is that instead of storing user session data on a server (which requires continuous database lookups), a JWT contains all necessary user information right inside the token itself.

Keeping that in mind, the next best idea should be to intercept the JWT token using Burp Suite, as it acts as an inline proxy between our browser and the target server.

When we submit the login form, the server processes our credentials and sends back a response containing the token.

Thus when we send the proxy to our repeater and check out what HTTP response we receive when sending the request, we see a very interesting jwt-token.

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

Since HS256 is a symmetric algorithm, the same secret key is used to sign and verify the token. If the developer uses a weak, default or guessable secret key (like `"secret"`, `"admin", or `"development"`, an attacker could use offline brute-force tools to guess the key, alter `"role":user` to `"role":admin`, and resign the token themselves.

To escalate privileges, we forge a new JWT token by modifying the payload to change the `role` from `user` to `admin`. First, we create a new JWT header with `alg` set to `none` and then construct a payload with `"role":"admin"`.

In Burp Suite we use the Proxy -> Intercept on option and forward the modified request to test admin access and reveal the admin-only content.

<img width="971" height="499" alt="grafik" src="https://github.com/user-attachments/assets/515bd2f5-59aa-4d0a-81ac-83f9115ffb4e" />

Using a Base64 decoder doesn't seem to work, so I pivoted to a JWT Debugger.

We encode the necessary information

<img width="935" height="763" alt="grafik" src="https://github.com/user-attachments/assets/0d916699-d54d-4cbf-8ce6-841d172f4ba8" />


So '{"alg":"none","typ":"JWT"}' 

<img width="935" height="763" alt="grafik" src="https://github.com/user-attachments/assets/99a5ab20-3a9f-40c2-a80a-ea86bab8ef87" />

And that seems to have worked out perfectly. We get a receipt.

<img width="930" height="260" alt="grafik" src="https://github.com/user-attachments/assets/121f2371-a4b5-47e2-b1dc-b8ed4b1a6f12" />

Still. Even when buying every item we quickly realize that the hidden Valenflag item is nowhere to be found. We might have to intercept the HTTP request again to alter the role from user to admin

<img width="920" height="709" alt="grafik" src="https://github.com/user-attachments/assets/b1482288-a9ca-4d55-9e7d-cf8ba32c5182" />

We paste the encoded JWT into our HTTP request and voila

<img width="919" height="704" alt="grafik" src="https://github.com/user-attachments/assets/c580ed38-5696-44cd-8f22-da687bd0ac4b" />

We see the item now. Let's buy it now. Keep in mind that we always have to alter the role for every request.

<img width="929" height="417" alt="grafik" src="https://github.com/user-attachments/assets/5a32afd6-3832-4d02-854e-eb0b19254b3c" />

After having done that the flag is ours.

<img width="929" height="417" alt="Bildschirmfoto vom 2026-06-29 20-38-17" src="https://github.com/user-attachments/assets/3429abf0-22fb-4866-b4f1-0eb53e6a9fb2" />

## Lesson Learned
The base difficulty of this challenge wasn't all that high. As soon as you knew that this had to do with JWT Tokens, the rest was pretty self explanatory. The only thing I seem to have had more problems with was that I thought I could alter the token simply by Base64 encoding my changes. This isn't possible as JWTs are cryptographically signed. While we can *decode* the payload to read it, any modification requires us to relocate the signature to make the token valid. The exact reasons on why my approach didn't work were:

- **Signature Verification:** A JWT consists of three parts separated by dots: Header, Payload and Signature. The signature is created by the server using a secret key to hash the first two parts. If we change the payload, the original signature will no longer match the data jwt.io
- **Server Rejection:** When we send an altered token, the server runs the same hashing algorithm on our modified payload. Since it won't match our forged signature - and the server has the only correct secret key to sign it properly - the server will reject the token as invalid or tampered with.
- **The Role of a JWT Debugger:** Tools like the jwt.io Debugger allow us to bypass this during development. They let us modify the payload, but more importantly, they give us a place to input the server's private key to **re-sign** the token, generating a valid signature that the server will actually accept.
