def reduce(code):
    code += "E"
    ptr = 0
    val = 0
    previous = code[0]
    temp = []
    result = []
    for i in code:
        temp.append(i)
        if i == "+":
            val += 1
        elif i == "-":
            val -= 1
        elif i == ">":
            ptr += 1
        elif i == "<":
            ptr -= 1
        if i!=previous and previous in {"+","-"} and i in {">", "<","[","]",".",",","E"}:
            if val > 0:
                result.append((val,"+"))
            elif val < 0:
                result.append((-val,"-"))
            temp = []
            val = 0
            if i == ">":
                ptr = 1
            elif i == "<":
                ptr = -1
        if i!=previous and previous in {">", "<"} and i in {"+", "-","[","]",".",",", "E"}:
            if ptr > 0:
                result.append((ptr,">"))
            if ptr < 0:
                result.append(((-ptr),"<"))
            temp = []
            ptr = 0
            if i == "+":
                val = 1
            elif i == "-":
                val = -1
        if i in {"[","]",".",","}:
            result.append(i)
        previous = i
    return result

def tag(code):
    result = []
    nmax = 0
    for i in code:
        if i == "[":
            nmax += 1
    left = nmax-1
    right = 0
    for i in code:
        if i in {".",","} or i not in {"[","]"}:
            result.append(i)
        else:
            if i == "[":
                result.append((left, i))
                left -= 1
            elif i == "]":
                result.append((right, i))
                right += 1
    return result

def compile(code, stacksize):
    asm = ".intel_syntax noprefix\n.globl _start\n.section .text\n\n"
    asm += "_start:\n\n"
    asm += "mov rbp, rsp\nsub rsp, "+str(stacksize)+"\n"
    asm += "mov rax, rsp\nsub rax, "+str(stacksize//2)+"\n"
    for i in code:
        if i not in {",","."}:
            match i[1]:
                case "+":
                    asm += "add byte ptr [rax], "+str(i[0])+"\n"
                case "-":
                    asm += "sub byte ptr [rax], "+str(i[0])+"\n"
                case ">":
                    asm += "add rax, "+str(i[0])+"\n"
                case "<":
                    asm += "sub rax, "+str(i[0])+"\n"
                case "[":
                    asm += "cmp byte ptr [rax], 0\nje tag"+str(i[0])+"b\ntag"+str(i[0])+"a:\n"
                case "]":
                    asm += "cmp byte ptr [rax], 0\njne tag"+str(i[0])+"a\ntag"+str(i[0])+"b:\n"
        else:
            if i == ".":
                    asm += "mov rbx, rax\nmov rax, 1\nmov rdi, 1\n"
                    asm += "mov rsi, rbx\nmov rdx, 1\nsyscall\n"
                    asm += "mov rax, rbx\n"
            else:
                    asm += "mov rbx, rax\nxor rax, rax\nxor rdi, rdi\n"
                    asm += "mov rsi, rbx\nmov rdx, 1\nsyscall\n"
                    asm += "mov rax, rbx\n"
    asm += "mov rax, 60\nsyscall"
    return asm

all = lambda a,b: compile(tag(reduce(a)),b) 

bf = input()
print(all(bf,0x10000))
