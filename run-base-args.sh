#!/usr/bin/env bash
log_file="run-base-args-log.txt"
debug="True"
base_cmd=(python3 ./src/main.py)
arg0=(empty entangle_nodes 1,4 $debug 0)
arg1=(empty entangle_nodes 1,4 $debug 1)
arg2=(combined entangle_nodes 1,4 $debug 0)
arg3=(combined entangle_nodes 1,4 $debug 1)
arg4=(empty protocol_a 1,2,4 $debug 0)
arg5=(empty protocol_a 1,2,4 $debug 1)
arg6=(combined protocol_b 1,2,4 $debug 0)
arg7=(combined protocol_b 1,2,4 $debug 1)

# combine all arguments into a single array
args=($arg0 $arg1 $arg2 $arg3 $arg4 $arg5 $arg6 $arg7)
# for loop to run the command for each argument
for arg in args; do
    $base_cmd $arg
done > $log_file
exit 0
