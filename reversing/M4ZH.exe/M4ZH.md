
## M47H – Reverse Engineering Writeup

Category: Reverse Engineering
Flag format: FlagY{}

Challenge Description : 

They say that C/C++ is old, so maybe it’s time to move on to something new.
But does using a “modern” language really make reversing harder?

This challenge provides a Windows executable that validates a flag using a non-trivial verification routine.
Our goal is to reverse the binary and recover the correct flag.

## File Information : 
$ file M47H.exe
```bash
M47H.exe: PE32+ executable (console) x86-64, for MS WindowsFile Information
```
## Characteristics:

>Native x64 PE

>Not .NET (no CLR header)

>Statically simple import table

>No packer or obfuscator detected

## 2. Entry Point & Program Flow

>The binary execution flow is:

>Print prompt string

>Read user input

>Strip newline

>Check input length

>Execute per-character validation loop

>Print success or failure message

The length check enforces 39 bytes exactly.

## 3. Input Length Check
Disassembly shows a comparison against 0x27 (39):
```asm
cmp     rcx, 27h
jne     wrong_flag
```

## 4. Core Validation Loop

The main verification loop iterates once per input character.
**Relevant Assembly Pattern (Simplified)**

```asm
movzx   eax, byte ptr [rsi + rbx]   ; load input[i]
imul    eax, eax, 34h               ; eax = input[i] * 0x34
xor     edx, edx
mov     ecx, 7Bh
div     ecx                         ; edx = (input[i] * 0x34) % 0x7B
cmp     dl, byte ptr [table + rbx]  ; compare remainder
jne     wrong_flag

```

**Registers:**

`rsi` → input buffer

`rbx` → loop index

`table` → static validation array

## 5. Mathematical Interpretation

**The validation enforces:**

(
𝑖
𝑛
𝑝
𝑢
𝑡
[
𝑖
]
×
52
)
 
m
o
d
 
123
=
𝑡
𝑎
𝑏
𝑙
𝑒
[
𝑖
]
(input[i]×52)mod123=table[i]

Where:

>`0x34 = 52`

>`0x7B = 123`

This is a linear modular equation per character.

## 6. Lookup Table Location

Using section headers:
```bash
objdump -h M47H.exe
```
| Section | VA       | File Offset |
| ------- | -------- | ----------- |
| .rdata  | 0x402000 | 0x1400      |

The table is referenced at VA `0x402020.`

**File Offset Calculation**
```bash
0x1400 + (0x402020 - 0x402000) = 0x1420
```
## 7. Extracting the Table
```python
with open("M47H.exe", "rb") as f:
    f.seek(0x1420)
    table = f.read(39)

print(table.hex())
```
Extracted bytes:
`495101434d006653320f220f582411455869695824584569012422580c0f666601326653663268`

## 8. Inverting the Equation

We solve:

𝑥
×
52
≡
𝑡
(
m
o
d
123
)
x×52≡t(mod123)

Since:

gcd
⁡
(
52
,
123
)
=
1
gcd(52,123)=1

A modular inverse exists.

Compute Modular Inverse

```python
for i in range(1, 123):
    if (52 * i) % 123 == 1:
        print(i)

```
Result:

`52
−
1
≡
97
(
m
o
d
123
)
52
−1
≡97(mod123)`

## 9. Character Recovery Formula

**input[i]=(table[i]×97)mod123**

The result is constrained to printable ASCII `(0x20–0x7E)`.

Each index produces exactly one valid printable character.

## 10. Full Solver Implementation
```python
#!/usr/bin/env python3

TABLE_OFFSET = 0x1420
FLAG_LEN = 39
MOD = 123
INV = 97

def recover_flag(path):
    with open(path, "rb") as f:
        f.seek(TABLE_OFFSET)
        table = f.read(FLAG_LEN)

    flag = []
    for t in table:
        val = (t * INV) % MOD
        for c in range(32, 127):
            if c % MOD == val:
                flag.append(c)
                break

    return bytes(flag).decode()

if __name__ == "__main__":
    print(recover_flag("M47H.exe"))
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
