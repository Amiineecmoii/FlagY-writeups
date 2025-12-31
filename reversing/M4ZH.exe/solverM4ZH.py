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
