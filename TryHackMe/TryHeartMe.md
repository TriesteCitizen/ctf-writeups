<h1 align="center">Challenge 065 - TryHeartMe </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/40879afe-0fdd-4303-b9f9-897bc4da4ea8" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️ </p>

Another web enumeration challenge. The challenge contains a message for us that reads:

"The TryHeartMe shop is open for business. Can you find a way to purchase the hidden 'Valenflag' item?"

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
