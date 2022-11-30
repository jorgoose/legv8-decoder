import main

print("--- Test Start ---")

# EXAMPLE 1
# ==================================================

# Example ADD instruction (R format)
# ADD X9, X20, X21
ex1 = "10001011000101010000001010001001" 

print("Input: " + ex1)

# Expected: ADD
print("Expected Instruction: ADD")


print("Actual:", main.opcodeToInstruction(ex1))

# Expected: ADD X9, X20, X21
print("Expected Output: ADD X9, X20, X21")

print("Actual:", main.instructionTypeR(ex1))
print("------------------")
# ==================================================

# EXAMPLE 2
# ==================================================
# Example ADDI instruction (I format)
# ADDI X9, X20, #5
# ex2 = "10001010000-000000000101-10100-01001"
ex2 = "10010001000000000001011010001001"

print("Input: " + ex2)

# Expected: ADDI
print("Expected Instruction: ADDI")

print("Actual:", main.opcodeToInstruction(ex2))

# Expected: # ADDI X9, X20, #5
print("Expected Output: ADDI X9, X20, #5")

print("Actual:", main.instructionTypeI(ex2))
print("------------------")
# ==================================================

# EXAMPLE 3
# ==================================================
# Example LDUR instruction (D format)
# LDUR X9, [X20, #5]

# LDUR opcode: 11111000010
# ex3 = "1111100001-00000101-00-10100-01001"
ex3 = "11111000010000000101001010001001"

print("Input: " + ex3)

# Expected: LDUR
print("Expected Instruction: LDUR")

print("Actual:", main.opcodeToInstruction(ex3))

# Expected: LDUR X9, [X20, #5]
print("Expected Output: LDUR X9, [X20, #5]")

print("Actual:", main.instructionTypeD(ex3))
