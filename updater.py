import requests
class Updater:
    def __init__(self):
        self.REPO = "Trenclik/PyFuck"
        self.API_URL = f"https://api.github.com/repos/{self.REPO}/releases/latest"
        self.VERSION = ''
        self.HEADERS = {
            "Accept":"application/vnd.github.v3+json",
            #"Authorization":""
        }
        self.updateApiKey()
    def updateApiKey(self):
        with open("API_KEY", "r") as api:
            self.HEADERS["Authorization"] = api.read()
        print(self.HEADERS)
    def checkRemoteVersion(self):
        response = requests.get(self.API_URL, headers=self.HEADERS)
        response.raise_for_status()
        release_data = response.json()
        assets = release_data.get("assets", [])
        if not assets:
            raise ValueError("No assets found in the latest release.")
        return assets
    def downloadPackage(self, assets:list):
        asset = self.checkRemoteVersion()[0]
        download_url = asset["browser_download_url"]
        asset_response = requests.get(download_url, stream=True)
        asset_response.raise_for_status()
        filename = asset["name"]
        with open(filename, "wb") as file:
            for chunk in asset_response.iter_content(chunk_size=8192):
                file.write(chunk)