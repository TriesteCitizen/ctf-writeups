# Challenge 019 - Commited
<img width="105" height="103" alt="image" src="https://github.com/user-attachments/assets/79a29427-c5d4-49a0-9c58-5d625330b574" />
Difficulty:  Completed: 

In this challenge we have to find some sensitive code that was commited to a GitHub repository, or at least it's what the developer told us. That's how the taks is described, so things may not be as they seem. For now I just tried to check out the target machine.

<img width="1273" height="307" alt="image" src="https://github.com/user-attachments/assets/42826730-84f1-460d-b5b1-34e3826a1b2e" />

Immediately after trying that though we get this error response telling us that the given method would be invalid for this resource. Are they referring to the GET Request? Even when using curl we get the same results

```
root@ip-10-10-130-18:~# curl -X GET http://10.10.15.129
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 405</p>
        <p>Message: Method Not Allowed.</p>
        <p>Error code explanation: 405 - Specified method is invalid for this resource.</p>
    </body>
</html>
```

Using POST just gave me some other sort of Error Message

```
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 501</p>
        <p>Message: Unsupported method ('POST').</p>
        <p>Error code explanation: HTTPStatus.NOT_IMPLEMENTED - Server does not support this operation.</p>
    </body>
</html>
```

Trying to use DELETE or PUT gave me the same results. Since we are working with a Git repository the next course of action was to try accessing the files through the terminal which were located at /home/ubuntu

```
root@ip-10-10-137-116:/home/ubuntu# ls -la
total 52
drwxr-xr-x 8 ubuntu ubuntu 4096 Nov  5  2024  .
drwxr-xr-x 5 root   root   4096 Aug 17  2020  ..
lrwxrwxrwx 1 ubuntu ubuntu    9 Feb 22  2021  .bash_history -> /dev/null
-rw-r--r-- 1 ubuntu ubuntu  220 Apr  4  2018  .bash_logout
-rw-r--r-- 1 ubuntu ubuntu 4069 Mar  8  2022  .bashrc
drwx------ 2 ubuntu ubuntu 4096 Feb 22  2021  .cache
drwx------ 4 ubuntu ubuntu 4096 Nov  4  2024  .config
-rw-rw-r-- 1 ubuntu ubuntu  746 Jan 24  2024 'Dark Blue to Green Gradient.svg'
drwx------ 3 ubuntu ubuntu 4096 Feb 22  2021  .gnupg
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar 18  2021  .local
drwxrwxr-x 2 ubuntu ubuntu 4096 Feb 10  2023  .msf4
-rw-r--r-- 1 ubuntu ubuntu  807 Apr  4  2018  .profile
drwx------ 2 ubuntu ubuntu 4096 Nov  1  2022  .ssh
-rw-r--r-- 1 ubuntu ubuntu    0 Feb 22  2021  .sudo_as_admin_successful
-rw------- 1 ubuntu ubuntu 1407 Nov  5  2024  .Xauthority
```

After a while I realized that I couldnt find the file because the AttackBox was set up properly. But after a short time I was finally able to get a hold of said directory.

<img width="762" height="662" alt="image" src="https://github.com/user-attachments/assets/85622f18-bdde-46c6-b0c3-b2f50453b297" />

In it we find 
