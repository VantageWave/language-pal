from customtypes.error_types import CustomHttpErrorCode
import firebase_admin
from firebase_admin import auth, firestore

app = firebase_admin.initialize_app()
db = firestore.client()

def get_token(authorization_header=None):
    if isinstance(authorization_header, str) and authorization_header.startswith("Bearer "):
        return authorization_header.split("Bearer ")[1]
    else:
        return None

def check_id_token_exists(request):
    id_token = get_token(request.headers.get("X-Function-Authorization"))
    if id_token is None:
        return {
            "code": CustomHttpErrorCode.UNAUTHORIZED.value,
            "message": "Unauthorized",
        }, 403
    return id_token

def get_decoded_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        if decoded_token is None:
            return {
                "code": CustomHttpErrorCode.UNAUTHORIZED.value,
                "message": "Unauthorized",
            }, 403
        return decoded_token
    except Exception as error:
        print(f"Error verifying ID token: {error}")
        return None

def get_user(decoded_token):
    user = db.collection('users').document(decoded_token['uid']).get().to_dict()
    if user is None:
        return {
            "code": CustomHttpErrorCode.NO_REQUESTS_AVAILABLE.value,
            "message": "Not enough request tokens.",
        }, 400
    return user

def check_user_tokens(user):
    try:
        if user['requestsPool'] <= 0:
            return {
                "code": CustomHttpErrorCode.NO_REQUESTS_AVAILABLE.value,
                "message": "Not enough request tokens.",
            }, 400
    except Exception as e:
        return {
            "code": CustomHttpErrorCode.DATABASE_ERROR.value,
            "message": "Database error",
        }, 500

def update_user_token(user, value = 1):
    try:
        db.collection('users').document(user["uid"]).update({
          'requestsPool': user.get('requestsPool') - value
        })
    except Exception as e:
        return {
            "code": CustomHttpErrorCode.DATABASE_ERROR.value,
            "message": "Database error",
            "error": str(e),
        }, 500

def verify_user(request):
    id_token = check_id_token_exists(request)
    decoded_token = get_decoded_token(id_token)
    user = get_user(decoded_token)
    return user