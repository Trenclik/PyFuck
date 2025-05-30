import sys
import requests
import os
import logging
import argparse
import re
import importlib

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class PyFuckInterpreter:
    """
    Interpreter for the PyFuck programming language
    """
    def __init__(self):
        self.pointer = 0
        self.chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ' ', '\t', '\n', '\r', '\x0b', '\x0c']
    
    def execute(self, code: str, silent: bool = False):
        """
        Executes PyFuck code.

        :param code: The code to execute.
        :param silent: If True, suppresses output.
        """
        output = ""
        for char in code:
            if char == '>':
                self.pointer += 1
            elif char == '<':
                self.pointer -= 1
            elif char == '!':
                output += self.chars[self.pointer]
        
        self.pointer = 0
        import_pattern = re.compile(r'^\s*import\s+(\w+)|^\s*from\s+(\w+)\s+import', re.MULTILINE)
        found_imports = import_pattern.findall(output)
        exec_env = { # type: ignore
            '__builtins__': __builtins__,
            '__name__':'__main__'
        }
        for imp in found_imports:
            module_name = imp[0] or imp[1]
            try:
                exec_env[module_name] = importlib.import_module(module_name)
            except ImportError:
                print(f"Warning: Could not import module '{module_name}'")
        try:
            exec(output, exec_env) # type: ignore
        except Exception as e:
            print(f"Error during execution: {e}")

    def run_file(self, file_path: str, silent: bool = False) -> None:
        """
        Reads and executes a .pyf file.

        :param file_path: Path to the file.
        :param silent: If True, suppresses output.
        """
        if not file_path.endswith(".pyf"):
            logging.error("File is not a valid PyFuck script!")
            return
        
        try:
            with open(file_path, "r") as file:
                self.execute(file.read(), silent)
                return
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            return
        except KeyboardInterrupt:
            logging.info("Execution interrupted by user.")
            return

class Updater:
    """
    Handles checking for updates and downloading new versions.
    """
    def __init__(self, repo:str ="Trenclik/PyFuck"):
        self.api_url = f"https://api.github.com/repos/{repo}/releases/latest"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        self.version_path = self.get_path("VERSION")
        self.local_version = self.load_local_version()

    def get_path(self, filename: str) -> str:
        """
        Gets the absolute path of a file, handling PyInstaller bundles.
        """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        return os.path.join(base_path, filename)

    def load_local_version(self) -> str:
        """
        Loads the local version from the VERSION file.
        """
        try:
            with open(self.version_path, "r") as ver_file:
                return ver_file.read().strip()
        except FileNotFoundError:
            logging.error("VERSION file not found!")
            return ""

    def is_update_available(self) -> tuple[dict[str,str], bool]:
        """
        Checks the latest version on GitHub and returns the asset dictionary if an update is needed.
        """
        try:
            response = requests.get(self.api_url, headers=self.headers)
            response.raise_for_status()

            release_data = response.json()
            remote_version = release_data.get("tag_name")
            assets = release_data.get("assets", [{}])[0]
            filtered_assets = {"Download":"","Filename":""}
            if assets:
                filtered_assets["Download"] = assets.get("browser_download_url")
                filtered_assets["Filename"] = assets.get("name")
            if not assets:
                logging.warning("No assets found in the latest release.")
                return (filtered_assets, False)

            if remote_version == self.local_version:
                logging.info("Already up-to-date.")
                return filtered_assets, True

            logging.info(f"New version available: {remote_version}")
            return filtered_assets, False

        except requests.RequestException as e:
            logging.error(f"Failed to check remote version: {e}")
            filtered_assets = {"Download":"","Filename":""}
            return filtered_assets, False

    def download_package(self, assets: dict[str,str]) -> None:
        """
        Downloads the latest release package if an update is needed.
        """
        try:
            download_url = assets.get("Download")
            filename = assets.get("filename")

            if not download_url or not filename:
                logging.warning("Skipping download: Missing URL or filename in assets.")
                return

            logging.info(f"Downloading {filename}...")

            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                logging.info(f"Downloaded {filename} successfully.")
                return

        except requests.RequestException as e:
            logging.error(f"Download failed: {e}")
            return
class Compiler:
    """
    Compiler for the PyFuck language
    """
    def __init__(self) -> None:
        self.chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ' ', '\t', '\n', '\r', '\x0b', '\x0c']
        self.is_verbose = False
        self.is_silent = False
        pass

    def main(self, filename: str) -> None:
        with open(filename,"r") as source_file:
            object_list: list[list[int]] = self.disassemble(source_file.read())
            instruction_list: list[tuple[int,int]] = self.link(object_list)
            code = self.assemble(instruction_list)
            self.write(code,filename)
    def disassemble(self, code: str) -> list[list[int]]:
        """
        Splits code and translates it into objects (lists with index integers)
        Preserves indentation by converting leading whitespace characters.
        """
        if not self.is_silent: 
            logging.info("Code disassembly started")
        lines: list[list[int]] = []
        
        try:
            for idx, line in enumerate(code.splitlines()):
                if self.is_verbose:logging.info(f"Started disassembly of line {idx}")
                
                line_indexes: list[int] = []
                
                if self.is_verbose:logging.info(f"Started whitespace processing for line {idx}")
                leading_ws:list[str] = []
                for symbol in line:
                    if symbol in (' ', '\t'):
                        leading_ws.append(symbol)
                    else:
                        break
                for ws_char in leading_ws:
                    try:
                        line_indexes.append(self.chars.index(ws_char))
                        if self.is_verbose:logging.info(f"Translated indentation {ws_char} -> {self.chars.index(ws_char)}")
                    except ValueError as ex:
                        logging.error(f"Whitespace character not in charset: {ws_char} - {ex}")
                if self.is_verbose: logging.info("Finished whitespace processing")
                if line.strip():
                    try:
                        for word in line[len(leading_ws):].split():
                            if self.is_verbose: 
                                logging.info(f"Started disassembly of word {word}")
                            try:
                                for symbol in word:
                                    line_indexes.append(self.chars.index(symbol))
                                    if self.is_verbose: 
                                        logging.info(f"Translated {symbol} -> {self.chars.index(symbol)}")
                            except ValueError as ex:
                                logging.error(ex)
                            
                            # Add space between words (but not after last word)
                            if word != line[len(leading_ws):].split()[-1]:
                                if self.is_verbose: 
                                    logging.info("Added space character")
                                line_indexes.append(self.chars.index(" "))
                            
                            if self.is_verbose:logging.info(f"Finished disassembly of word {word}")
                    except Exception as ex:
                        logging.error(ex)
                
                lines.append(line_indexes)
                if self.is_verbose:logging.info(f"Finished disassembly of line: {line}")
                    
        except Exception as ex:
            logging.error(ex)
        
        if not self.is_silent: 
            logging.info("Code disassembled successfully!")
        return lines

    def link(self, line_object: list[list[int]]) -> list[tuple[int,int]]:
        """
        Translates object lists into 1 instruction list
        """
        instructions: list[tuple[int,int]] = []
        previous_idx: int = 0
        if self.is_verbose: logging.info(f"Object linking started")
        for idx, line in enumerate(line_object):
            if self.is_verbose: logging.info(f"Opening new line")
            result:tuple[int,int]
            for sym_idx in line:
                if self.is_verbose: logging.info(f"Linking instruction {sym_idx} of line {idx}")
                opt:int = 0
                mult:int = 0
                if sym_idx > previous_idx:
                    opt = 2
                    mult = sym_idx - previous_idx
                elif sym_idx < previous_idx:  
                    opt = 1
                    mult = previous_idx - sym_idx
                else:
                    opt = 0
                result = (opt,mult)
                if self.is_verbose: logging.info(f"Created instruction No.{sym_idx}: {result}")
                if self.is_verbose: logging.info(f"Assigning previous_idx {previous_idx} -> {sym_idx}")
                previous_idx = sym_idx
                instructions.append(result)
            if self.is_verbose: logging.info(f"Previous instruction index: {previous_idx}")
            if 96 > previous_idx:
                opt:int = 2
                mult:int = 96 - previous_idx
            elif 96 < previous_idx:  
                opt:int = 1
                mult:int = previous_idx - 96
            else:
                opt:int = 0
                mult:int = 0
            if self.is_verbose: logging.info(f"Assigning previous_idx {previous_idx} -> 96")
            previous_idx = 96
            if self.is_verbose: logging.info(f"Adding newline symbol")
            instructions.append((opt,mult))
        if self.is_verbose: logging.info(f"Object linking finished")
        return instructions

    def assemble(self, instructions: list[tuple[int,int]]) -> str:
        """
        Assembles code from instructions
        """
        code = ""
        previous_inst = ()
        for idx, instruction in enumerate(instructions):
            if self.is_verbose: logging.info(f"Decoding instruction {str(instruction)} No.{idx} of {str(len(instructions) - 1)}")
            if instruction[0] == 0:
                code += "!"
            if instruction[0] == 1:
                for mult in range(instruction[1]):
                    code += "<"
                code += "!"
            if instruction[0] == 2:
                for mult in range(instruction[1]):
                    code += ">"
                code += "!"
            if self.is_verbose: logging.info(f"Assigning previous_inst {previous_inst} -> {instruction}")
            previous_inst = instruction
            if self.is_verbose: logging.info(f"Decoding complete!")
        return code

    def write(self, code: str, filename: str) -> None:
        """
        Writes PyFuck code into file
        """
        with open(filename + "f","+w") as pyf:
            pyf.write(code)
        return
        
def main():
    parser = argparse.ArgumentParser(description="PyFuck Interpreter CLI")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Run command
    run_parser = subparsers.add_parser("run", aliases=["r"], help="Run a PyFuck script")
    run_parser.add_argument("file", help="File to execute (.pyf script)")
    run_parser.add_argument("--silent", "-s", action="store_true", help="Suppress output")

    # Update command
    update_parser = subparsers.add_parser("update", aliases=["u"], help="Check for updates and download new version")
    update_parser.add_argument("--noconfirm", "-nc", action="store_true", help="Auto-confirm updates")

    # Version command
    subparsers.add_parser("version", aliases=["v"], help="Show the current version")

    # Compile command (not implemented yet)
    compile_parser = subparsers.add_parser("compile", aliases=["c"], help="Compile PyFuck to an executable (Not implemented yet)")
    compile_parser.add_argument("file", help="File to compile (.pyf script)")
    compile_parser.add_argument("--verbose", action="store_true", help="More verbose output")
    compile_parser.add_argument("--silent", action="store_true", help="Suppress output")

    args = parser.parse_args()

    interpreter = PyFuckInterpreter()
    updater = Updater()
    compiler = Compiler()
    if args.command in ("run", "r"):
        if args.file:
            if not args.file.endswith(".pyf"):
                logging.warning("Provided file is not a PyFuck script! Attempting to run in plaintext mode.")
            interpreter.run_file(args.file, args.silent)
        else:
            logging.error("No file specified for execution.")

    elif args.command in ("update", "u"):
        assets, is_latest = updater.is_update_available()
        if not is_latest and assets:
            if args.noconfirm or input("Do you want to download the newest version? [Y/n]: ").lower() in ("y", ""):
                updater.download_package(assets)
            else:
                logging.info("Update canceled by user.")

    elif args.command in ("version", "v"):
        print(f"Current version: {updater.local_version}")

    elif args.command in ("compile", "c"):
        if args.verbose:
            compiler.is_verbose = True
        if args.silent:
            compiler.is_silent = True
        if args.silent and args.verbose:
            logging.error("Compiler can be only verbose or silent. Not both!")
            return
        compiler.main(args.file)
        #logging.info("This feature is not implemented yet.")

if __name__ == "__main__":
    main()
