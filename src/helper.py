def validate_input_string(input, max_len):
    if len(input) > max_len:
        return False, "length of input cannot exceed {}".format(max_len)
    if len(input.strip()) == 0:
        return False, "input cannot be blank"
    return True, "OK"


def validate_authen_string(input, max_len):
    status, message = validate_authen_string(input, max_len)
    if not status:
        return status, message
    if input.count(' '):
        return False, "input cannot contain spaces"
    return True, "OK"
