#!/bin/bash
for inf in *.fchk
do
echo Running ${inf}
time ./Multiwfn $inf < $(basename $inf .fchk) > $(basename $inf .fchk).output 
echo ${inf} is finished
echo
done 
