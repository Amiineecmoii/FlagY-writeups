# 🧊 FlagY – ICED 

## 📌 Challenge Information
- **Category:** Forensics / Malware Analysis
- **Flag format:** `FlagY{}`

---

## 🧠 Challenge Description

A Windows host was compromised by an attacker who leveraged **Living-off-the-Land Binaries (LOLBins)** to deliver malicious code.  
The payload was **obfuscated** and executed in a **fileless manner**, making detection and analysis non-trivial.

Objective: **Analyze the forensic artifacts, reverse the obfuscation, and extract the hidden flag.**

---

## 🔍 Initial Triage & Artifact Overview

After extracting the archive, the file structure mimics a realistic Windows user environment:
Iced/

└── AppData/

├── Local/

│ └── Microsoft/

│ └── Windows/

│ └── INetCache/

│ └── IE/

│ └── XBF3V9IT/

│ └── secret[1].ps1

└── LocalLow/

└── Microsoft/

└── CryptnetUrlCache/

```yaml
### Key Indicators
- Presence of **Internet Explorer cache artifacts**
- Suspicious **PowerShell script inside INetCache**
- No standalone malicious executable
- Strong indication of **fileless execution**

This immediately suggests a **LOLBin-based delivery mechanism**.
```
---
```yaml
## 🛠️ Execution Technique (LOLBin Abuse)

The attacker avoided dropping binaries and instead relied on:
- Native **PowerShell**
- Cached script execution
- Trusted Windows execution paths

This aligns with common malware families such as **IcedID (BokBot)**, which frequently abuse:
- `powershell.exe`
- `mshta.exe`
- `rundll32.exe`
```
➡️ This technique bypasses traditional AV by blending into normal system behavior.

---

## 🔐 Obfuscated PowerShell Analysis

### File of Interest
`AppData/Local/Microsoft/Windows/INetCache/IE/XBF3V9IT/secret[1].ps1`

```lua
Upon inspection:
- No readable strings
- Heavy use of string formatting (`-f`)
- Fake variable names
- Runtime string replacement logic
```
Example pattern:

```powershell
("{0}{1}{2}" -f 'a','b','c') -replace 'Cvx',''''
```
This confirms intentional obfuscation to hinder static analysis.

##🧩 Deobfuscation Process
**Step 1 – Identify Replacement Tokens**

The script replaces placeholders at runtime:

`Cvx` → `'`

`jYO` → `"`

Applying these substitutions reveals a Base64-encoded blob.

**Step 2 – Extract the Encoded Payload**

After reconstructing the string, we obtain:
```bash
ZgBsAGEAZwBZAHsAZAA0ADEAZAA4AG...
```
The structure indicates UTF-16LE Base64, a common PowerShell obfuscation method.

**Step 3 – Decode Correctly**

Decoding steps:

>Base64 decode

>Interpret output as UTF-16LE text

Resulting PowerShell snippet:
```powershell
$flag = "FlagY{d41d8c*********************************}"
```

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

