
# 🧩 Reverse Engineering Challenge – Python Bytecode (.pyc)

**Category:** Reverse Engineering  
**Difficulty:** Easy  
**Flag format:** `FlagY{}`  

---

## 📌 Challenge Overview

In this challenge, we are provided with a **compiled Python bytecode file** (`.pyc`) instead of a standard Python source file.  
The objective is to reverse engineer the bytecode, recover the original logic, and extract the hidden flag.

---

## 🧠 Initial Analysis

The given file is:

**chall.pyc**

```yaml
A `.pyc` file contains **Python bytecode**, which means:
- The original source code is not directly visible
- However, the logic and strings can often be recovered
- Python bytecode is **not strongly protected** against reverse engineering

---
```
## 🔍 Step 1 – Identify the File Type

First, we verify the file type:
```bash
file chall.pyc
```

Expected output:
```arduino
Python 3.x byte-compiled
```

This confirms that the challenge is a Python reverse engineering task.

## 🛠️ Step 2 – Decompile the Bytecode

To recover readable Python code from the .pyc file, we use a Python decompiler.

Option 1: pycdc 
```bash
pycdc chall.pyc
```
Option 2: uncompyle6
```bash
uncompyle6 chall.pyc
```
Both tools reconstruct Python-like source code from bytecode.

## 🧩 Step 3 – Analyze the Decompiled Code

After decompiling, we observe that:

>The program contains a simple validation logic

>The flag is hardcoded directly in the bytecode

>No encryption, hashing, or runtime checks are applied

## 🏁 Step 4 – Extract the Flag

Since the flag is stored as a plain string in the bytecode, recovering it is trivial.

`**FlagY{w0w_I_ho.....}**`

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

