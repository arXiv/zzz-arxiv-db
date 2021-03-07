import jwt


def decode(token: str, secret: str):
    """Decode an auth token to access session information."""
    data = dict(jwt.decode(token, secret, algorithms=['HS256']))
    return data
