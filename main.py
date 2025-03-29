import string
import sys
import requests
import os
import logging
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class PyFuckInterpreter:
    """
    Interpreter for the PyFuck programming language.
    """
    def __init__(self):
        self.pointer = 0
        self.chars = list(string.printable)
    
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
        if not silent:
            exec(output)

    def run_file(self, file_path: str, silent: bool = False):
        """
        Reads and executes a .pyf file.

        :param file_path: Path to the file.
        :param silent: If True, suppresses output.
        """
        if not file_path.endswith(".pyf"):
            logging.warning("File type is not .pyf. Attempting to read as plaintext.")
        
        try:
            with open(file_path, "r") as file:
                self.execute(file.read(), silent)
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
        except KeyboardInterrupt:
            logging.info("Execution interrupted by user.")

class Updater:
    """
    Handles checking for updates and downloading new versions.
    """
    def __init__(self, repo="Trenclik/PyFuck"):
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
            return None

    def is_update_available(self) -> tuple[dict, bool]:
        """
        Checks the latest version on GitHub and returns the asset dictionary if an update is needed.
        """
        try:
            response = requests.get(self.api_url, headers=self.headers)
            response.raise_for_status()

            release_data = response.json()
            remote_version = release_data.get("tag_name")
            assets = release_data.get("assets", [{}])[0]
            
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

    def download_package(self, assets: dict):
        """
        Downloads the latest release package if an update is needed.
        """
        try:
            download_url = assets.get("browser_download_url")
            filename = assets.get("name")

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

        except requests.RequestException as e:
            logging.error(f"Download failed: {e}")


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

    args = parser.parse_args()

    interpreter = PyFuckInterpreter()
    updater = Updater()

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
        logging.info("This feature is not implemented yet.")

if __name__ == "__main__":
    main()
