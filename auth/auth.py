import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-kgm20.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'gamingtourney'

'''
Most of the code on this script comes from auth0 documentation:

https://auth0.com/docs/quickstart/backend/python/01-authorization
#validate-access-tokens
'''


class AuthError(Exception):
    """
    AuthError Exception
    A standardized way to communicate auth failure modes
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    This method obtains the JWT recevied on the Authorization headers.

    We ensure the header is an authorization bearer token and then obtain the
    JWT from it.

    Parameters:
    Authorization (string): This is the auth0 Bearer Token that corresponds
                            to the current user session Authorization header.

    Returns:
    token (string): This is the encoded JWT provided by our auth0 server.

    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            "success": False,
            "error": 401,
            "message": "Authorization header is expected."
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            "success": False,
            "error": 401,
            "message": "Authorization header must start with 'Bearer'."
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            "success": False,
            "error": 401,
            "message": "Token not found."
        }, 401)

    elif len(parts) > 2:
        print(len(parts))
        raise AuthError({
            "success": False,
            "error": 401,
            "message": "Authorization header must be bearer token."
        }, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    """
    This method ensures that the current session has the permission to perform
    an specific action.

    Parameters:
    permission (string): This is the permission required to perform the action
                         that called this method before it begins to work

    payload (string): The payload contains the permissions from the current
                      session

    Returns:
    True (boolean): This means the session has the required permission

    """
    if 'permissions' not in payload:
        raise AuthError({
            "success": False,
            "error": 400,
            "message": "Payload does not contain permissions."
        }, 400)

    elif permission not in payload['permissions']:
        raise AuthError({
            "success": False,
            "error": 403,
            "message": "Token has not the required persmission."
        }, 403)

    return True


def verify_decode_jwt(token):
    """
    This method ensures that the received JWT is valid an decode it.

    First, the functions reads the JSON Web Key Set (JWKS) containing the
    public keys to verify any JSON Web Token (JWT) issued by our authorization
    server. Then, after the JWT was successfully verified,we create a payload
    that contatins the decrypted JWT using the RSA key to decode it.

    Parameters:
    token (string): This is the auth0 encoded JWT obtained as the result from
                    the get_token_auth_header() method.

    Returns:
    payload (string): This is the decoded JWT that was originally received.

    """
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            "success": False,
            "error": 401,
            "message": "Authorization malformed."
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                "success": False,
                "error": 401,
                "message": "Token has expired."
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                "success": False,
                "error": 401,
                "message": "Incorrect claims. Please,\
                 check the audience and issuer."
            }, 401)
        except Exception:
            raise AuthError({
                "success": False,
                "error": 400,
                "message": "Unable to parse authentication token."
            }, 400)
    raise AuthError({
        "success": False,
        "error": 400,
        "message": "Unable to find the appropriate key."
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
