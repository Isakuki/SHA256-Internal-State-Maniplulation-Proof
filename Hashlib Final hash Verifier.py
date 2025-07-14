import hashlib

# Ask user for hex input
hex_input = input("Enter hex string: ")

# Calculate SHA256 hash
hash_result = hashlib.sha256(bytes.fromhex(hex_input)).hexdigest()

# Print the output
print(f"From Python hash library SHA256 final hash: {hash_result}")