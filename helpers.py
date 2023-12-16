def format_error_msg(msg):
    return "\033[91m" + msg + "\033[0m"

def format_success_msg(msg):
    return "\033[92m" + msg + "\033[0m"

def format_warning_msg(msg):
    return "\033[93m" + msg + "\033[0m"

def format_underline_msg(msg):
    return "\033[4m" + msg + "\033[0m"

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
