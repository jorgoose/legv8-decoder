

#----------------------------------
# INSTRUCTION TO OPCODE DICTIONARY
#----------------------------------

instruction_to_format = {
    "ADD": "R",
    "ADDI": "I",
    "AND": "R",
    "ANDI": "I",
    "B": "B",
    "B.cond": "CB",
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

#----------------------------------
# BINARY TO CONDITION DICTIONARY
#----------------------------------

binary_to_condition = {
    "00000": "EQ",
    "00001": "NE",
    "00010": "HS",
    "00011": "LO",
    "00100": "MI",
    "00101": "PL",
    "00110": "VS",
    "00111": "VC",
    "01000": "HI",
    "01001": "LS",
    "01010": "GE",
    "01011": "LT",
    "01100": "GT",
    "01101": "LE",
}

#------------------
# REVERSE COMPILER
#------------------

def reverseCompiler(filename):

    leg_result = []

    instructions = readFile(filename)

    for instruction in instructions:

        # If the instruction is of type R, decode it using the R decoder
        if (instruction_to_format[opcodeToInstruction(instruction)] == "R"):
            leg_result.append(instructionTypeR(instruction))
            
        # If the instruction is of type I, decode it using the I decoder
        elif (instruction_to_format[opcodeToInstruction(instruction)] == "I"):
            leg_result.append(instructionTypeI(instruction))

        # If the instruction is of type D, decode it using the D decoder
        elif (instruction_to_format[opcodeToInstruction(instruction)] == "D"):
            leg_result.append(instructionTypeD(instruction))

        # If the instruction is of type B, decode it using the B decoder
        elif (instruction_to_format[opcodeToInstruction(instruction)] == "B"):
            leg_result.append(instructionTypeB(instruction))

        # If the instruction is of type CB, decode it using the CB decoder
        elif (instruction_to_format[opcodeToInstruction(instruction)] == "CB"):
            leg_result.append(instructionTypeCB(instruction))

        # Otherwise, the instruction is not supported
        else:
            print("Unknown instruction type: " + instruction)

    return leg_result

# ---------------------------
# READ FILE (TEXT OR BINARY)
# ---------------------------

# Read in .txt file of binary code and split it into a list of instructions, 
#   with each line being an instruction
# This also works for binary files, as the data for each instruction is stored in a list of 32 bits as a string,
#   and calling the splitlines() function on a binary file will split it into a list of 32 bit strings.
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
    elif (binary.find("01010100") == 0):
        return "B.cond"
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

# Decodes binary of type R
# opcode, Rm, shamt, Rn, Rd
# 31-21 20-16 15-10 9-5 4-0
def instructionTypeR(binary):
    instruction = opcodeToInstruction(binary)
    Rm = binary[11:16]
    shamt = binary[16:22]
    Rn = binary[22:27]
    Rd = binary[27:32]

    # Special case for HALT
    if (instruction == "HALT"):
        return "HALT"
    # Special case for BR
    elif (instruction == "BR" or instruction == "PRNT"):
        res = "BR X" + str(int(Rn, 2))
        return res
    elif (instruction == "LSL" or instruction == "LSR"):
        return instruction + " X" + str(int(Rd, 2)) + ", X" + str(int(Rn, 2)) + ", #" + str(int(shamt, 2))
    else:
        return instruction + " X" + str(int(Rd, 2)) + ", X" + str(int(Rn, 2)) + ", X" + str(int(Rm, 2))

# Decodes binary of type I
# opcode, imm12, Rn, Rd
# 31-21 20-10 9-5 4-0
def instructionTypeI(binary):
    instruction = opcodeToInstruction(binary)
    imm12 = binary[10:22]
    Rn = binary[22:27]
    Rd = binary[27:32]

    imm12_converted = convert_twos_complement(imm12)

    # Return the instruction in the format of the instruction name, followed by the destination register, 
    # followed by the source register, followed by the immediate value
    return instruction + " X" + str(int(Rd, 2)) + ", X" + str(int(Rn, 2)) + ", #" + str(imm12_converted)

# Decodes binary of type D
# opcode, dt, op, Rn, Rt
# 31-21 20-12 11-10 9-5 4-0
def instructionTypeD(binary):
    instruction = opcodeToInstruction(binary)
    dt = binary[11:20]
    op = binary[20:22]
    Rn = binary[21:27]
    Rt = binary[27:32]

    dt_converted = convert_twos_complement(dt)

    # Return the instruction in the format of the instruction name, followed by the target register,
    # followed by the source register, followed by the offset
    return instruction + " X" + str(int(Rt, 2)) + ", [X" + str(int(Rn, 2)) + ", #" + str(dt_converted) + "]"

# Decodes binary of type B
# opcode, addr
# 31-26 25-0
def instructionTypeB(binary):

    # Add B instruction condition code handling
    instruction = opcodeToInstruction(binary)
    addr = binary[6:32]

    addr_converted = convert_twos_complement(addr)

    # Return the instruction and the offset of instruction to branch to
    res = instruction + " " + str(addr_converted)

    return res

# Decodes binary of type CB
# opcode, addr, Rt
def instructionTypeCB(binary):
    instruction = opcodeToInstruction(binary)
    addr = binary[8:27]
    Rt = binary[27:32]

    addr_converted = convert_twos_complement(addr)

    if instruction == "B.cond":
        res = "B."+ binary_to_condition[Rt] + " " + str(addr_converted)
    else:
        # Return the instruction and the address of instruction to branch to
        res = instruction + " X" + str(int(Rt, 2)) + " " + str(addr_converted)

    return res

# ---------------
# LABEL GENERATOR
# ---------------

def generateLabels(leg_instructions):

    # Key: address --> Value: label name
    labels = {}

    for i in range(len(leg_instructions)):
        if (leg_instructions[i].find("B") == 0 or leg_instructions[i].find("C") == 0) and leg_instructions[i].find("BR") != 0:

            offset = leg_instructions[i].split(" ")[-1]
            branch_to = i + int(offset) + 1

            if (branch_to not in labels):
                new_label = "label_" + str(len(labels) + 1)
                labels[branch_to] = new_label
        
    return labels

# ---------------
# INJECT LABELS
# ---------------

def injectLabels(leg_instructions, labels):

    # List to store all of the lines of the final assembly code
    final_result = []

    for i in range(len(leg_instructions)):

        # Handle label injection for label locations
        if (i in labels):
            final_result.append(labels[i] + ":")

        # Handle label injection for B instructions
        if (
            (leg_instructions[i].find("B") == 0 or leg_instructions[i].find("C") == 0) and
            leg_instructions[i].find("BR") != 0 and i + int(leg_instructions[i].split(" ")[-1]) + 1 in labels
            ):

            instr = leg_instructions[i].split(" ")[0]
            label = labels[i + int(leg_instructions[i].split(" ")[-1]) + 1]

            final_result.append(instr + " " + label)

        # If there's no label to handle, just append the instruction
        else: 
            final_result.append(leg_instructions[i])

    
    # Finally, if there is a label at the end of the program, add it to the result
    if (len(leg_instructions) in labels):
        final_result.append(labels[len(leg_instructions)] + ":")

    return final_result

# ----------------------------
# TWO'S COMPLEMENT CONVERSION
# ----------------------------

# Convert a string of a signed two's complement binary number into an integer
def convert_twos_complement(binary):
    if binary[0] == '0':
        return int(binary, 2)
    else:
        return int(binary, 2) - (1 << len(binary))

# -----
# MAIN
# -----

def main():

    # Get the filepath of the file to decode from the user
    # ----------------------------------------------------
    filepath = input("Enter the filename of the file you would like to decode: ")

    # Display the original binary code to the user
    # --------------------------------------------
    print("Original Binary Code: ")
    print("---------------------")
    file = open(filepath, "r")
    instructions = file.read().splitlines()
    for instruction in instructions:
        print(instruction)
    print("---------------------")
    print("")

    # Display the converted LEGv8 code to the user
    # ---------------------------------------------
    print("Converted to LegV8 Code: ")
    print("---------------------")

    # Convert the binary instructions to LEGv8 instructions
    instrs = reverseCompiler(filepath)

    # Generate labels for the instruction set
    labels = generateLabels(instrs)

    # # Inject the labels into the instruction set and print the final result
    final_result = injectLabels(instrs, labels)
    for line in final_result : print(line)

# Call main method if this file is run as a script
if __name__ == '__main__':
    main()