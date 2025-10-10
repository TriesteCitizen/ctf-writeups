<h1 align="center">Challenge 039 - Scripting </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/8bcbb5a1-dacf-480f-b757-66322f3872ad" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️  </p>

It's time to tackle some CTFs that might be a bit more challenging. As I'm not known to be a real expert when it comes to scripting I thought this might be a good way to improve my logical skills. Here we have 3 different tasks that expect me to write some Bash and/or Python. Here we go

## Base64

This file has been base64 encoded 50 times. Our task is to write a script to retrieve said flag. The general process will be as follow:
1. Read input from the file
2. use function to decode the file
3. do process in a loop

### Bash
I thought I would probably have more luck using bash commands, but then I realized this was the time where I would have to run for loops and work with variables. I didn't even know you used dollar signs "$" to retrieve values that are stored in variables. 

<img width="643" height="132" alt="Bildschirmfoto vom 2025-10-10 13-29-31" src="https://github.com/user-attachments/assets/f83f04af-2fee-4ec4-9a56-a7a63fc7dacc" />

In the fourth line *echo "$output" > b64.txt* I took the contents stored in the variable *output* and wrote them to the file b64.txt. When you know the necessary commands this isn't even that difficult. You just have to get into the nitty gritty of it all.

### Python
Now we try our luck with Python. While writing the script we internalize that Base64 encoding is designed to work with binary data, so when we want to perform the decoding, we have to turn the string into bytes. By encoding the string into bytes (using methods like *encode('utf-8')*, we convert the string into a format that can be processed by the base64 deocoding function. After the decoding is done, we can convert the bytes back into a string format by decoding yet again. Don't forget to update the data for the next iteration!

<img width="534" height="382" alt="image" src="https://github.com/user-attachments/assets/d9217a6f-9fe4-40b3-b8f1-824048e5d04c" />

All in all pretty manageable. We move on.

## Gotta Catch Em All

As this CTF will gradually raise in difficulty this second task will logically be a bit more challenging.

Here we have to write a script that connects to this webserver on the correct port, do an operation on a number and then move onto the next port. We have to start our original number at 0. 

The format is: *operation, number, next port.*

The website itself explains this procedure as well. When we go to the machines IP-Address and specify the port we see the following site

<img width="1154" height="398" alt="Bildschirmfoto vom 2025-10-10 15-00-05" src="https://github.com/user-attachments/assets/00172c38-900b-4326-9a4b-1d9d5648a4d2" />

The best approach for this is
1. We create a socket in Python using the sockets library
2. Connect to the port
3. Send an operation
4. View response and continue

To get started I just wrote a simple socket script that would be able to send several GET requests to the given server

```
import socket
HOST = '10.10.50.147'
PORT = 3010

while PORT != 9765:
    try:
        if PORT == 3010:
            print(f"Connecting to {HOST} on port {PORT} until it's available")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST,PORT))
                
            #send get request to the server
            request = f"GET / HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n"
            client.send(request.encode('utf-8'))
                
                
            response = client.recv(1024)
            data = response.decode('utf-8')
            print(data)
            client.close()
    except Exception as e:
        print(f"Error occured at {e}")
```

There were some variables I was not familiar with
- socket.AF_INET: Refers to the Address Family for IPv4, meaning the socket will use Internet Protocol version 4 addresses
- socket.SOCK_STREAM: Indicates that the socket will be used for TCP
- sendall(b'GET / HTTP/1.1\r\nHost: ' + HOST.encode() + b'\r\n\r\n'): sends an HTTP GET request to the web server. In the request the Host gets encoded as a byte string as the sendall method requires data to be in bytes. We also include the method (GET), the path (/) to request the root resource, the HTTP version (HTTP/1.1), and the Host header that specifies the server's hostname. The request is terminated with two carriage return and line feed characters (\r\n) to indicate the end of the headers.

This is were my brain started fuming though. I was successfully able to receive responses and print them. Sometimes the full body would be printed and sometimes it wouldn't

```
Connecting to 10.10.50.147 on port 3010 until it's available
HTTP/1.0 200 OK

Connecting to 10.10.50.147 on port 3010 until it's available
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1031
Server: Werkzeug/0.14.1 Python/3.5.2
Date: Fri, 10 Oct 2025 16:38:47 GMT


        <center>
        You need to write a script that connects to this webserver on the correct port, do an operation on a number and then move onto the next port. Start your original number at 0.</br></br>
        The format is: operation, number, next port.</br></br>
        For example the website might display, <b>add 900 3212</b> which would be: add 900 and move onto port 3212.</br>
        Then if it was <b>minus 212 3499</b>, you'd minus 212 (from the previous number which was 900) and move onto the next port 3499</br></br>
        Do this until you the page response is STOP (or you hit port 9765).</br></br>
        Each port is also only live for 4 seconds. After that it goes to the next port. You might have to wait until port 1337 becomes live again...</br></br>
        <h3>Its currenly on port <u><a target="_blank" id="onPort">5050</a></u>. R
Connecting to 10.10.50.147 on port 3010 until it's available
HTTP/1.0 200 OK
```

We also never got any operation data from this site. The reason why we sometimes get the body and sometimes don't is simply because of the timing and puffer. *recv* always tries to read what is in the buffer, but might not be able to because the body also is too large. Things we can avoid by looping recv until len(data) >= Content-Length or until recv() b'' gets returned (Connection Closed).

