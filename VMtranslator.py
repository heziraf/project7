# written by elitali94 and yechezker
# this program gets vm files (files that written in vm language),
# and translate them to asm (hack language).
#  for every input file_name.vm, the program output file_name.asm .
############################################################
# Imports
############################################################
import sys
import os
############################################################
# Constants
############################################################
START_BRACKET = '('
END_BRACKET = ')'
A_INSTRUCTION = "@"
COMMENT = "//"
ENTER = "\n"
SPACE= " "
FIRST_PLACE = 0
SEC_PLACE = 1
VM_SUFFIX = ".vm"
HACK_SUFFIX = ".hack"
PUSH = "push"
POP = "pop"
ADD="add"
SUB= "sub"
NEG = "neg"
EQ="eq"
GT="gt"
LT="lt"
AND="and"
OR="or"
NOT="not"
LOCAL = "loacl"
ARGUMENT ="argument"
THIS= "this"
THAT= "that"
CONSTANT ="constant"
STATIC ="static"
POINTER ="pointer"
TEMP= "temp"
COUNTER = 0


############################################################
# Global variables
############################################################
list_of_vm_lines = []
list_of_asm_lines = []
list_of_memory_segments=[LOCAL,ARGUMENT,THAT,THIS]



############################################################
# Functions
############################################################


def list_without_comments():
    '''
    The function runs on the array list_of_asm_lines and deletes all comments
    That appear after a standard A INSTRUCTION/ C INSTRUCTION
    '''
    for i in range(0, len(list_of_vm_lines)):
        if len( list_of_vm_lines[i])>3:
            list_of_vm_lines[i]=list_of_vm_lines[i][:3]




def writing_to_a_file(input_file):
    '''
    The function runs on the array list_of_asm_lines and write to file all
    the values in array
    :param input_file: the given path with the ending .hack
    '''
    with open(input_file, "w") as file_lines:
        for i in range(0, len(list_of_asm_lines)):
            end = ENTER
            if i == len(list_of_asm_lines) - 1:
                end = ""
            file_lines.write(list_of_asm_lines[i] + end)
    if len(list_of_asm_lines) != 0:
        del list_of_asm_lines[:]


def from_asm_to_list(input_file):
    '''
    The function runs on the lines of the input file, and add to
    dictionary_new_symbol_label ant @(label). also save all valuable lines to
     list_of_asm_lines
    :param input_file: the given path
    '''
    with open(input_file, "r") as file_lines:
        for line in file_lines:
            if line.startswith(COMMENT):
                continue
            elif not line or line == ENTER or line == SPACE or line=="\r":
                continue
            else:
                line_with_no_enter = line.replace(ENTER,"")
                split_line = line_with_no_enter.replace("\r","")
                if not (split_line == ""):
                    turn_to_lise= split_line.split(SPACE)
                    list_of_vm_lines.append(turn_to_lise)
def line_without_aritmetic(line):
    if line == ADD:
        list_of_asm_lines.extend(["//"+line,"@SP","A = M - 1","D = M",
                                  "A = A - 1","D = D + M","M = D","@SP","M=M-1"])
    elif line == SUB:
        list_of_asm_lines.extend(
            ["//" + line, "@SP", "A = M - 1", "D = M", "A = A - 1",
             "D=M-D", "M = D","@SP","M=M-1"])
    elif line ==NEG:
        list_of_asm_lines.extend(
            ["//" + line, "@SP", "A = M - 1", "M = -M"])
    elif line ==EQ:
        list_of_asm_lines.extend(["//" + line, "@SP", "A=M-1", "D=M", "A=A-1",
                                  "D=M-D","@13","M=D","@sp","M=M-1","A=M","A=A-1",
            "M=0","D=A","@14","M=D","@13","D=M","@CONTINU","D;JNE","@14",
                                  "A=M","M=1","(CONTINU)"])
    elif line ==GT:
        list_of_asm_lines.extend(["//" + line, "@SP", "A=M-1", "D=M", "A=A-1",
                            "D=M-D","@13","M=D","@sp","M=M-1","A=M","A=A-1",
                                  "M=0", "D=A", "@14", "M=D", "@13", "D=M",
                                  "@CONTINU", "D;JLE", "@14",
                                  "A=M", "M=1", "(CONTINU)"])
    elif line ==LT:
        list_of_asm_lines.extend(["//" + line, "@SP", "A=M-1", "D=M", "A=A-1",
                                "D=M-D","@13","M=D","@sp","M=M-1","A=M","A=A-1",
                                  "M=0", "D=A", "@14", "M=D", "@13", "D=M",
                                  "@CONTINU", "D;JGE", "@14",
                                  "A=M", "M=1", "(CONTINU)"])
    elif line ==AND:
        list_of_asm_lines.extend(["//" + line, "@SP", "A=M-1", "D=M", "A=A-1",
                    "D=M+D","D=D-1","@13","M=D","@sp","M=M-1","A=M","A=A-1",
                                  "M=0", "D=A", "@14", "M=D", "@13", "D=M",
                                  "@CONTINU", "D;JLE", "@14",
                                  "A=M", "M=1", "(CONTINU)"])
    elif line ==OR:
        list_of_asm_lines.extend(["//" + line, "@SP", "A=M-1", "D=M", "A=A-1",
                    "D=M+D","@13","M=D","@sp","M=M-1","A=M","A=A-1",
                                  "M=0", "D=A", "@14", "M=D", "@13", "D=M",
                                  "@CONTINU", "D;JLE", "@14",
                                  "A=M", "M=1", "(CONTINU)"])
    elif line ==NOT:
        list_of_asm_lines.extend(["//" + line, "@SP", "A=M-1", "D=M",
           "@13", "M=D", "@SP", "A=M", "A=A-1",
          "M=0", "D=A", "@14", "M=D", "@13", "D=M",
          "@CONTINU", "D;JGT", "@14",
          "A=M", "M=1", "(CONTINU)"])


def line_without_push(line):
    segment = line[1]
    i = line[2]
    if segment in list_of_memory_segments:
        push_for_memory_segments(PUSH,segment,i)
    if segment == POINTER:
        push_for_pointer(PUSH, segment, i)
    if segment == CONSTANT:
        list_of_asm_lines.extend(["//" + PUSH + str(segment) + str(i),
                                  "@" + str(i), "D=A", "@SP", "A=M", "M=D",
                                  "@SP", "M=M+1"])

def push_for_pointer(PUSH, segment, i):
    address = ""
    if i == 0:
        address = "THIS"
    else:
        address = "THAT"

def pop_for_pointer(pop, segment, i):
    address = ""
    if i == 0:
        address = "THIS"
    else:
        address = "THAT"

def push_for_memory_segments(push, segment,i):
    address = ""
    if segment == LOCAL:
        address ="LCL"
    elif segment == ARGUMENT:
        address= "ARG"
    elif segment == THIS:
        address= "THIS"
    else:
        address ="THAT"
    list_of_asm_lines.extend(["//"+str(push)+str(segment)+str(i),
                              "@"+str(i),"D=A","@"+str(address),"D=D+M","A=D",
                              "D=M","@SP","A=M","M=D","@SP","M=M+1"])

def line_without_pop(line):
    pop = line[0]
    segment = line[1]
    i = line[2]
    if segment in list_of_memory_segments:
        pop_for_memory_segments(pop,segment, i)
    if segment == POINTER:
        pop_for_pointer(POP, segment, i)

def pop_for_memory_segments(pop,segment,i):
    address = ""
    if segment == LOCAL:
        address ="LCL"
    elif segment == ARGUMENT:
        address= "ARG"
    elif segment == THIS:
        address= "THIS"
    else:
        address ="THAT"
    list_of_asm_lines.extend(["//"+str(pop)+str(segment)+str(i),"@SP", "A=M-1",
                              "D=M","@13","M=D","@"+str(i),"D=A",
                              "@"+str(address),"D=D+M","A=D","@14","M=D","@13",
                             "D=M","@14","A=M","M=D","@SP","M=M-1"])


def vm_to_asm():
    for line in list_of_vm_lines:
        if list_of_vm_lines[0]== PUSH:
            line_without_push(line)
        elif  list_of_vm_lines[0]== POP:
            line_without_pop(line)
        else:
            line_without_aritmetic(line)




def from_vm_to_asm(input_file):
    '''
    The function runs on the functions that transfer the file from vm to asm
    if file end with .asm
    :param input_file: the given path
    '''
    if input_file.endswith(VM_SUFFIX):
        from_asm_to_list(input_file)
        list_without_comments()
        print(list_of_vm_lines)
        vm_to_asm()
      #  writing_to_a_file(os.path.splitext(input_file)[FIRST_PLACE] + HACK_SUFFIX)


def __main__():


    input_file = sys.argv[SEC_PLACE]
    if os.path.isfile(input_file):
        from_vm_to_asm(input_file)
    elif os.path.isdir(input_file):
        list_of_files = os.listdir(input_file)
        for file in list_of_files:
            from_vm_to_asm(input_file+file)
    else:
        return


if __name__ == "__main__":
    __main__()