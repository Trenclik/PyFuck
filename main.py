import string
import sys

class PyFuckInterpreter:
    def __init__(self):
        self.vyber = 0
        self.chars = list(string.printable)
    
    def options(self):
        try:
            if len(sys.argv) > 1:
                if sys.argv[1].endswith(".pyf"):
                    self.display_help(sys.argv[2])
                if sys.argv[1] in ("help", "h"):
                    try:self.display_help(sys.argv[2])
                    except:self.display_help()
                if sys.argv[1] in ("run", "r"):
                    try:self.decode_file(sys.argv[2],sys.argv[3:None])
                    except:print("No command option provided. Use command [help] for usage information.")
                if sys.argv[1] in ("compile", "c"):
                    try:self.compile_file(sys.argv[2])
                    except:print("No command option provided. Use command [help] for usage information.")
                
            else:
                print("No command or file path provided. Use command [help] for usage information.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            

    def display_help(self, command=None):
        if command in ("help","h"):
            print(f"""Displays help for PyFuck interpreter and its commands.
    Usage: pyfuck help [command]
    """)
        if command in ("run", "r"):
            print(f"""Executes a PyFuck file. 
    Usage: pyfuck run <path to file>
    
    Options:
    
    --verbose, -v   enables terminal output
    --silent, -s    disables terminal output
    """)
        if command == None:
            print(f"""Help for PyFuck interpreter.
    Usage: pyfuck [command] --options <path to file> or pyfuck <path to file> (recomended for automatic execution when opening file)

    Use pyfuck help [command] for more specific info.

    Commands:
    
    help, h    display this help message
    run, r     run a .pyf file with the interpreter
    compile, c compile Python to PyFuck
    """)

    def decode_file(self, file_path, options=None):
        exstr = ""
        try:file = open(file_path, 'r')
        except FileNotFoundError:
            print(f"Error: No such file or directory: {file_path}")
            return ""
        except KeyboardInterrupt:
            print("Execution interrupted by user.")
            return ""
        for char in file.read():
            if char == '>':
                self.vyber += 1
            elif char == '<':
                self.vyber -= 1
            elif char == '!':
                exstr += self.chars[self.vyber]
        self.vyber = 0
            

    def compile_file(self, file_path):
        print("This command currently doesn't work.")
        pass

if __name__ == "__main__":
    PyFuckInterpreter().options()
