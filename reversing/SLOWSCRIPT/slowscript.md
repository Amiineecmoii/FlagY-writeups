# 🧩 Challenge Write-Up — Too Slow Decryption

**Category:** Reverse Engineering / Cryptography  
**Flag format:** `FlagY{...}`

---

## 📜 Challenge Description

> *"Too slow, I don't know why… can you help me speed up the decryption?"*

We are provided with a Python script (`challenge.py`) intended to decrypt an encrypted flag.  
However, running the script normally is extremely slow and practically impossible to finish.

The goal is to **analyze the code**, **identify the bottleneck**, **optimize the logic**, and **recover the flag**.

---

## 🔍 Code Analysis

The relevant part of the script is shown below:

```python
tmp = 31337

for i in range(len(enc_flag)):
    fn = tmp ** i
    sm = 0
    for j in range(fn + 1):
        sm += j
    dec_char = (sm % 256) ^ enc_flag[i]
```
**Observations**

>tmp = 31337

>fn = 31337 ** i grows exponentially

>The inner loop computes:
```python
sm = 0
for j in range(fn + 1):
    sm += j
```

This is equivalent to:

<img width="83" height="49" alt="image" src="https://github.com/user-attachments/assets/0d894855-8146-45c6-a666-6b072f971fa9" />


For even small values of `i`, this loop becomes astronomically large, making the script unusable.

## 🧠 Mathematical Optimization

The summation used in the loop has a well-known closed-form formula:

<img width="126" height="47" alt="image" src="https://github.com/user-attachments/assets/d3b4dd14-32ab-462b-bca7-3ff03ac46b92" />

Instead of looping billions of times, we can compute this value instantly.

## ⚠️ Modular Arithmetic Optimization

The script only uses:
```python
sm % 256
```
Therefore, we do not need the full value of `n = 31337 ** i.`
We only need:

<img width="152" height="57" alt="image" src="https://github.com/user-attachments/assets/e7236836-3b10-4e54-94a4-f8a216026269" />


Handling the division by 2

To safely divide by 2 under modulo arithmetic, we compute n modulo 512:

***Handling the division by 2***

To safely divide by 2 under modulo arithmetic, we compute `n` modulo **512**:
```python
n_mod512 = pow(31337, i, 512)
```
This allows us to preserve correctness when dividing by 2.

## ⚡ Optimized Summation Function
```python
def sum0n_mod256(n_mod512):
    a = n_mod512
    b = (n_mod512 + 1) % 512
    if a % 2 == 0:
        a //= 2
    else:
        b //= 2
    return (a * b) % 256
```
This computes:

<img width="145" height="52" alt="image" src="https://github.com/user-attachments/assets/42c8c70c-9507-44a3-8bc4-e4c5e70881d2" />

## 🧪 Final Optimized Decryption Script

```python
enc_flag = [
    71,209,120,114,232,150,255,119,82,46,31,23,
    35,43,28,144,246,78,184,177,137,101,26,36,
    143,2,94,34,20,156,237,54,21,188,91,84,
    226,104,223,85,182,11,169,164,6,9,52
]

tmp = 31337

def sum0n_mod256(n_mod512):
    a = n_mod512
    b = (n_mod512 + 1) % 512
    if a % 2 == 0:
        a //= 2
    else:
        b //= 2
    return (a * b) % 256

flag = ""
for i, c in enumerate(enc_flag):
    n_mod512 = pow(tmp, i, 512)
    sm = sum0n_mod256(n_mod512)
    flag += chr(sm ^ c)

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

