import os
import requests
from dotenv import load_dotenv


load_dotenv()
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


class API:
    # Owners
    @staticmethod
    def list_owners():
        r = requests.get(f"{API_BASE}/owners/")
        r.raise_for_status()
        return r.json()


    @staticmethod
    def create_owner(payload: dict):
        r = requests.post(f"{API_BASE}/owners/", json=payload)
        r.raise_for_status()
        return r.json()


    # Pets
    @staticmethod
    def list_pets(owner_id: int | None = None):
        params = {"owner_id": owner_id} if owner_id else None
        r = requests.get(f"{API_BASE}/pets/", params=params)
        r.raise_for_status()
        return r.json()


    @staticmethod
    def create_pet(payload: dict):
        r = requests.post(f"{API_BASE}/pets/", json=payload)
        r.raise_for_status()
        return r.json()


    # Appointments
    @staticmethod
    def list_appointments(day: str | None = None):
        params = {"day": day} if day else None
        r = requests.get(f"{API_BASE}/appointments/", params=params)
        r.raise_for_status()
        return r.json()


    @staticmethod
    def create_appointment(payload: dict):
        r = requests.post(f"{API_BASE}/appointments/", json=payload)
        if r.status_code == 409:
            raise ValueError("Conflicto de horario para ese veterinario")
            r.raise_for_status()
        return r.json()


    @staticmethod
    def update_appointment(appt_id: int, payload: dict):
        r = requests.put(f"{API_BASE}/appointments/{appt_id}", json=payload)
        r.raise_for_status()
        return r.json()