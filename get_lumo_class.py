#!/usr/bin/env python
# Filename : get_lumo.py
"""
Get the index of the LUMO orbitals for all molecules in the current directory. Calculate the contribution of atoms to the LUMO orbital
"""

import os
import sys
import os.path


def get_lumo(filename):
    myfile = open (filename)
    lines = myfile.readlines()
    flen = len (lines)
    result = os.path.split(filename)[1]
    for i in range (flen):
        if 'Number of alpha electrons' in lines[i]:
            list = lines[i].split()
            lumo = int(list[5])+1
            input_name = result[:-5]
            input = open (input_name,'w')
            input.write ('8\n8\n1\n')
            input.write (str(lumo))
            return input

def get_contribution(filename):
    myfile = open(filename)
    lines = myfile.readlines()
    flen = len (lines) 
    total = ''
    for i in range (flen):
        if 'Contributions after normalization:' in lines[i]:
            while True:
                i += 1
                if 'Now input the orbital index' in lines[i]:
                    break
                total += lines[i]
    return total

def classify_lumo(filename):
    myfile = open(filename)
    lines = myfile.readlines()
    flen = len(lines)
    func = 0
    side = 0
    halogen = 0
    for i in range(flen):
        if 'Atom' in lines[i]:
            list = lines[i].split()
            temp = list[1].replace('(',' ')
            new = temp.replace(')','')
            percentage = list[-1][:-1]
            atom_contribution = new + ' '+ list[-1]
            contribution_list = atom_contribution.split()
            if str(contribution_list[1]) in ['F','Cl','Br']:
                if float (percentage) > 0.1:
                    halogen += 1
            elif float(percentage) > 3:
                if int(contribution_list[0]) < 15:
                    func += 1
                elif int(contribution_list[0]) >= 15:
                    side += 1
    if halogen > 0 :
        type = 'halogen'
    elif func >= 4 and side  >=4:
        type = 'cross'
    elif func >= 4:
        type = 'func'
    else:
        type = 'side'
    return type

def main():
    for dirpath, dirnames, filenames in os.walk('.'):
        for f in filenames:
            if os.path.splitext(f)[1]=='.fchk':
                get_lumo(f)
    os.system("./multiall.sh")

    for dirpath, dirnames, filenames in os.walk('.'):
        for f in filenames:
            if os.path.splitext(f)[1]=='.output':
                output_name = os.path.split(f)[1][:-7]+'.lumo'
                output = open (output_name,'w')
                output.write(get_contribution(f))
                os.remove(f)
    for dirpath, dirnames, filenames in os.walk('.'):
        for f in filenames:
            if os.path.splitext(f)[1]=='.lumo':
                print os.path.splitext(f)[0]+ ' '+ classify_lumo(f)

if  __name__ == '__main__':
    main()
