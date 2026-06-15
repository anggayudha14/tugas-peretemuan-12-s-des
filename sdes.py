# ==========================================
# S-DES FINAL
# ==========================================

P10 = [3,5,2,7,4,10,1,9,8,6]
P8  = [6,3,7,4,8,5,10,9]

IP = [2,6,3,1,4,8,5,7]
IP_INV = [4,1,3,5,7,2,8,6]

EP = [4,1,2,3,2,3,4,1]
P4 = [2,4,3,1]

S0 = [
    [1,0,3,2],
    [3,2,1,0],
    [0,2,1,3],
    [3,1,3,2]
]

S1 = [
    [0,1,2,3],
    [2,0,1,3],
    [3,0,1,0],
    [2,1,0,3]
]


# ==========================================
# HELPER
# ==========================================

def permute(bits, table):
    return ''.join(bits[i - 1] for i in table)


def left_shift(bits, n):
    return bits[n:] + bits[:n]


def xor(a, b):
    return ''.join(
        str(int(x) ^ int(y))
        for x, y in zip(a, b)
    )


def sbox_lookup(bits, sbox):

    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)

    return format(sbox[row][col], '02b')


# ==========================================
# KEY GENERATION
# ==========================================

def generate_keys(key):

    details = []

    p10 = permute(key, P10)

    details.append({
        "title": "P10",
        "value": p10
    })

    left = p10[:5]
    right = p10[5:]

    details.append({
        "title": "Split P10",
        "value": f"{left} | {right}"
    })

    ls1_left = left_shift(left, 1)
    ls1_right = left_shift(right, 1)

    details.append({
        "title": "LS-1",
        "value": f"{ls1_left} | {ls1_right}"
    })

    k1 = permute(
        ls1_left + ls1_right,
        P8
    )

    details.append({
        "title": "K1",
        "value": k1
    })

    ls2_left = left_shift(ls1_left, 2)
    ls2_right = left_shift(ls1_right, 2)

    details.append({
        "title": "LS-2",
        "value": f"{ls2_left} | {ls2_right}"
    })

    k2 = permute(
        ls2_left + ls2_right,
        P8
    )

    details.append({
        "title": "K2",
        "value": k2
    })

    return k1, k2, details


# ==========================================
# ROUND FUNCTION
# ==========================================

def fk(bits, key, round_name):

    steps = []

    left = bits[:4]
    right = bits[4:]

    steps.append({
        "title": f"{round_name} - Split",
        "value": f"L={left} | R={right}"
    })

    ep = permute(right, EP)

    steps.append({
        "title": f"{round_name} - EP",
        "value": ep
    })

    xor_result = xor(ep, key)

    steps.append({
        "title": f"{round_name} - XOR Key",
        "value": xor_result
    })

    left4 = xor_result[:4]
    right4 = xor_result[4:]

    steps.append({
        "title": f"{round_name} - Split XOR",
        "value": f"{left4} | {right4}"
    })

    s0 = sbox_lookup(left4, S0)

    steps.append({
        "title": f"{round_name} - S0",
        "value": s0
    })

    s1 = sbox_lookup(right4, S1)

    steps.append({
        "title": f"{round_name} - S1",
        "value": s1
    })

    combined = s0 + s1

    steps.append({
        "title": f"{round_name} - S0+S1",
        "value": combined
    })

    p4 = permute(combined, P4)

    steps.append({
        "title": f"{round_name} - P4",
        "value": p4
    })

    left_new = xor(left, p4)

    steps.append({
        "title": f"{round_name} - XOR Left",
        "value": left_new
    })

    output = left_new + right

    steps.append({
        "title": f"{round_name} - Output",
        "value": output
    })

    return output, steps


# ==========================================
# SWAP
# ==========================================

def swap(bits):

    return bits[4:] + bits[:4]


# ==========================================
# ENCRYPT
# ==========================================

def encrypt(plaintext, key):

    steps = []

    k1, k2, key_steps = generate_keys(key)

    steps.extend(key_steps)

    ip = permute(plaintext, IP)

    steps.append({
        "title": "Initial Permutation (IP)",
        "value": ip
    })

    round1, round1_steps = fk(
        ip,
        k1,
        "Round 1"
    )

    steps.extend(round1_steps)

    sw = swap(round1)

    steps.append({
        "title": "Swap (SW)",
        "value": sw
    })

    round2, round2_steps = fk(
        sw,
        k2,
        "Round 2"
    )

    steps.extend(round2_steps)

    cipher = permute(
        round2,
        IP_INV
    )

    steps.append({
        "title": "Inverse IP (IP⁻¹)",
        "value": cipher
    })

    return cipher, steps


# ==========================================
# DECRYPT
# ==========================================

def decrypt(ciphertext, key):

    steps = []

    k1, k2, key_steps = generate_keys(key)

    steps.extend(key_steps)

    ip = permute(ciphertext, IP)

    steps.append({
        "title": "Initial Permutation (IP)",
        "value": ip
    })

    round1, round1_steps = fk(
        ip,
        k2,
        "Round 1"
    )

    steps.extend(round1_steps)

    sw = swap(round1)

    steps.append({
        "title": "Swap (SW)",
        "value": sw
    })

    round2, round2_steps = fk(
        sw,
        k1,
        "Round 2"
    )

    steps.extend(round2_steps)

    plain = permute(
        round2,
        IP_INV
    )

    steps.append({
        "title": "Inverse IP (IP⁻¹)",
        "value": plain
    })

    return plain, steps