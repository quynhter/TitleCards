import sys
import os

def get_executable_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))
    
PROGRAM_DIR  = get_executable_path()