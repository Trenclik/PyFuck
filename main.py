import string
import sys
import contextlib
import requests
import os
import logging

class PyFuckInterpreter:
    def __init__(self):
        self.vyber = 0
        self.chars = list(string.printable)
        self._debug = False
        
    def debug(self, text:str):
        if self._debug:
            print("\nDebug.msg: ",text)
        else:
            pass
    def options(self):
        if [x for x in sys.argv[2:None] if x in (("--debug", "-d"))]:
            self._debug = True
        try:
            if len(sys.argv) > 1:
                if sys.argv[1].endswith(".pyf"):
                    self.decode_file("",sys.argv[1])
                if sys.argv[1] in ("help", "h"):
                    try:
                        self.display_help([x for x in sys.argv[2:None] if not x.startswith(("--", "-"))])
                    except Exception:
                        self.display_help()
                if sys.argv[1] in ("run", "r"):
                    try:
                        self.decode_file(
                            [x for x in sys.argv[2:None] if x.startswith(("--", "-"))],
                            sys.argv[-1]
                        )
                    except Exception as err:
                        print(err)
                if sys.argv[1] in ("compile", "c"):
                    try:
                        self.compile_file(sys.argv[2])
                    except Exception:
                        print("No command option provided. Use command [help] for usage information.")
                if sys.argv[1] in ("version", "v"):
                    self.version()
                if sys.argv[1] in ("update", "u"):
                    try:
                        self.check_for_updates(sys.argv[2])
                    except IndexError:
                        self.check_for_updates()
            else:
                print("No command or file path provided. Use command [help] for usage information.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    def version(self):
        try:
            with open(Updater().version_path, "r") as ver:
                print("Current version: ",ver.read())
        except Exception as ex:
            print(ex + "Program might be demaged.\nPlease reinstall.")
    def display_help(self, commands:list=[]):
        self.debug("dislplay_help commands: "+str(commands))
        if len(commands) > 0:
            for command in commands:
                self.debug("command: "+str(command))
                if command in ("help", "h"):
                    print("""\nDisplays help for PyFuck interpreter and its commands.
    Usage: \"pyfuck help [command,...]\"
    """)
                if command in ("update", "u"):
                    print("""\nChecks for updates.
    Usage: \"pyfuck update --options
    
    Oprions:
    
    --noconfirm, -nc automaticly confirms update download
    --silent, -s     disables terminal output
    """)
                if command in ("run", "r"):
                    print("""\nExecutes a PyFuck file. 
    Usage: \"pyfuck run --options <path to file>\"
    
    Options:
    
    --silent, -s    disables terminal output
    """)
                if command in ("version", "v"):
                    print("""\nDisplays current vesion.
    Usage: \"pyfuck version\"
    """)
        else:
            print("""\nHelp for PyFuck interpreter.
    Usage: \"pyfuck [command] --options <path to file>\" or \"pyfuck <path to file>\" (recomended for automatic execution when opening file)

    Use pyfuck help [command] for more specific info.

    Commands:
    
    help, h       display this help message
    run, r        run a .pyf file with the interpreter
    compile, c    compile Python to PyFuck
    update, u     check for updates
    version, v    display installed version
    """)
    def check_for_updates(self, options=[]):
        updater = Updater()
        assets, is_latest_version = updater.check_remote_version()
        if len(options) == 0 and not is_latest_version:
            confirmation = input("Do you want to download the newest version? [Y/n]: ")
            if confirmation.lower() == "y" or confirmation == "":
                if [x for x in options[0:None] if x in (("--silent", "-s"))]:
                    with contextlib.redirect_stdout(None):
                        updater.download_package(assets)
                        return
                else:
                    updater.download_package(assets)
                    return
            if confirmation.lower() == "n":
                    logging.info("Skipping download: User aborted the operation.")
                    return
            else:
                logging.warning("Skipping download: Invalid option")
        if [x for x in options[0:None] if x in (("--noconfirm", "-nc"))]:
            updater.download_package(assets)
            return
            
    def decode_file(self, options=[], file_path=None):
        exstr = ""
        self.debug("decode_file options:"+str(options))
        if not file_path.endswith(".pyf"):
            print("Warning: File type is not .pyf\nattempting to read as plaintext")
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


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Updater:
    def __init__(self, repo="Trenclik/PyFuck"):
        self.api_url = f"https://api.github.com/repos/{repo}/releases/latest"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        self.local_version = self.load_local_version()

    def get_path(self, filename):
        """Gets the absolute path of a file, handling PyInstaller bundles."""
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        return os.path.join(base_path, filename)

    def load_local_version(self):
        """Loads the local version from the VERSION file."""
        self.version_path = self.get_path("VERSION")
        try:
            with open(self.version_path, "r") as ver_file:
                return ver_file.read().strip()
        except FileNotFoundError:
            logging.error("VERSION file not found!")
            return None

    def check_remote_version(self):
        """Checks the latest version on GitHub and returns the asset dictionary if an update is needed."""
        try:
            response = requests.get(self.api_url, headers=self.headers) # prvotní check remote serveru
            if response.status_code == 403:
                logging.error("GitHub API rate limit exceeded. Consider setting an API key.")
                return None, False
            response.raise_for_status()

            release_data = response.json()
            remote_version = release_data.get("tag_name") # tag jako na githubu verze v tagu jako vole tag na GH jako verze
            assets = release_data.get("assets", {})[0]
            if not assets:
                logging.warning("No assets found in the latest release.")
                return None, False

            if remote_version == self.local_version:
                logging.info("Already up-to-date.")
                return assets, True

            logging.info(f"New version available: {remote_version}")
            return assets, False

        except requests.RequestException as e:
            logging.error(f"Failed to check remote version: {e}")
            return None, False

    def download_package(self, assets):
        """Downloads the latest release package if an update is needed."""
        try:
            download_url = assets.get("browser_download_url")
            filename = assets.get("name")

            if not download_url or not filename:
                logging.warning("Skipping download: Missing URL or filename in assets dictionary.")
                return

            logging.info(f"Downloading {filename}...")

            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                logging.info(f"Downloaded {filename} successfully.")

        except requests.RequestException as e:
            logging.error(f"Download failed: {e}")

if __name__ == "__main__":
    PyFuckInterpreter().options()
