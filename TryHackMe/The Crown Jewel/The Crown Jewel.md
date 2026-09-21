<h1 align="center">The Crown Jewel </h1>

<p align="center">
  <img src="assets/crownjewel.png" width="90" height="90"/>
</p>

<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 21.09.2026 </p>

We are on a shift, looking at the new alert coming from Imperium Labs - a company under MSSP monitoring long before we joined the team. It's hard to say what the company's primary focus is, but it has a global presence and undoubtedly has secrets to protect, especially those on heavily secured GitLab and Jira servers which store proprietary source code and project data.

## The Alert
The alert we are looking at is called `Reverse Shell Outbound Connection Detected`, not something you see every day. Fortunately, we were able to obtain the raw PCAPs and Splunk logs for this event. Can we analyze the network traffic and logs to reconstruct and stop a sophisticated attack aimed at stealing the "Crown Jewel" data?

<img width="1166" height="839" alt="5e8dd9a4a45e18443162feab-1762806692464" src="https://github.com/user-attachments/assets/b81396e6-b4d4-4e9a-88e0-711de26d403d" />

### From which internal IP did the suspicious connection originate?
I immediately opted on doing my analysis on Splunk, using the same query that was used in the screenshot: `index=network_logs log_type=ids`.

<img width="613" height="712" alt="image" src="https://github.com/user-attachments/assets/36e30f3c-5f53-4c60-9aa2-4ec339352724" />

The event.source_ip field gives away the answer.

### What outbound connection was detected as a C2 channel?
The event.dest_ip and event.dest_port fields reveal the dedicated connection.

### Which MAC address is impersonating the gateway 10.10.10.1?
This time we have to make sure to have a look at the challenge.pcap. To identify the MAC address impersonating the gateway I looked at ARP traffic and the given IP address and quickly recognized a high amount of broadcast messages announcing "10.10.10.1 is at 00:0c:29:11:22:33".

<img width="978" height="421" alt="image" src="https://github.com/user-attachments/assets/6f437621-3ddb-4062-8805-a75bdaad59ba" />

### What is the non-standard User-Agent hitting the Jira instance?
While there might have been good queries that could have also helped I just settled on checking all values of the event.agent field.

<img width="877" height="526" alt="image" src="https://github.com/user-attachments/assets/7a479abe-05e7-4601-9099-fb2bdae9c2d7" />

It's pretty evident which user agent is suspicious here.

### How many ARP spoofing attacks were observed in the PCAP?
Looking back into the Wireshark utility it was enough to just query `arp` or `arp.opcode == 2`to see all requests and responses regarding the ARP protocol. Exactly 90 packets were being displayed and that's also the amount of spoofing attacks.

### What's the payload containing the plaintext creds found in the POST request?
The query `http.request.method == "POST"` gives us exactly one packet where we can follow the HTTP Stream.

<img width="830" height="158" alt="image" src="https://github.com/user-attachments/assets/ae8ba253-2f3c-46a6-8597-f7abb947d630" />

There we see the plaintext credentials.

### What domain, owned by the attacker, was used for data exfiltration?
For this it might be useful to check DNS traffic this time around. I used the query`index=network_logs log_type="dns"` and checked the `event.domain` field in Splunk.

<img width="875" height="240" alt="image" src="https://github.com/user-attachments/assets/c07c1cb3-d18e-4396-b4e5-b5e1ae10ce9d" />

### After examining the logs, which protocol was used for data exfiltration?
I clicked on the corresponding event domain to find out more information on the whole data exfiltration process. The answer still is evident, given the whole context that was already given to us. DNS was obviously used here.

<img width="874" height="759" alt="image" src="https://github.com/user-attachments/assets/4e22c265-ff8f-41fa-8ea0-01ba5c288a8b" />

## Lesson Learned
This was a cute reintroduction in network traffic analysis. For a quick refresh on already established topics like data exfiltration, ARP spoofing and DNS tunneling it's doing a good job. It also gave me a good opportunity to combine the strengths of Wireshark and Splunk, using each tool where it was most effective. I might have made it myself too easy by jumping to the tool that felt the most easy to use at specific points, so I might return to showcase two different walkthroughs, one for Wireshark and one for Splunk.

