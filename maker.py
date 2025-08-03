#!/usr/bin/env python3
"""
SHA-256 Implementation with Backwards W Calculation
Target: a14 = b14 = c14 = d14 = 0xDEADBEEF
Adjusted so that W[14] and W[15] follow real SHA-256 padding:
  W[14] = 0x80000000, W[15] = 0x00000000
"""

import struct
import hashlib

# SHA-256 constants
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
    0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
    0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
    0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
    0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# SHA-256 initial hash values
H_INIT = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def ch(x, y, z):
    return (x & y) ^ (~x & z) & 0xFFFFFFFF

def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def sigma0(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)

def sigma1(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)

def gamma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)

def gamma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)

def calculate_required_w():
    print("🎯 Target: a14 = b14 = c14 = d14 = 0xDEADBEEF")
    print("=" * 60)
    
    W = [0] * 16
    # your permanent first 10 words:
    W[0:10] = [
        0x48656c6c, 0x6f20576f, 0x726c6421, 0x20546869,
        0x73206973, 0x20612074, 0x65737420, 0x6d657373,
        0x61676520, 0x666f7220
    ]
    print("\n📌 PERMANENTLY STORED W[0:9]:")
    for i in range(10):
        print(f"W[{i:2d}] = 0x{W[i]:08X}")
    
    # init state
    a,b,c,d,e,f,g,h = H_INIT
    
    # rounds 0–9
    for i in range(10):
        T1 = (h + sigma1(e) + ch(e,f,g) + K[i] + W[i]) & 0xFFFFFFFF
        T2 = (sigma0(a) + maj(a,b,c)) & 0xFFFFFFFF
        h,g,f,e,d,c,b,a = g,f,e,(d+T1)&0xFFFFFFFF,c,b,a,(T1+T2)&0xFFFFFFFF
    
    TARGET = 0xDEADBEEF
    
    # rounds 10–13, forcing a10..a13 = TARGET and computing W[10..13]
    for rnd, idx in enumerate(range(10,14), start=10):
        print(f"\n🎯 Round {idx}: Target a{idx} = 0x{TARGET:08X}")
        T2 = (sigma0(a) + maj(a,b,c)) & 0xFFFFFFFF
        T1 = (TARGET - T2) & 0xFFFFFFFF
        W[idx] = (T1 - h - sigma1(e) - ch(e,f,g) - K[idx]) & 0xFFFFFFFF
        print(f"  T2_{idx} = 0x{T2:08X}, T1_{idx} = 0x{T1:08X}, W[{idx}] = 0x{W[idx]:08X}")
        h,g,f,e,d,c,b,a = g,f,e,(d+T1)&0xFFFFFFFF,c,b,a,TARGET
    
    # Now at round 14, before padding words:
    print(f"\n✅ State at round 14: a14=0x{a:08X}, b14=0x{b:08X}, c14=0x{c:08X}, d14=0x{d:08X}")
    
    # **Actual SHA-256 padding words for a single 64-byte block**:
    W[14] = 0x80000000
    W[15] = 0x00000000
    print("\n📌 Applied real-SHA padding:")
    print(f"W[14] = 0x{W[14]:08X}")
    print(f"W[15] = 0x{W[15]:08X}")
    
    print("\n📋 Final W[0:15]:")
    for i in range(16):
        print(f"W[{i:2d}] = 0x{W[i]:08X}")
    return W

def pad_message(message):
    msg_len = len(message)
    msg_bit_len = msg_len * 8
    padded = bytearray(message)
    padded.append(0x80)
    zeros_needed = (56 - (msg_len + 1)) % 64
    padded.extend(b'\x00' * zeros_needed)
    padded.extend(struct.pack('>Q', msg_bit_len))
    return bytes(padded)

def sha256_compress(block, h_prev, trace=False):
    W = block[:16] + [0]*48
    for i in range(16,64):
        W[i] = (gamma1(W[i-2]) + W[i-7] + gamma0(W[i-15]) + W[i-16]) & 0xFFFFFFFF
    a,b,c,d,e,f,g,h = h_prev
    for i in range(64):
        T1 = (h + sigma1(e) + ch(e,f,g) + K[i] + W[i]) & 0xFFFFFFFF
        T2 = (sigma0(a) + maj(a,b,c)) & 0xFFFFFFFF
        h,g,f,e,d,c,b,a = g,f,e,(d+T1)&0xFFFFFFFF,c,b,a,(T1+T2)&0xFFFFFFFF
        if trace and i==14:
            print(f"Round14: a={a:08X} b={b:08X} c={c:08X} d={d:08X}")
    return [
        (h_prev[0]+a)&0xFFFFFFFF, (h_prev[1]+b)&0xFFFFFFFF,
        (h_prev[2]+c)&0xFFFFFFFF, (h_prev[3]+d)&0xFFFFFFFF,
        (h_prev[4]+e)&0xFFFFFFFF, (h_prev[5]+f)&0xFFFFFFFF,
        (h_prev[6]+g)&0xFFFFFFFF, (h_prev[7]+h)&0xFFFFFFFF
    ]

def sha256_full(message):
    padded = pad_message(message)
    h = H_INIT.copy()
    for i in range(0, len(padded), 64):
        block = [struct.unpack('>I', padded[j:j+4])[0] for j in range(i, i+64, 4)]
        h = sha256_compress(block, h, trace=(i==0))
    return b''.join(struct.pack('>I', w) for w in h)

def create_message_from_w(W):
    # W[0..13] → 14 words → 56 bytes
    # Padding words W[14]=0x80000000, W[15]=0x00000000 come from pad_message
    msg = b''.join(struct.pack('>I', W[i]) for i in range(14))
    return msg

def test_with_real_sha256():
    print("="*60)
    print("🧪 TEST WITH REAL SHA-256")
    print("="*60)
    W = calculate_required_w()
    message = create_message_from_w(W)
    print(f"\nGenerated message ({len(message)} bytes): {message.hex()}\n")
    ours = sha256_full(message)
    std  = hashlib.sha256(message).digest()
    print(f"Our SHA256:  {ours.hex()}")
    print(f"Python SHA: {std.hex()}")
    print("Match: ", "✅" if ours==std else "❌")

if __name__ == "__main__":
    test_with_real_sha256()