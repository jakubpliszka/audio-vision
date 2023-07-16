import requests
import json


class AspenAPI:
    SERVER_PORT = 3000

    token = None
    user_id = None
    tenant_db = None

    def __init__(self, user_api_key: str, tenant_id: str, server_ip_address: str = "localhost") -> None:
        self.server_url = f"http://{server_ip_address}:{self.SERVER_PORT}"
        self.user_api_key = user_api_key
        self.tenant_id = tenant_id

        self.login()

    def __del__(self) -> None:
        self.logout()

    def login(self) -> None:
        headers = {
            "Content-Type": "application/json",
            "api_key": self.user_api_key,
            "api_type": "user"
        }

        body = {
            "tenant_id": self.tenant_id
        }

        url = self.server_url + "/auth/api-login"
        response = requests.post(url=url, headers=headers, data=json.dumps(body))

        if not response.status_code == 201:
            raise Exception(f"Error with login response: {response.text}")

        data = json.loads(response.text)
        self.token = data["token"]
        self.user_id = data["userId"]
        self.tenant_db = data["tenantDb"]

    def logout(self) -> None:
        if not self.token or not self.user_id or not self.tenant_db:
            raise Exception("Not logged in")

        headers = {
            "Content-Type": "application/json",
            "api_key": self.user_api_key,
            "api_type": "user",
            "token": self.token,
            "user-id": self.user_id,
            "tenant-db": self.tenant_db
        }

        url = self.server_url + "/auth/logout"

        body = {
            "token": self.token
        }

        response = requests.post(url=url, headers=headers, data=json.dumps(body))
        if response.status_code != 201:
            raise Exception("Logout failed")

    def open_tray(self) -> None:
        if not self.token or not self.user_id or not self.tenant_db:
            raise Exception("Not logged in")

        headers = {
            "Content-Type": "application/json",
            "api_key": self.user_api_key,
            "api_type": "user",
            "token": self.token,
            "user-id": self.user_id,
            "tenant-db": self.tenant_db
        }

        url = self.server_url + "/device-driver/autosampler/compound-movement/tray"

        body = {
            "tray_out": True,
        }

        response = requests.patch(url=url, headers=headers, data=json.dumps(body))
        if response.status_code != 200:
            raise Exception("Open tray failed")

    def close_tray(self) -> None:
        if not self.token or not self.user_id or not self.tenant_db:
            raise Exception("Not logged in")

        headers = {
            "Content-Type": "application/json",
            "api_key": self.user_api_key,
            "api_type": "user",
            "token": self.token,
            "user-id": self.user_id,
            "tenant-db": self.tenant_db
        }

        url = self.server_url + "/device-driver/autosampler/compound-movement/tray"

        body = {
            "tray_out": False,
        }

        response = requests.patch(url=url, headers=headers, data=json.dumps(body))
        if response.status_code != 200:
            raise Exception("Open tray failed")
