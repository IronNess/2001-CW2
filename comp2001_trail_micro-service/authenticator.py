import requests

AUTHENTICATOR_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def authenticate_user(email, password):
    """Authenticate a user using the external Authenticator API."""
    try:
        response = requests.post(
            f"{AUTHENTICATOR_API_URL}/login",
            json={"email": email, "password": password},
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error connecting to Authenticator API: {e}")
        return None