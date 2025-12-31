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


