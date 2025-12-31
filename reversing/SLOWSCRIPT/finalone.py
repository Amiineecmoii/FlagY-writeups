
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
