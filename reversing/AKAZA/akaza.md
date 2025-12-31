# Reverse Engineering Writeup — **Akaza**

## 🧩 Challenge Information
- **Name:** Akaza  
- **Category:** Reverse Engineering  
- **Flag format:** `FlagY{}`  

---

## 📜 Challenge Description

> *In this world, the strong devour the weak. Only by rising above your limitations can we truly become powerful.*

The challenge provides a single Windows executable `Akaza.exe`.  
No input is required from the user. The objective is to analyze the binary and recover the internally generated flag.

---

## 🧪 Initial Binary Analysis

### File identification
```bash
file Akaza.exe
```
**Result:**

>PE32+ executable (x86-64)

>Dynamically linked

>No obvious packer (not UPX)

**Basic triage**

>No command-line arguments

>Program exits immediately after execution

>No file/network I/O observed

This strongly suggests the flag is generated entirely at runtime.

## 🔎 Strings & Entropy Analysis
```bash
strings Akaza.exe
```
**Observations:**

>No plaintext flag present

>Presence of hexadecimal-looking constants

>Standard MSVC runtime strings

>No obvious obfuscation

The absence of the flag in plaintext indicates **computed or transformed data**.

## 🧠 Static Reverse Engineering
Tools used

**`IDA Pro / Ghidra (static analysis)`**

**`x64dbg (verification only)`**

## 📍 Program Entry & Control Flow

The entry point leads to a single main execution path:

>Load static data from `.rdata`

>Pass data to a transformation function

>Format the result as a string

>Exit

There are no branches depending on user input.

## 🧬 Embedded Data Discovery

Inside the `.rdata` section, a hardcoded byte array is referenced:
```c
unsigned char data[] = {
    0x61, 0x6B, 0x61, 0x7A, 0x61
};
```
ASCII decoding:

```arduino
"akaza"
```
This buffer is passed to a function that performs multiple rounds of bitwise operations.

## 🔐 Hash Function Identification
**Key observations inside the function:**

>Four 32-bit state variables `(A, B, C, D)`

>64 rounds of transformation

>Use of bitwise operations (`AND`, `OR`, `XOR`, `NOT`)

>Left-rotation operations

>Constants matching the MD5 sine table

>Final output size: **128 bits (16 bytes)**

These characteristics match the MD5 hashing algorithm exactly.

## 🔍 Decompiled Pseudocode (Simplified)
```c
hash = MD5("akaza");
hex_digest = to_hex(hash);
printf("FlagY{%s}", hex_digest);
```
No additional encryption or obfuscation is applied after hashing.

## 🧪 Reproducing the Flag

The flag can be reproduced independently without the binary:

```python
import hashlib

data = b"akaza"
flag = "FlagY{" + hashlib.md5(data).hexdigest() + "}"
print(flag)

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
