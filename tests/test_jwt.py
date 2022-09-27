import modapi.auth as auth


def test_encode_decode():
    data = auth.Auth(
        user_id="1234344", session_id="2342432", nonce="cheeseburger", expires="foo"
    )
    sec = "l2k3j4lkjlkdsj"
    assert auth.decode(auth.encode(data, sec), sec) == data
