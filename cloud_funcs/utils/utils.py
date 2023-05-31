def get_token(authorization_header=None):
    if isinstance(authorization_header, str) and authorization_header.startswith("Bearer "):
        return authorization_header.split("Bearer ")[1]
    else:
        return None

def check_id_token_exists(request):
    return get_token(request.headers.get("X-Function-Authorization"))

from firebase_admin import auth

def get_decoded_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as error:
        print(f"Error verifying ID token: {error}")
        return None
