import string, sys, contextlib

class PyFuckInterpreter:
    def __init__(self):
        self.vyber = 0
        self.chars = list(string.printable)
        self._debug = False
        
    def debug(self, text:str):
        if self._debug == True:
            print("\nDebug.msg: ",text)
        else:
            pass
    def options(self):
        if [x for x in sys.argv[2:None] if x in (("--debug", "-d"))]:
            self._debug = True
        try:
            if len(sys.argv) > 1:
                if sys.argv[1].endswith(".pyf"):
                    self.display_help(sys.argv[2])
                if sys.argv[1] in ("help", "h"):
                    try:self.display_help([x for x in sys.argv[2:None] if not x.startswith(("--", "-"))])
                    except:self.display_help()
                if sys.argv[1] in ("run", "r"):
                    try:self.decode_file(
                        [x for x in sys.argv[2:None] if x.startswith(("--", "-"))],
                        sys.argv[-1]
                    )
                    except Exception as err:print(err)
                if sys.argv[1] in ("compile", "c"):
                    try:self.compile_file(sys.argv[2])
                    except:print("No command option provided. Use command [help] for usage information.")
                if sys.argv[1] in ("version", "v"):
                    self.version()
            else:
                print("No command or file path provided. Use command [help] for usage information.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    def version(self):
        try:
            with open("VERSION", "r") as ver:
                print("Current version: ",ver.read())
        except Exception as ex:
            print(ex + "Program might be demaged.\nPlease reinstall.")
    def display_help(self, commands:list=[]):
        self.debug("dislplay_help commands: "+str(commands))
        if len(commands) > 0:
            for command in commands:
                self.debug("command: "+str(command))
                if command in ("help","h"):
                    print(f"""\nDisplays help for PyFuck interpreter and its commands.
    Usage: \"pyfuck help [command,...]\"
    """)
                if command in ("run", "r"):
                    print(f"""\nExecutes a PyFuck file. 
    Usage: \"pyfuck run --options <path to file>\"
    
    Options:
    
    --debug,  -d     enables debug output
    --silent, -s    disables terminal output
    """)
                if command in ("version", "v"):
                    print(f"""\nDisplays current vesion.
    Usage: \"pyfuck version\"
    """)
        else:
            print(f"""\nHelp for PyFuck interpreter.
    Usage: \"pyfuck [command] --options <path to file>\" or \"pyfuck <path to file>\" (recomended for automatic execution when opening file)

    Use pyfuck help [command] for more specific info.

    Commands:
    
    help, h       display this help message
    run, r        run a .pyf file with the interpreter
    compile, c    compile Python to PyFuck
    """)

    def decode_file(self, options=[], file_path=None):
        exstr = ""
        self.debug("decode_file options:"+str(options))
        if not file_path.endswith(".pyf"):
            print(f"Warning: File type is not .pyf\nattempting to read as plaintext")
        try:
            file = open(file_path, 'r')
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
        if not [x for x in options[0:None] if x in (("--silent", "-s"))]:
            exec(exstr)
            
        if [x for x in options[0:None] if x in (("--silent", "-s"))]:
            with contextlib.redirect_stdout(None):
                exec(exstr)
            self.debug("silent")
            
    def compile_file(self, file_path):
        print("This command currently doesn't work.")
        pass

if __name__ == "__main__":
    PyFuckInterpreter().options()
