from datetime import datetime, timedelta

import jwt


def generate_jwt(payload, expiry, secret):
    _payload = {'exp': expiry}
    _payload.update(payload)

    if not secret:
        pass
    token = jwt.encode(playload=_payload, key=secret, algorithm='HS256')
    return token.decode()


def verify_jwt(token, secret=None):
    if not secret:
        pass
    try:
        payload = jwt.decode(token, secret, algorithm='HS256')
    except jwt.PyJWTError:
        payload = None
    return payload


if __name__ == '__main__':
    expiry = datetime.utcnow() + timedelta(hours=1)
