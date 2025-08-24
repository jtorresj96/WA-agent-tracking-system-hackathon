import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


class TraccarAPI:
    """A client for interacting with the Traccar API."""

    def __init__(self):
        """Initializes the API client with credentials from environment variables."""
        load_dotenv()
        base_url = os.getenv("BASE_URL")
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")

        if not all([base_url, user, password]):
            raise ValueError(
                "Missing required environment variables: BASE_URL, USER, or PASSWORD."
            )

        self.base_url = base_url
        self.auth = HTTPBasicAuth(user, password)
        self.session = requests.Session()
        self.session.auth = self.auth

    def _request(self, method, endpoint, **kwargs):
        """
        A private helper method to handle API requests.
        It encapsulates common logic like URL construction and error handling.
        """
        url = f"{self.base_url}/api/{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the API request: {e}")
            raise

    def get_devices(self):
        """Fetches a list of all devices."""
        return self._request("GET", "devices")

    def get_positions(self, device_id, from_date, to_date, limit=None):
        """
        Fetches positions for a device within a date range.
        Date format: 'YYYY-MM-DDTHH:MM:SSZ'
        """
        params = {"deviceId": device_id, "from": from_date, "to": to_date}
        if limit:
            params["limit"] = limit
        return self._request("GET", "positions", params=params)

    def get_latest_position(self, device_id):
        """Fetches the latest position for a device."""
        data = self._request("GET", "positions", params={"deviceId": device_id, "limit": 1})
        return data[-1] if data else None

    def send_command(self, device_id, cmd_type, attributes=None):
        """
        Sends a command to a device.
        Example cmd_type: 'engineStop', 'engineResume'
        """
        body = {"deviceId": device_id, "type": cmd_type}
        if attributes:
            body["attributes"] = attributes
        return self._request("POST", "commands/send", json=body)


if __name__ == "__main__":
    # Example usage:
    try:
        api = TraccarAPI()
        devices = api.get_devices()
        print("Devices:", devices)

        if devices:
            first_device_id = devices[0]["id"]
            latest_pos = api.get_latest_position(first_device_id)
            print("Latest position:", latest_pos)

    except ValueError as e:
        print(f"Initialization error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"API interaction failed: {e}")