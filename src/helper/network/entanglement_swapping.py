from netsquid.components import INSTR_X, INSTR_Z


def apply_gates(curr_state: int, position: int, remote_node_memory, debug: bool) -> None:
    """
    Apply the necessary gates to the qubit in the memory position (in the RemoteNode),
    based on the state (in the repeater).
    :param curr_state: The state of the qubit in the Repeater memory position, w M format(0, 1, 2, or 3)
    :param position: The memory position in the RemoteNode (0 or 1)
    :param remote_node_memory: The memory of the RemoteNode
    :param debug: A flag to print the steps of the function
    """
    # dictionary with the instructions to apply based on the state of the qubit
    # (represented w numbers, input of the function curr_state or as bell states in the comments)
    instructions = {
        0: [],  # |00> (no gates to apply)
        1: [INSTR_X],  # |01>
        2: [INSTR_Z, INSTR_X],  # |11>
        3: [INSTR_Z]  # |10>
    }
    # get the instructions based on the state of the qubit in the memory position
    get_instructions = instructions[curr_state]
    # apply the instructions to the qubit in the memory position (in the RemoteNode)
    for instr in get_instructions:
        remote_node_memory.execute_instruction(instr, [position])
        # , output_key="M" , inplace=True, repetitions=1, position=position)  # position=position
        if debug:
            print(f"Applying instruction {instr} to the qubit "
                  f"in memory position {position} in the RemoteNode")
