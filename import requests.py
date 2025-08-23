import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

auth = HTTPBasicAuth(USER, PASSWORD)


def get_devices():
    """Obtener lista de dispositivos"""
    url = f"{BASE_URL}/api/devices"
    r = requests.get(url, auth=auth)
    r.raise_for_status()
    return r.json()


def get_positions(device_id, date_from, date_to, limit=None):
    """
    Obtener posiciones de un dispositivo entre dos fechas.
    Formato de fechas: '2025-08-22T00:00:00Z'
    """
    url = f"{BASE_URL}/api/positions"
    params = {"deviceId": device_id, "from": date_from, "to": date_to}
    if limit:
        params["limit"] = limit
    r = requests.get(url, auth=auth, params=params)
    r.raise_for_status()
    return r.json()


def get_latest_position(device_id):
    """Obtener la última posición de un dispositivo"""
    url = f"{BASE_URL}/api/positions"
    params = {"deviceId": device_id, "limit": 1}
    r = requests.get(url, auth=auth, params=params)
    r.raise_for_status()
    data = r.json()
    return data[-1] if data else None


def send_command(device_id, cmd_type, attributes=None):
    """
    Enviar comando a un dispositivo.
    Ejemplos de cmd_type: 'engineStop', 'engineResume'
    """
    url = f"{BASE_URL}/api/commands/send"
    body = {"deviceId": device_id, "type": cmd_type}
    if attributes:
        body["attributes"] = attributes
    r = requests.post(url, auth=auth, json=body)
    r.raise_for_status()
    return r.json()
