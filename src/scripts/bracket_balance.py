def bracket_balance(bracket_string):
    running_list = []
    opposite_char = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    for char in bracket_string:
        if char in opposite_char:
            if len(running_list) > 0 and running_list[-1] == opposite_char[char]:
                del running_list[-1]
            else:
                return False
        else:
            running_list.append(char)
    if len(running_list) != 0:
        return False
    return True