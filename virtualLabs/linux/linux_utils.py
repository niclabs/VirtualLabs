""""Creates an empty file that can be written"""
def touch(file_name):
    return open(file_name, 'w')