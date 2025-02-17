import requests
import os
import sys
import logging

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
                logging.warning(f"Skipping download: Missing URL or filename in assets dictionary.")
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
