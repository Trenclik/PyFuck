import string
import sys
from colorama import init, Fore, Back, Style

class PyFuckInterpreter:
    def __init__(self):
        self.vyber = 0
        self.chars = list(string.printable)
    
    def run(self):
        try:
            if len(sys.argv) > 1:
                if sys.argv[1] in ("--help", "-h"):
                    self.display_help()
                if sys.argv[1] in ("--run", "-r"):
                    exec(self.execute_file(sys.argv[2]))
            else:
                print("Error: No file path provided. Use --help for usage information.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            

    def display_help(self):
        print(f"""Help for PyFuck interpreter.
Usage: pyfuck [command] --options <path to file>
Commands:
  --help, -h    Display this help message
  --run, -r     Run the interpreter
  --compile, -c Compile python to PyFuck
""")

    def execute_file(self, file_path):
        try:
            exstr = ""
            for char in open(file_path, 'r').read():
                if char == '>':
                    self.vyber += 1
                elif char == '<':
                    self.vyber -= 1
                elif char == '!':
                    exstr += self.chars[self.vyber]

            self.vyber = 0
            return exstr

        except FileNotFoundError as fnfe:
            print(f"Error: {fnfe}")
            return ""
        except KeyboardInterrupt:
            print("Execution interrupted by user.")
            return ""
    def compile_file(self, file_path):
        pass

if __name__ == "__main__":
    init(autoreset=True)
    PyFuckInterpreter().run()
