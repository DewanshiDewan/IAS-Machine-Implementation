Memory = [
    '0000000100000000010000001111000000000010',  # load a, cond. jump left to pc=2
    # add a+b, store(a+b) to c(pc=6)
    '0000010100000000010100100001000000000110',
    # sub a-b, store(a-b) to c(pc=6)
    '0000011000000000010100100001000000000110',
    '0000000000000000000000000000000000000000',  # halt
    '0000000000000000000000000000000000001111',  # a=15
    '0000000000000000000000000000000000000101',  # b=5
]

inst_dic = {
    '00100001': 'stor m(x)',
    '00000001': 'load m(x)',
    '00000010': 'load -m(x)',
    '00000011': 'load |m(x)|',
    '00001101': 'jump m(x,0:19)',
    '00001110': 'jump m(x,20:39)',
    '00001111': 'jump + m(x,0:19)',
    '00010000': 'jump + m(x,20:39)',
    '00000101': 'add m(x)',
    '00000111': 'add |m(x)|',
    '00000110': 'sub m(x)',
    '00001000': 'sub |m(x)|',
    '00010100': 'lsh',
    '00010101': 'rsh',
    '00000000': 'hlt'
}


def BtoD(data):  # BtoD is binary to decimal function
    return int(data, 2)  # bin works on string inputs


def DtoB(data):  # DtoB is decimal to binary function
    return str(bin(data).replace("0b", ""))


# setting initial values of the flags and the registers
PC = '000000000000'  # 12 bits
AC = '0000000000000000000000000000000000000000'  # 40 bits
MAR = '000000000000'  # 12 bits
IR = '00000000'  # 8 bits
IBR = '00000000000000000000'  # 20 bits
flag = True  # is true till we don't encounter the halt opcode
# is true till we have to execute the left instruction(which exists)
inst_set = 'Left'


while(flag):
    print('flag is true')
    if(inst_set == 'Left'):
        print('Inside inst_set as LEFT')

        MAR = PC
        mar = BtoD(MAR)
        MBR = Memory[mar][0:40]  # 40 bit instruction fetch

        if(MBR[0:20] != ' '*20):  # left and right instructions exist
            to_Be_Processed = True
            MAR = MBR[8:20]  # location of data in memory
            IR = MBR[0:8]  # opcode
            IBR = MBR[20:40]  # right instruction
            data_address = BtoD(MAR)
            print('To be processed is TRUE')

        else:  # only right instruction exists
            inst_set = 'Right'
            to_Be_Processed = False
            IR = MBR[20:28]
            MAR = MBR[28:40]
            data_address = BtoD(MAR)
            print('To be processed is FALSE')

        # to execute the left instruction before the right instruction if it exists
        if (to_Be_Processed == True):
            print('Processing codeblock when To be processed is  TRUE')

            # value = ir, key = IR(opcode fetched from the instruction)
            ir = inst_dic[IR]
            print('Printing ir in the LEFT', ir)

            # DECODE and EXECUTE cycle
            if(ir == 'load m(x)'):  # load m(x)
                inst_set = 'Right'
                AC = Memory[data_address]

            elif(ir == 'load -m(x)'):  # load -m(x)
                inst_set = 'Right'
                if(Memory[data_address][0] == '1'):
                    AC = '0' + Memory[data_address][1:40]
                else:
                    AC = '1' + Memory[data_address][1:40]

            elif(ir == 'load |m(x)|'):  # load |m(x)|
                inst_set = 'Right'
                AC = '0' + Memory[data_address][1:40]

            elif(ir == 'stor m(x)'):  # stor m(x)
                inst_set = 'Right'
                Memory.insert(data_address, AC)
                print('Memory [' + str(data_address) +
                      '] = ' + Memory[data_address])

            elif(ir == 'jump m(x,0:19)'):  # jump m(x, 0:19)
                PC = MAR
                inst_set = 'Left'
                print('Jump encountered')

            elif(IR == 'jump m(x,20:39)'):  # jump m(x, 20:39)
                PC = MAR
                inst_set = 'Right'
                to_Be_Processed = False
                print('Jump encountered')

            elif(ir == 'jump + m(x,0:19)'):  # jump+m(x, 0:19)
                if(AC[0] == '0'):  # value in accumulator is non-negative
                    PC = MAR
                    inst_set = 'Left'
                    print('Jump encountered')
                else:
                    inst_set = 'Right'

            elif(ir == 'jump + m(x,20:39)'):  # jump+m(x, 20:39)
                if(AC[0] == '0'):  # value in accumulator is non-negative
                    PC = MAR
                    inst_set = 'Left'
                    to_Be_Processed = False
                    print('Jump encountered')
                else:
                    # since we are at the left instruction, hence we want to go to the right instruction next
                    inst_set = 'Right'

            elif(ir == 'add m(x)'):  # add m(x)
                inst_set = 'Right'
                signAC = 1
                signMX = 1
                if(AC[0] == '1'):
                    signAC = -1
                if(Memory[data_address][0] == '1'):
                    signMX = -1
                ac = BtoD(AC[1:40])
                mx = BtoD(Memory[data_address][1:40])
                ac = signAC*ac + signMX*mx
                if(ac < 0):
                    AC = '1' + '0'*(39 - len(DtoB(-1*ac))) + DtoB(-1*ac)
                else:
                    AC = '0' + '0'*(39 - len(DtoB(ac))) + DtoB(ac)
                # '0'*(39 - len(DtoB(ac))) is added to convert the answet to a 40 bit binary for Memory

            elif(ir == 'add |m(x)|'):  # add |m(x)|
                inst_set = 'Right'
                signAC = 1
                if(AC[0] == '1'):
                    signAC = -1
                ac = BtoD(AC[1:40])
                mx = BtoD(Memory[data_address][1:40])
                ac = signAC*ac + mx
                if(ac < 0):
                    AC = '1' + '0'*(39 - len(DtoB(-1*ac))) + DtoB(-1*ac)
                else:
                    AC = '0' + '0'*(39 - len(DtoB(ac))) + DtoB(ac)

            elif(ir == 'sub m(x)'):  # sub m(x)
                inst_set = 'Right'
                signAC = 1
                signMX = 1
                if(AC[0] == '1'):
                    signAC = -1
                if(Memory[data_address][0] == '1'):
                    signMX = -1
                ac = BtoD(AC[1:40])
                mx = BtoD(Memory[data_address][1:40])
                ac = signAC*ac - (signMX*mx)
                if(ac < 0):
                    AC = '1' + '0'*(39 - len(DtoB(-1*ac))) + DtoB(-1*ac)
                else:
                    AC = '0' + '0'*(39 - len(DtoB(ac))) + DtoB(ac)

            elif(ir == 'sub |m(x)|'):  # sub |m(x)|
                inst_set = 'Right'
                signAC = 1
                if(AC[0] == '1'):
                    signAC = -1
                if(Memory[data_address][0] == '1'):
                    signMX = -1
                ac = BtoD(AC[1:40])
                mx = BtoD(Memory[data_address][1:40])
                ac = signAC*ac - mx
                if(ac < 0):
                    AC = '1' + '0'*(39 - len(DtoB(-1*ac))) + DtoB(-1*ac)
                else:
                    AC = '0' + '0'*(39 - len(DtoB(ac))) + DtoB(ac)

            elif(ir == 'lsh'):  # lsh
                inst_set = 'Right'
                signAC = 1
                if(AC[0] == '1'):
                    signAC = -1
                ac = BtoD(AC[1:40])
                ac = 2*signAC*ac
                if(ac < 0):
                    AC = '1' + '0'*(39 - len(DtoB(-1*ac))) + DtoB(-1*ac)
                else:
                    AC = '0' + '0'*(39 - len(DtoB(ac))) + DtoB(ac)

            elif(ir == 'rsh'):  # rsh
                inst_set = 'Right'
                signAC = 1
                if(AC[0] == '1'):
                    signAC = -1
                ac = BtoD(AC[1:40])
                ac = signAC*int(ac/2)
                if(ac < 0):
                    AC = '1' + '0'*(39 - len(DtoB(-1*ac))) + DtoB(-1*ac)
                else:
                    AC = '0' + '0'*(39 - len(DtoB(ac))) + DtoB(ac)

            elif(ir == 'hlt'):  # halt
                print('Inside HALT condition')
                IR = '00000000'
                flag = False
                print('Program halted as per instruction!')
                break
        x = input('We have reviewed the parameters. Now press any key to continue...')

    if(inst_set == 'Right' or to_Be_Processed == False):  # right instruction execution
        print('Inst_set is RIGHT or To be processed is TRUE')
        IR = IBR[0:8]  # location of data in memory
        MAR = IBR[8:20]  # opcode
        data_address = BtoD(MAR)
        print('printing IR = ' + IR + ' and MAR = ' + MAR)

        pc = BtoD(PC)
        # pc is incremented after the instruction fetch is complete
        PC = DtoB(pc+1)

        # value = ir, key = IR(opcode fetched from the instruction)
        ir = inst_dic[IR]
        print('Printing ir ==', ir)

        # DECODE and EXECUTE cycle
        if(ir == 'load m(x)'):  # load m(x)
            inst_set = 'Left'
            AC = Memory[data_address]

        elif(ir == 'load -m(x)'):  # load -m(x)
            inst_set = 'Left'
            if(Memory[data_address][0] == '1'):
                AC = '0' + Memory[data_address][1:40]
            else:
                AC = '1' + Memory[data_address][1:40]

        elif(ir == 'load |m(x)|'):  # load |m(x)|
            inst_set = 'Left'
            AC = '0' + Memory[data_address][1:40]

        elif(ir == 'stor m(x)'):  # stor m(x)
            inst_set = 'Left'
            Memory.insert(data_address, AC)
            print('Memory [' + str(data_address) + '] = ' +
                  Memory[data_address])

        elif(ir == 'jump m(x,0:19)'):  # jump m(x,0:19)
            PC = MAR
            inst_set = 'Left'
            print('Jump encountered')

        elif(ir == 'jump m(x,20:39)'):  # jump m(x,20:39)
            PC = MAR
            inst_set = 'Left'
            to_Be_Processed = False
            print('Jump encountered')

        elif(ir == 'jump + m(x,0:19)'):  # jump+m(x,0:19)
            if(AC[0] == '0'):  # value in accumulator is non-negative
                PC = MAR
                inst_set = 'Left'
                print('Jump encountered')
            else:
                inst_set = 'Left'

        elif(ir == 'jump + m(x,20:39)'):  # jump+m(x,20:39)
            if(AC[0] == '0'):  # value in accumulator is non-negative
                PC = MAR
                inst_set = 'Left'  # after the execution of the right instruction to which the PC jumps, the next left instruction would be executed
                to_Be_Processed = False
                print('Jump encountered')
            else:
                inst_set = 'Left'

        elif(ir == 'add m(x)'):  # add m(x)
            inst_set = 'Left'
            signAC = 1
            signMX = 1
            if(AC[0] == '1'):
                signAC = -1
            if(Memory[data_address][0] == '1'):
                signMX = -1
            ac = BtoD(AC[1:40])
            mx = BtoD(Memory[data_address][1:40])
            ac = signAC*ac + signMX*mx
            if(ac < 0):
                AC = '1' + '0'*(39 - len(DtoB(ac))) + DtoB(-1*ac)
            else:
                AC = '0' + '0'*(39 - len(DtoB(ac))) + DtoB(ac)

        elif(ir == 'add |m(x)|'):  # add |m(x)|
            inst_set = 'Left'
            signAC = 1
            if(AC[0] == '1'):
                signAC = -1
            ac = BtoD(AC[1:40])
            mx = BtoD(Memory[data_address][1:40])
            ac = signAC*ac + mx
            if(ac < 0):
                AC = '1' + '0'*(39 - len(DtoB(-1*ac))) + DtoB(-1*ac)
            else:
                AC = '0' + '0'*(39 - len(DtoB(ac))) + DtoB(ac)

        elif(ir == 'sub m(x)'):  # sub m(x)
            inst_set = 'Left'
            signAC = 1
            signMX = 1
            if(AC[0] == '1'):
                signAC = -1
            if(Memory[data_address][0] == '1'):
                signMX = -1
            ac = BtoD(AC[1:40])
            mx = BtoD(Memory[data_address][1:40])
            ac = signAC*ac - (signMX*mx)
            if(ac < 0):
                AC = '1' + '0'*(39 - len(DtoB(-1*ac))) + DtoB(-1*ac)
            else:
                AC = '0' + '0'*(39 - len(DtoB(ac))) + DtoB(ac)

        elif(ir == 'sub |m(x)|'):  # sub |m(x)|
            inst_set = 'Left'
            signAC = 1
            if(AC[0] == '1'):
                signAC = -1
            if(Memory[data_address][0] == '1'):
                signMX = -1
            ac = BtoD(AC[1:40])
            mx = BtoD(Memory[data_address][1:40])
            ac = signAC*ac - mx
            if(ac < 0):
                AC = '1' + '0'*(39 - len(DtoB(-1*ac))) + DtoB(-1*ac)
            else:
                AC = '0' + '0'*(39 - len(DtoB(ac))) + DtoB(ac)

        elif(ir == 'lsh'):  # lsh
            inst_set = 'Left'
            signAC = 1
            if(AC[0] == '1'):
                signAC = -1
            ac = BtoD(AC[1:40])
            ac = 2*signAC*ac
            if(ac < 0):
                AC = '1' + '0'*(39 - len(DtoB(-1*ac))) + DtoB(-1*ac)
            else:
                AC = '0' + '0'*(39 - len(DtoB(ac))) + DtoB(ac)

        elif(ir == 'rsh'):  # rsh
            inst_set = 'Left'
            signAC = 1
            if(AC[0] == '1'):
                signAC = -1
            ac = BtoD(AC[1:40])
            ac = signAC*int(ac/2)
            if(ac < 0):
                AC = '1' + '0'*(39 - len(DtoB(-1*ac))) + DtoB(-1*ac)
            else:
                AC = '0' + '0'*(39 - len(DtoB(ac))) + DtoB(ac)

        elif(ir == 'hlt'):  # halt
            print('Inside HALT condition')
            IR = '00000000'
            flag = False
            print('Program halted as per instruction!')
            break
    x = input('We have reviewed the parameters. Now press any key to continue...')


# take care of IR, MAR, MBR, IBR, PC

# instruction-> MBR-> right half in IBR and left half[0:8] in IR and [8:20] in MAR
# then convert MAR-> binary to decimal and pass the IR, MAR(address) to the function decode
