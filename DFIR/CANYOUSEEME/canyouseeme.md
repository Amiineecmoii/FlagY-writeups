# 🕵️ Web Log Forensics – Blind SQL Injection Incident Analysis

## 📌 Challenge Overview

You are a security analyst investigating an **unauthorized database access incident**.  
The attacker exploited a vulnerability in a web application using **advanced SQL injection techniques** to extract sensitive credentials.

Your task was to analyze the provided **web server logs**, reconstruct the attack, identify the stolen data, and determine the full extent of the breach.

**Flag format:** `FlagY{}`

---

## 📂 Evidence Provided

- `apache2.zip`
  - Apache logs
  - ModSecurity audit logs (`modsec_audit.log`)

---

## 🔍 Initial Investigation

After extracting the archive, the primary artifact of interest was:
**modsec_audit.log**
```yaml

This log contains:
- Full HTTP requests
- Headers
- POST bodies
- Server responses

Making it ideal for **forensic reconstruction** of web attacks.

---
```
Suspicious traffic was identified by searching for SQL keywords and abnormal user agents:

```bash
grep -i "sql" modsec_audit.log
```
**Key Finding**

Multiple requests contained the following User-Agent:
```cpp
sqlmap/1.8.8#stable
```

## 🎯 Targeted Endpoint

All malicious requests targeted the following endpoint:
```swift
POST /DVWA/vulnerabilities/sqli_blind/
```
With cookies:
```ini
security=medium
PHPSESSID=...
```
➡️ The application was identified as Damn Vulnerable Web Application (DVWA)

➡️ Vulnerability: Blind SQL Injection (Boolean-based)

## 🧪 Attack Technique Analysis

The attacker used **Boolean-based Blind SQL Injection**, which works by:

>Injecting logical SQL conditions

>Observing differences in the HTTP response

>Reconstructing database values character-by-character

**Example Payload Observed**
```sql
id=1 AND ORD(MID(
  (SELECT password FROM dvwa.users ORDER BY user LIMIT 0,1),
  1,
  1
)) > 52
```

**Payload Breakdown**

>`SELECT password FROM dvwa.users`

>`MID(..., 1, 1)` → extract one character

>`ORD()` → ASCII value

>`> 52` → Boolean comparison

## 📄 Boolean Oracle Identification

The DVWA page responded differently depending on the SQL condition:

| Condition | Response                               |
| --------- | -------------------------------------- |
| TRUE      | `User ID exists in the database`       |
| FALSE     | `User ID is MISSING from the database` |

## 🔐 Extracted Database Content

By analyzing the logged payloads, the attacker successfully enumerated the dvwa.users table.

**Compromised Credentials**

| Username | Extracted Value                  |
| -------- | -------------------------------- |
| 1337     | 8d3533d75ae2c3966d7e0d4fcc69216b |
| admin    | 5f4dcc3b5aa765d61d8327deb882cf99 |
| gordonb  | e99a18c428cb38d5f260853678922e03 |
| pablo    | 0d107d09f5bbe40cade3de5c71e9e9b7 |
| smithy   | 5f4dcc3b5aa765d61d8327deb882cf99 |

>The extracted values are MD5 password hashes, confirming a full credential breach.

## 🧩 Flag Discovery

During enumeration, two unusual records were observed:

| Username | Extracted Value       |
| -------- | --------------------- |
| etoo     | FlagY{f0931********** |
| etoo16   | *****************}    |

The flag was split across two rows.

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

