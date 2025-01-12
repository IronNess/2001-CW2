import requests

AUTHEENTICATOR_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def authenticate_user(email, password):
    try:
        response = requests.post(
            f"{AUTHEENTICATOR_API_URL}/login",
            json={"email": email, "password": password},
        )
        if response.status_code == 200:
            user_data = response.json()
            return user_data
        else:
            return None
    except Exception as e:
        print(f"Error connecting to Authenticator API: {e}")
        return None
       