import main



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

instrs = main.reverseCompiler('binary_branch.txt')

labels = {0: 'main'}

print(instrs)

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