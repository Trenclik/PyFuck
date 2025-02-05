import requests
class Updater:
    def __init__(self):
        self.REPO = "Trenclik/PyFuck"
        self.API_URL = f"https://api.github.com/repos/{self.REPO}/releases/latest"
        self.HEADERS = {
            "Accept":"application/vnd.github.v3+json",
            #"Authorization":""
        }
        self.update()
    def update(self):
        with open("API_KEY", "r") as api:
            self.HEADERS["Authorization"] = api.read()
        with open("VERSION", "r") as ver:
            self.VERSION = ver.read()
    def checkRemoteVersion(self):
        response = requests.get(self.API_URL, headers=self.HEADERS)
        response.raise_for_status()
        release_data = response.json()
        ver = release_data.get("tag_name")
        assets = release_data.get("assets", [])
        if ver == self.VERSION:
            return True
        elif not assets:
            raise ValueError("No assets found in the latest release.")
        return assets
    def downloadPackage(self, assets):
        try:
            if assets == True:
                print("bruh")
                return
        except ValueError as err:
            print(err)
        except:
            download_url = assets["browser_download_url"]
            asset_response = requests.get(download_url, stream=True)
            asset_response.raise_for_status()
            filename = assets["name"]
            with open(filename, "wb") as file:
                for chunk in asset_response.iter_content(chunk_size=8192):
                    file.write(chunk)