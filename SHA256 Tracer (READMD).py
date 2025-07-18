import sys
import struct

# --- SHA-256 primitives ---
def rotr(x, n): return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF
def ch(x, y, z): return (x & y) ^ (~x & z) & 0xFFFFFFFF
def maj(x, y, z): return (x & y) ^ (x & z) ^ (y & z)
def sigma0(x): return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)
def sigma1(x): return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)
def gamma0(x): return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
def gamma1(x): return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)

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

# Initial hash values
H_INIT = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

# Pad message into 512-bit blocks
def pad_message(msg_bytes):
    bit_len = len(msg_bytes) * 8
    padded = bytearray(msg_bytes)
    padded.append(0x80)
    # pad with zeros until length ≡ 56 mod 64
    padded.extend(b'\x00' * ((56 - (len(padded) % 64)) % 64))
    # append 64-bit length
    padded.extend(struct.pack('>Q', bit_len))
    return bytes(padded)

# SHA-256 on multi-block input with round-13 trace on first block
def demo_sha256(msg_bytes):
    padded = pad_message(msg_bytes)
    h = H_INIT.copy()
    # process each 512-bit block
    for block_index in range(0, len(padded), 64):
        block = [struct.unpack('>I', padded[i:i+4])[0]
                 for i in range(block_index, block_index+64, 4)]
        # message schedule
        W = block + [0]*48
        for t in range(16,64):
            W[t] = (gamma1(W[t-2]) + W[t-7] + gamma0(W[t-15]) + W[t-16]) & 0xFFFFFFFF
        # init working vars
        a,b,c,d,e,f,g0,h0 = h
        # compression rounds
        for i in range(64):
            T1 = (h0 + sigma1(e) + ch(e,f,g0) + K[i] + W[i]) & 0xFFFFFFFF
            T2 = (sigma0(a) + maj(a,b,c)) & 0xFFFFFFFF
            h0, g0, f, e, d, c, b, a = g0, f, e, (d+T1)&0xFFFFFFFF, c, b, a, (T1+T2)&0xFFFFFFFF
            # trace only on first block
            if block_index == 0 and i == 13:
                print(f"🔍 Round 13 State (block 0):")
                print(f"  a13 = 0x{a:08X}")
                print(f"  b13 = 0x{b:08X}")
                print(f"  c13 = 0x{c:08X}")
                print(f"  d13 = 0x{d:08X}")
        # update hash values
        h = [
            (h[0] + a) & 0xFFFFFFFF,
            (h[1] + b) & 0xFFFFFFFF,
            (h[2] + c) & 0xFFFFFFFF,
            (h[3] + d) & 0xFFFFFFFF,
            (h[4] + e) & 0xFFFFFFFF,
            (h[5] + f) & 0xFFFFFFFF,
            (h[6] + g0) & 0xFFFFFFFF,
            (h[7] + h0) & 0xFFFFFFFF
        ]
    # produce digest
    digest = b''.join(struct.pack('>I', word) for word in h)
    print(f"\n✅ Computed SHA-256 Hash: {digest.hex()}")

if __name__ == '__main__':
    hex_input = input("📥 Enter your hex-encoded message: ").strip()
    try:
        data = bytes.fromhex(hex_input)
    except ValueError:
        print("❌ Invalid hex input.")
        sys.exit(1)
    demo_sha256(data)