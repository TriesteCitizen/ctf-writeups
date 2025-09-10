<h1 align="center">Challenge 019 - Commited</h1>

<p align="center">
  <img width="105" height="103" alt="image" src="https://github.com/user-attachments/assets/79a29427-c5d4-49a0-9c58-5d625330b574" />
</p>
Difficulty: 1/10 (Very Easy)  Completed: ✔️ 

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

In it we find the commited zip file, which we are able to unzop with 

```
unzip commited.zip
```

now we are able to enter the github repository and check the most recent pushes and changes in it. With the command 

```
git log 
```

We get a clear idea of what kind of commit history we are dealing with

```
ubuntu@thm-comitted:~/commited/commited$ git log
commit 28c36211be8187d4be04530e340206b856198a84 (HEAD -> master)
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:49:32 2022 -0800

    Finished

commit 9ecdc566de145f5c13da74673fa3432773692502
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:40:19 2022 -0800

    Database management features added.

commit 26bcf1aa99094bf2fb4c9685b528a55838698fbe
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:32:49 2022 -0800

    Create database logic added

commit b0eda7db60a1cb0aea86f053816a1bfb7e2d6c67
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:30:43 2022 -0800

    Connecting to db logic added

commit 441daaaa600aef8021f273c8c66404d5283ed83e
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:28:16 2022 -0800

    Initial Project.
```

As I clearly wanted to see the differences that were made between specific commits I proceeded to use a command which compares changes made in a repository by using their specific commit ids

```
git diff 9ecdc566de145f5c13da74673fa3432773692502
28c36211be8187d4be04530e340206b856198a84
```

By doing that I only saw that differences in the README were done, which should not really have any influence on the source code whatsoever. THe result showed the following

```
ubuntu@thm-comitted:~/commited/commited$ git diff 9ecdc566de145f5c13da74673fa3432773692502 28c36211be8187d4be04530e340206b856198a84
diff --git a/Readme.md b/Readme.md
index 69d6211..0b8b1d5 100644
--- a/Readme.md
+++ b/Readme.md
@@ -5,6 +5,10 @@
 
 Commited is our project created to manage our databases, Commited will bring help our database management team by simplfying database management by using our python scripts.
 
+## Project Status
+
+Completed.
+
 ## Team
 
 Our development team consists of finest developers and we work simultaneously using our cool version control methodology. We are the BEST.

```

It didn't really contain any information about changed source code, so I kept on checking the next two commit ids, with each other

```
ubuntu@thm-comitted:~/commited/commited$ git diff 9ecdc566de145f5c13da74673fa3432773692502 26bcf1aa99094bf2fb4c9685b528a55838698fbe
diff --git a/main.py b/main.py
index 161979c..447ef7f 100644
--- a/main.py
+++ b/main.py
@@ -1,49 +1,13 @@
 import mysql.connector
 
-def create_db():
-    mydb = mysql.connector.connect(
-    host="localhost",
-    user="", # Username Goes Here
-    password="" # Password Goes Here
-    )
+mydb = mysql.connector.connect(
+  host="localhost",
+  user="", # Username Goes Here
+  password="" # Password Goes Here
+)
 
-    mycursor = mydb.cursor()
+mycursor = mydb.cursor()
 
-    mycursor.execute("CREATE DATABASE commited")
+mycursor.execute("CREATE DATABASE commited")
 
 
-def create_tables():
-    mydb = mysql.connector.connect(
-    host="localhost",
-    user="", #username Goes here
-    password="", #password Goes here
-    database="commited"
-    )
-
-    mycursor = mydb.cursor()
-
-    mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
-    
R(255))")
-    
-
-def populate_tables():
-    mydb = mysql.connector.connect(
-    host="localhost",
-    user="",
-    password="",
-    database="commited"
-    )
-
-    mycursor = mydb.cursor()
-
-    sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
-    val = ("John", "Highway 21")
-    mycursor.execute(sql, val)
-
-    mydb.commit()
-
-    print(mycursor.rowcount, "record inserted.")
-
-
-create_db()
-create_tables()
-populate_tables()
(END)

```
As I was not quite able to figure out what exactly was wrong with the given code, from what was given to me I just decided to run earlier commits. If we run the most recent we get the followin error output

```
ubuntu@thm-comitted:~/commited/commited$ python3 main.py
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    import mysql.connector
ModuleNotFoundError: No module named 'mysql'

```

But it was not helping either, as I was still not able to get the file running. So I changed back to the master branch with git checkout master.
Now I was very confused and decided to ask for help. People advised me to use the git log --all command, which would be abnle to show commits across all branches. So after doing that a hint finally revealed itself to me

```
ubuntu@thm-comitted:~/commited/commited$ git log --all
commit 28c36211be8187d4be04530e340206b856198a84 (HEAD -> master)
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:49:32 2022 -0800

    Finished

commit 4e16af9349ed8eaa4a29decd82a7f1f9886a32db (dbint)
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:48:08 2022 -0800

    Reminder Added.

commit c56c470a2a9dfb5cfbd54cd614a9fdb1644412b5
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:46:39 2022 -0800

    Oops

commit 3a8cc16f919b8ac43651d68dceacbb28ebb9b625
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:45:14 2022 -0800

    DB check

commit 6e1ea88319ae84175bfe953b7791ec695e1ca004
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:43:34 2022 -0800

    Note added

commit 9ecdc566de145f5c13da74673fa3432773692502
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:40:19 2022 -0800

    Database management features added.

commit 26bcf1aa99094bf2fb4c9685b528a55838698fbe
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:32:49 2022 -0800

    Create database logic added

commit b0eda7db60a1cb0aea86f053816a1bfb7e2d6c67
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:30:43 2022 -0800

    Connecting to db logic added

commit 441daaaa600aef8021f273c8c66404d5283ed83e
Author: fumenoid <fumenoid@gmail.com>
Date:   Sun Feb 13 00:28:16 2022 -0800

    Initial Project.

```
It immediately revealed a commit that may contain some interesting information to us

<img width="443" height="110" alt="image" src="https://github.com/user-attachments/assets/49003e42-7d09-4b9b-ac23-0b615520d297" />

We use the checkout command to then cat the main to see what's going on. After doing that we immediately see that there is some username that was hardcoded in the source code, which is a big mistake.

<img width="528" height="359" alt="Bildschirmfoto vom 2025-09-10 17-39-37" src="https://github.com/user-attachments/assets/d3d0cddc-172e-41d0-812c-dc64329f2352" />

Since this is the commit that was supposed to fix the actual mistake we go back one commit prior to then realize that the source code clearly contains the password, in form of a flag. 

<img width="681" height="366" alt="Bildschirmfoto vom 2025-09-10 17-51-27" src="https://github.com/user-attachments/assets/ff66c31d-dafa-4a0c-8740-129cf72afe97" />

What do we learn from this? Never hardcode your credentials into your source code, especially not if you commit them afterwards. Those commits should be cleaned up and removed before people make use of them, as they will remain in the git history.

