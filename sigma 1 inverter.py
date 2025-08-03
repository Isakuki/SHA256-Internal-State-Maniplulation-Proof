#!/usr/bin/env python3
"""
SHA-256 Sigma1 Function Complete Inverter
Demonstrates that Sigma1 is perfectly invertible using linear algebra over GF(2)
"""

def rotr32(x, n):
    """32-bit right rotation"""
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def sigma1(x):
    """SHA-256 Sigma1 function: ROTR(x,6) ⊕ ROTR(x,11) ⊕ ROTR(x,25)"""
    return rotr32(x, 6) ^ rotr32(x, 11) ^ rotr32(x, 25)

def build_transformation_matrix():
    """Build the 32x32 transformation matrix for Sigma1 over GF(2)"""
    matrix = [[0 for _ in range(32)] for _ in range(32)]
    
    # For each output bit position
    for output_bit in range(32):
        # Test each input bit to see if it affects this output bit
        for input_bit in range(32):
            test_input = 1 << input_bit
            output = sigma1(test_input)
            
            if output & (1 << output_bit):
                matrix[output_bit][input_bit] = 1
    
    return matrix

def invert_matrix_gf2(matrix):
    """Invert a matrix over GF(2) using Gaussian elimination"""
    n = len(matrix)
    
    # Create augmented matrix [A | I]
    augmented = []
    for i in range(n):
        row = matrix[i][:] + [1 if i == j else 0 for j in range(n)]
        augmented.append(row)
    
    # Gaussian elimination
    for i in range(n):
        # Find pivot
        pivot = -1
        for j in range(i, n):
            if augmented[j][i] == 1:
                pivot = j
                break
        
        if pivot == -1:
            raise ValueError("Matrix is not invertible")
        
        # Swap rows if needed
        if pivot != i:
            augmented[i], augmented[pivot] = augmented[pivot], augmented[i]
        
        # Eliminate
        for j in range(n):
            if j != i and augmented[j][i] == 1:
                for k in range(2 * n):
                    augmented[j][k] ^= augmented[i][k]
    
    # Extract inverse matrix from right side
    inverse = []
    for i in range(n):
        inverse.append(augmented[i][n:])
    
    return inverse

def apply_matrix_gf2(matrix, input_bits):
    """Apply matrix multiplication over GF(2)"""
    result = [0] * 32
    
    for row in range(32):
        sum_bit = 0
        for col in range(32):
            sum_bit ^= (matrix[row][col] & input_bits[col])
        result[row] = sum_bit
    
    return result

def number_to_bits(num):
    """Convert 32-bit number to bit array (LSB first)"""
    return [(num >> i) & 1 for i in range(32)]

def bits_to_number(bits):
    """Convert bit array to 32-bit number (LSB first)"""
    return sum(bit << i for i, bit in enumerate(bits)) & 0xFFFFFFFF

class Sigma1Inverter:
    """Complete Sigma1 inversion system"""
    
    def __init__(self):
        print("Building Sigma1 transformation matrix...")
        self.transform_matrix = build_transformation_matrix()
        
        print("Computing inverse matrix...")
        self.inverse_matrix = invert_matrix_gf2(self.transform_matrix)
        
        print("✅ Sigma1 inverter ready!")
    
    def invert(self, target_output):
        """Find the input that produces the given Sigma1 output"""
        output_bits = number_to_bits(target_output)
        input_bits = apply_matrix_gf2(self.inverse_matrix, output_bits)
        return bits_to_number(input_bits)
    
    def verify(self, input_val, expected_output):
        """Verify that input produces expected output"""
        actual_output = sigma1(input_val)
        return actual_output == expected_output

def main():
    """Demonstration and testing with full round-trip verification"""
    print("SHA-256 Sigma1 Round-Trip Inversion Test")
    print("=" * 50)
    
    # Initialize the inverter
    inverter = Sigma1Inverter()
    
    print("\n🔄 ROUND-TRIP TESTS: Random Input -> Sigma1 -> Invert -> Sigma1 -> Verify")
    print("=" * 80)
    
    import random
    success_count = 0
    total_tests = 10
    
    for test_num in range(total_tests):
        print(f"\n📊 TEST {test_num + 1}:")
        print("-" * 20)
        
        # Step 1: Generate random input
        original_input = random.randint(0, 0xFFFFFFFF)
        print(f"1. Random input:        0x{original_input:08X}")
        
        # Step 2: Apply Sigma1 to get output
        sigma1_output = sigma1(original_input)
        print(f"2. Sigma1(input):       0x{sigma1_output:08X}")
        
        # Step 3: Use our inversion logic to find input from output
        inverted_input = inverter.invert(sigma1_output)
        print(f"3. Inverted input:      0x{inverted_input:08X}")
        
        # Step 4: Apply Sigma1 to inverted input to verify
        final_output = sigma1(inverted_input)
        print(f"4. Sigma1(inverted):    0x{final_output:08X}")
        
        # Step 5: Check if everything matches
        input_matches = (original_input == inverted_input)
        output_matches = (sigma1_output == final_output)
        perfect_roundtrip = input_matches and output_matches
        
        print(f"\n🔍 VERIFICATION:")
        print(f"   Original input  == Inverted input:  {input_matches} {'✅' if input_matches else '❌'}")
        print(f"   Original output == Final output:    {output_matches} {'✅' if output_matches else '❌'}")
        print(f"   Perfect round-trip:                 {perfect_roundtrip} {'✅' if perfect_roundtrip else '❌'}")
        
        if perfect_roundtrip:
            success_count += 1
            print(f"   ✅ SUCCESS: Complete round-trip verified!")
        else:
            print(f"   ❌ FAILURE: Round-trip broken!")
            
            if not input_matches:
                diff = original_input ^ inverted_input
                print(f"      Input difference (XOR): 0x{diff:08X}")
                print(f"      Different bits: {bin(diff).count('1')}")
            
            if not output_matches:
                diff = sigma1_output ^ final_output
                print(f"      Output difference (XOR): 0x{diff:08X}")
                print(f"      Different bits: {bin(diff).count('1')}")
    
    print(f"\n" + "=" * 50)
    print(f"FINAL RESULTS")
    print("=" * 50)
    print(f"Perfect round-trips: {success_count}/{total_tests} ({success_count/total_tests*100:.1f}%)")
    
    if success_count == total_tests:
        print("\n🚀 ALL ROUND-TRIP TESTS PASSED!")
        print("✅ Every random input was perfectly recovered through inversion")
        print("✅ Sigma1 is confirmed to be a perfect bijection")
        print("✅ Our inversion algorithm is mathematically sound")
        print("\n💡 CRYPTOGRAPHIC IMPLICATIONS:")
        print("   • Sigma1 creates NO barrier to algebraic attacks")
        print("   • Can replace every Sigma1(x) with linear algebra")
        print("   • SHA-256 constraint systems become much simpler")
        print("   • Round 20+ control becomes feasible!")
    else:
        print(f"\n⚠️  {total_tests - success_count} round-trip tests FAILED!")
        print("❌ There are errors in our inversion implementation")
        print("❌ Sigma1 inversion needs debugging")
        
    print("\n🎯 BONUS: Testing your original example")
    print("-" * 30)
    target = 0x6A3F1FED
    found_input = inverter.invert(target)
    verification = sigma1(found_input)
    matches = verification == target
    
    print(f"Target output:    0x{target:08X}")
    print(f"Found input:      0x{found_input:08X}")
    print(f"Verification:     0x{verification:08X}")
    print(f"Matches:          {matches} {'✅' if matches else '❌'}")

def interactive_test():
    """Interactive testing function"""
    print("\n" + "=" * 50)
    print("INTERACTIVE SIGMA1 INVERTER")
    print("=" * 50)
    
    inverter = Sigma1Inverter()
    
    while True:
        try:
            user_input = input("\nEnter target Sigma1 output (hex, e.g., 0x6A3F1FED) or 'quit': ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            # Parse hex input
            if user_input.startswith('0x') or user_input.startswith('0X'):
                target = int(user_input, 16)
            else:
                target = int(user_input, 16)
            
            target &= 0xFFFFFFFF  # Ensure 32-bit
            
            print(f"\nTarget: 0x{target:08X}")
            
            # Find input
            found_input = inverter.invert(target)
            print(f"Found input: 0x{found_input:08X}")
            
            # Verify
            verification = sigma1(found_input)
            success = verification == target
            
            print(f"Verification: 0x{verification:08X}")
            print(f"Success: {'YES ✅' if success else 'NO ❌'}")
            
            if success:
                print(f"✅ Sigma1(0x{found_input:08X}) = 0x{target:08X}")
            else:
                print(f"❌ Expected 0x{target:08X}, got 0x{verification:08X}")
                
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
    
    print("Goodbye!")

if __name__ == "__main__":
    main()
    
    # Uncomment the line below for interactive testing
    # interactive_test()

