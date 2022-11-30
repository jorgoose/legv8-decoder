
import util


# Pre-Code Notes:
# PROBLEM 1: Need to come up with a way to handle branching instructions. I think I can do this the following way:
#   Since we are decoding the binary in the order at which it is processed by the computer, that means when 
#   a branch instruction is encountered, we know the following binary up until BR LR or another branch is made is its own subset.
#   So, we can just store the address of the initial branch instruction and the address to branch to in a dictionary. 
#   Then, when we are done decoding the binary, we can go through the dictionary and replace the branch instruction with the address to branch to.
#
# Ex 1:
# 0     BL label          // label address gets stored to link register
# 1     ...
# 2     ...              // Arbitrary code that is not part of the  "label" procedure
# 3     label:
# 4     ADDI X0, X0, 1   // This is the instruction associated with the label
# 5     BR LR            // Return to the address stored in the link register
#
# Execution order in binary:
# 0, 3, 4, 5, 1, 2

# Ex 2:
# 0     B label          // label address gets stored to link register
# 1     ...
# 2     ...              // Abritrary code
# 3     label:
# 4     ADDI X0, X0, 1   // This is the instruction associated with the label
#
# Execution order in binary:
# 0, 3, 4
# 0, (new procedure discovered)

# My Solution: Store the instructions of each procedure call individually, each with an associated label

# To keep track of procedures and instructions, use a dictionary where each entry essentially represents a procedure
# Each key is the address of the first instruction in the procedure, 
# and the associated value is a list of instructions associated with that procedure

# Procedure --> Associated Instructions
procedures = {0: []}
labels = {0: 'main'}

registers = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0, 31: 0}

global currentProcedureAddr
currentProcedureAddr = 0

#----------------------------------
# INSTRUCTION TO OPCODE DICTIONARY
#----------------------------------

format = {
    "ADD": "R",
    "ADDI": "I",
    "AND": "R",
    "ANDI": "I",
    "B": "B",
    "BL": "B",
    "BR": "R",
    "CBNZ": "CB",
    "CBZ": "CB",
    "EOR": "R",
    "EORI": "I",
    "LDUR": "D",
    "LSL": "R",
    "LSR": "R",
    "ORR": "R",
    "ORRI": "I",
    "STUR": "D",
    "SUB": "R",
    "SUBI": "I",
    "SUBIS": "I",
    "SUBS": "R",
    "MUL": "R",
    "PRNT": "R",
    "PRNL": "R",
    "DUMP": "R",
    "HALT": "R"
}

#------------------
# REVERSE COMPILER
#------------------

def reverseCompiler(filename):

    global currentProcedureAddr

    instructions = readFile(filename)
    for instruction in instructions:

        leg_result = []

        # If the instruction is of type R, decode it using the R decoder
        if (format[opcodeToInstruction(instruction)] == "R"):

            # Special case for BR
            if(opcodeToInstruction(instruction) == "BR"):

                res_and_addr = instructionTypeR(instruction)
                res = res_and_addr[0]
                addr = res_and_addr[1]
                
                leg_result.append(res)

                # Add the branch instruction to the current procedure
                procedures[currentProcedureAddr].append(leg_result)

                currentProcedureAddr = addr
                continue

            else:
                leg_result.append(instructionTypeR(instruction))

        # If the instruction is of type I, decode it using the I decoder
        elif (format[opcodeToInstruction(instruction)] == "I"):
            leg_result.append(instructionTypeI(instruction))

        # If the instruction is of type D, decode it using the D decoder
        elif (format[opcodeToInstruction(instruction)] == "D"):
            leg_result.append(instructionTypeD(instruction))

        # If the instruction is of type B, decode it using the B decoder
        elif (format[opcodeToInstruction(instruction)] == "B"):

                res_and_addr = instructionTypeB(instruction)
                res = res_and_addr[0]
                addr = res_and_addr[1]

                leg_result.append(res)

                # Add the branch instruction to the current procedure
                procedures[currentProcedureAddr].append(leg_result)
    
                # Update the current procedure address to where the branch instruction is pointing to
                currentProcedureAddr = addr

                continue

        # If the instruction is of type CB, decode it using the CB decoder
        elif (format[opcodeToInstruction(instruction)] == "CB"):
           leg_result.append(instructionTypeCB(instruction))

        # Otherwise, the instruction is not supported
        else:
            print("Unknown instruction type: " + instruction)

        # Add the decoded instruction to the list of instructions associated with the current procedure
        procedures[currentProcedureAddr].append(leg_result)

    return procedures

# -----------------------
# READ FILE LINE BY LINE
# -----------------------

# Read in .txt file of binary code and split it into a list of instructions, 
# with each line being an instruction
def readFile(filename):
    file = open(filename, "r")
    instructions = file.read().splitlines()
    file.close()
    return instructions

# ------------------------------------
# EXTRACT INSTRUCTION BASED ON OPCODE
# ------------------------------------

# Gets the operation of a given instruction
def opcodeToInstruction(binary):

    if (binary.find("10001011000") == 0):
        return "ADD"
    elif (binary.find("1001000100") == 0):
        return "ADDI"
    elif (binary.find("10001010000") == 0):
        return "AND"
    elif (binary.find("1001001000") == 0):
        return "ANDI"
    elif (binary.find("000101") == 0):
        return "B"
    elif (binary.find("100101") == 0):
        return "BL"
    elif (binary.find("11010110000") == 0):
        return "BR"
    elif (binary.find("10110101") == 0):
        return "CBNZ"
    elif (binary.find("10110100") == 0):
        return "CBZ"
    elif (binary.find("11001010000") == 0):
        return "EOR"
    elif (binary.find("1101001000") == 0):
        return "EORI"
    elif (binary.find("11111000010") == 0):
        return "LDUR"
    elif (binary.find("11010011011") == 0):
        return "LSL"
    elif (binary.find("11010011010") == 0):
        return "LSR"
    elif (binary.find("10101010000") == 0):
        return "ORR"
    elif (binary.find("1011001000") == 0):
        return "ORRI"
    elif (binary.find("11111000000") == 0):
        return "STUR"
    elif (binary.find("11001011000") == 0):
        return "SUB"
    elif (binary.find("1101000100") == 0):
        return "SUBI"
    elif (binary.find("1111000100") == 0):
        return "SUBIS"
    elif (binary.find("11101011000") == 0):
        return "SUBS"
    elif (binary.find("10011011000") == 0):
        return "MUL"
    elif (binary.find("11111111101") == 0):
        return "PRNT"
    elif (binary.find("11111111100") == 0):
        return "PRNL"
    elif (binary.find("11111111110") == 0):
        return "DUMP"
    elif (binary.find("11111111111") == 0):
        return "HALT"
    else:
        return "Unknown Opcode: " + binary


# --------------------------
# INSTRUCTION TYPE DECODERS
# --------------------------

# COMPLETE
# Decodes binary of type R
# R-type instructions
# opcode, Rm, shamt, Rn, Rd
# 31-21 20-16 15-10 9-5 4-0
def instructionTypeR(binary):
    instruction = opcodeToInstruction(binary)
    Rm = binary[11:16]
    shamt = binary[16:22]
    Rn = binary[22:27]
    Rd = binary[27:32]

    # Special case for BR
    if (instruction == "BR"):
        res = "BR X" + str(int(Rd, 2))
        addr = int(Rd, 2)
        return res, addr
    elif (int(shamt, 2) == 0):
        return instruction + " X" + str(int(Rd, 2)) + ", X" + str(int(Rn, 2)) + ", X" + str(int(Rm, 2))
    else:
        return instruction + " X" + str(int(Rd, 2)) + ", X" + str(int(Rn, 2)) + ", #" + str(int(shamt, 2))

# TODO Test for correctness and completeness
# Decodes binary of type I
# opcode, imm12, Rn, Rd
# 31-21 20-10 9-5 4-0
def instructionTypeI(binary):
    instruction = opcodeToInstruction(binary)
    imm12 = binary[10:22]
    Rn = binary[22:27]
    Rd = binary[27:32]

    # Return the instruction in the format of the instruction name, followed by the destination register, 
    # followed by the source register, followed by the immediate value
    return instruction + " X" + str(int(Rd, 2)) + ", X" + str(int(Rn, 2)) + ", #" + str(int(imm12, 2))

# TODO Test for correctness and completeness
# Decodes binary of type D
# opcode, dt, op, Rn, Rt
# 31-21 20-12 11-10 9-5 4-0
def instructionTypeD(binary):
    instruction = opcodeToInstruction(binary)
    dt = binary[11:20]
    op = binary[20:22]
    Rn = binary[21:27]
    Rt = binary[27:32]

    # Return the instruction in the format of the instruction name, followed by the target register,
    # followed by the source register, followed by the offset
    return instruction + " X" + str(int(Rt, 2)) + ", [X" + str(int(Rn, 2)) + ", #" + str(int(dt, 2)) + "]"

# Decodes binary of type B
# opcode, addr
# 31-26 25-0
def instructionTypeB(binary):

    # Add B instruction condition code handling
    instruction = opcodeToInstruction(binary)
    addr = binary[6:32]

    # Return the instruction and the address of instruction to branch to
    res = instruction + " #" + str(int(addr, 2))

    return res

# TODO
# Decodes binary of type CB
# opcode, addr, Rt
def instructionTypeCB(binary):
    # TODO
    instruction = opcodeToInstruction(binary)
    return ""

# -----
# MAIN
# -----

def main():
    
    print("Binary Code: ")
    # Open a file and print each line in the file
    file = open('binary_branch.txt', "r")
    instructions = file.read().splitlines()
    for instruction in instructions:
        print(instruction)
        # print(main.opcodeToInstruction(instruction))
        # print(main.format[main.opcodeToInstruction(instruction)])
        # print("")
    print("------------------")
    print("")
    print("Converted to LegV8 Code: ")

    instrs = reverseCompiler('binary_branch.txt')

    labels = {0: 'main'}

    print(instrs)

    # Convert each procedure address to a generic label, and add the label to the list of labels
    # Then, print the newly generated label and the instructions in the procedure
    for proc in instrs:

        if proc not in labels:
            labels[proc] = 'procedure_' + str(len(labels) - 1)

        print(labels[proc] + ':')

        for instr in instrs[proc]:

            proc_addr = int(instr[0][-1])

            if(instr[0][0] == 'B' and proc_addr not in labels):
                labels[proc_addr] = 'procedure_' + str(len(labels) - 1)
                print(instr[0].split(' ')[0] + ' ' + labels[proc_addr])
            else:
                print(instr[0])

# Call main method if this file is run as a script
if __name__ == '__main__':
    main()

