import pytest

from app.auth.errors import AuthError
from app.utils.auth0 import (
    _validate_bearer_token,
    check_permissions,
    requires_auth,
    verify_decode_jwt,
)

# ===========
#  Fixtures
# ===========


@pytest.fixture()
def jwks() -> dict:
    return {
        "keys": [
            {
                "alg": "RS256",
                "kty": "RSA",
                "use": "sig",
                "n": "tCHvWwxolSJ5KIr2ZuX_ZMhAzWgVXOEndbdQ2kt6VeF2LhGcaY-iz1h7FrYW_xwCbw4RrnpLl8RitOJ7XyqZJuQD37-Ch4Pw8Gr19x01vWnoC3cp1yix0Ee5DAUzhewUg-671o6iTsKw8Bf3TnoFZthIvjnI8b83Ou8U-jRxiKxwhKm3zsYMB5CRkINkaz8KG3LoPUv0yNM6Rbd3SCPzYuy_chQPhNTnJRYA5JXsnqLohU_OTYVxsx2ZOpy4ELmiyNXrC2C_Vqcez6RUwRAbeJtWalMTuz3OrUMecT5_YsChK0oTOBz6PGBLAWn-gcNNWPndI32nTKYLNx0NWVhKiw",
                "e": "AQAB",
                "kid": "I7X1nELwFkmw5pX3OgXRY",
                "x5t": "2m4YKjbt23k_k4Br9gEiaDvko7U",
                "x5c": [
                    "MIIDDTCCAfWgAwIBAgIJCwsuWP9e4gYzMA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGWRldi10LTBsYTFpaC51cy5hdXRoMC5jb20wHhcNMjIwNzI3MjAyOTM0WhcNMzYwNDA0MjAyOTM0WjAkMSIwIAYDVQQDExlkZXYtdC0wbGExaWgudXMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtCHvWwxolSJ5KIr2ZuX/ZMhAzWgVXOEndbdQ2kt6VeF2LhGcaY+iz1h7FrYW/xwCbw4RrnpLl8RitOJ7XyqZJuQD37+Ch4Pw8Gr19x01vWnoC3cp1yix0Ee5DAUzhewUg+671o6iTsKw8Bf3TnoFZthIvjnI8b83Ou8U+jRxiKxwhKm3zsYMB5CRkINkaz8KG3LoPUv0yNM6Rbd3SCPzYuy/chQPhNTnJRYA5JXsnqLohU/OTYVxsx2ZOpy4ELmiyNXrC2C/Vqcez6RUwRAbeJtWalMTuz3OrUMecT5/YsChK0oTOBz6PGBLAWn+gcNNWPndI32nTKYLNx0NWVhKiwIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBRcAgr1Y6jK1OP/UFAa+kYfuoVsCTAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBAKNX77y++F0Sid+pSWxaefpW5mMKsKMKQhlW/N5hxowtR619RdMHCwhIVF0eatpmAQKKSeWRlgUvkv8uJyv2DgbVDbn+EaR22a526j3fI+OHkHyarQWKU3qa97YfMCXTv+0kEeZcIujFGGSkOCe4J7gjygAwb9ADtZO0lAOdOeRxbpSwwIJ9vbFPWG41dpPz2+74DQhgbBOn0moKBIuPdGymevEPyNVE2qJRr3Vx4sG6m65oPQy6pvTvY+5Dl0UsQxxQB8ki4W23Y5baL4kDkTEYJTfbjaCrEkox7ir8VDWNFzCG4C46S4NbobyeJ896+XrgUtkwNeKJk07glXRe9yY="
                ],
            },
            {
                "alg": "RS256",
                "kty": "RSA",
                "use": "sig",
                "n": "6fELrjrVA2pK5wXg5fb_OtgQYUQzNGfAAN85juRez0d9J9a681jqL1T-amb3xygObbNJJJ6pPKJ0IXEBAMepTa45bZ26XcXgIRYki6ByNFfuJvliLIye7pGaQUsujEEQnkGrjKxTBJo7x2D4dIxYLRrhyjOf4RNsN7hjINcCJaA1NDRAmBPjPhkfVyjmmH6OJ7GSaQEva7c0-F5gVsWa3lrxp9amL3HzE26JCZsjgcaIC4Gd4qy2WKRtXjZG0SA_8GrGgmffjNEQ6MoMymOCowfXC0uVmkT2gMWIZXCV7xM8aisXSN8_xCyYr5KLNSi6XnyT3On697skC77VWc_65w",
                "e": "AQAB",
                "kid": "XVT4cr2S4QTRSnIHU-T94",
                "x5t": "nZogblwFfboo4uTZsSNBQ6_XOKY",
                "x5c": [
                    "MIIDDTCCAfWgAwIBAgIJddELbR0oPAA+MA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGWRldi10LTBsYTFpaC51cy5hdXRoMC5jb20wHhcNMjIwNzI3MjAyOTM0WhcNMzYwNDA0MjAyOTM0WjAkMSIwIAYDVQQDExlkZXYtdC0wbGExaWgudXMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6fELrjrVA2pK5wXg5fb/OtgQYUQzNGfAAN85juRez0d9J9a681jqL1T+amb3xygObbNJJJ6pPKJ0IXEBAMepTa45bZ26XcXgIRYki6ByNFfuJvliLIye7pGaQUsujEEQnkGrjKxTBJo7x2D4dIxYLRrhyjOf4RNsN7hjINcCJaA1NDRAmBPjPhkfVyjmmH6OJ7GSaQEva7c0+F5gVsWa3lrxp9amL3HzE26JCZsjgcaIC4Gd4qy2WKRtXjZG0SA/8GrGgmffjNEQ6MoMymOCowfXC0uVmkT2gMWIZXCV7xM8aisXSN8/xCyYr5KLNSi6XnyT3On697skC77VWc/65wIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBQ1ZJkqVu2ZD7k1t2c53WqxQfMQgDAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBALieNWvpHXlMZOztlDGur8arx9R6zWydOKgvO9RcXNgM5L/7w+jt7RidnLtaaMDkSi42fBWh11pKK06iwBrtV2eEK6VWfn1IlPwAFzVYIdNfcQeXrEiaX/9ncG35ulg9pKFKrii8w4HsBTA9p04Hu+SdPpuDDjNIWJ+9LP8kKqMkhEhtHnW6jdtoCJSHMrYKLMAUT4oLm9eqQ2ftrHI3ZxP7MZayTS6JyGABC5+v0IlKF4elxBkV+a4LjYeceCmU0NE41eXtKc5y8ucrGutLN9PE069LYuOrNQd7GlAjMW/ZODnEaGevAmjpzAjNghy2dGKOM0zw8gjs5aEWVj5Uhas="
                ],
            },
        ]
    }


# TODO get actual token with permissions
@pytest.fixture()
def token() -> str:
    return "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikk3WDFuRUx3RmttdzVwWDNPZ1hSWSJ9.eyJuaWNrbmFtZSI6InVzZXIiLCJuYW1lIjoidXNlciIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci8wMGZkYjRhZjk0YzEzOWVlOTFmNGRhNjZhNTc1MjY3Yj9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRnVzLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDIyLTA4LTI3VDE4OjU3OjA0LjE4OFoiLCJlbWFpbCI6InVzZXJAZ2FtZXMuaW8iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOi8vZGV2LXQtMGxhMWloLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzA2MzkwMDdmZWEzMzlmOTkzMWY5MjEiLCJhdWQiOiJGaDNPaXh3dlFXTUMwWGxsRGJLOWFRT2twUW9aM1lJcCIsImlhdCI6MTY2MTYyNjYyNCwiZXhwIjoxNjYxNzEzMDI0LCJzaWQiOiJHNlNZc2pYNUZiU2JQUGs4Zzgxa1h5UDAwaVFyR0ktUSIsIm5vbmNlIjoiQXhPVHo4dFRXWUdyNWpoYTFGVWgifQ.QQBV-Ty1rp3Zk6n8IVCfoNmtgH1E165OtsDeCAHRRfg8mYhJRJn3iMFj9KWCLsYYProo6CpwfglZweSphWn93Cobky1k2J2gcj5xbBC9PweESkfkx8JOSBYiex8ios1nQf8vuqriREIcMjtcFHjTtuApiOIfvupwQoTWQTclClXRyf_0qPE38glVJkwzNj2WiEOd19oO9L9Q5ThTOB86Rlv63_r6Dmc5Vd4IYWLTyVLByJy99eAXp01W-TpbUX8xpSlqXapTr3rVlJf-8Y1lX13BztrS4E7WEdwqBH4-86duGL5Y_iZdtmu9TfuiWmiizuCSoILt2jjtyEgQD_AOzw"


@pytest.fixture()
def token_decoded() -> dict:
    return {
        "nickname": "user",
        "name": "user",
        "picture": "https://s.gravatar.com/avatar/00fdb4af94c139ee91f4da66a575267b?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fus.png",
        "updated_at": "2022-08-27T18:57:04.188Z",
        "email": "user@games.io",
        "email_verified": False,
        "iss": "https://dev-t-0la1ih.us.auth0.com/",
        "sub": "auth0|630639007fea339f9931f921",
        "aud": "Fh3OixwvQWMC0XllDbK9aQOkpQoZ3YIp",
        "iat": 1661626624,
        "exp": 1661713024,
        "sid": "G6SYsjX5FbSbPPk8g81kXyP00iQrGI-Q",
        "nonce": "AxOTz8tTWYGr5jha1FUh",
    }


# ===========
#  Tests
# ===========


def test_validate_bearer_token():
    token = "Bearer eyJhbGciO"
    assert _validate_bearer_token(token)


def test_validate_bearer_token_raises_invalid_header():
    token = "Bearer eyJhbGciO 0g9tew2jH"
    with pytest.raises(
        AuthError, match="must have the format 'Bearer {{bearer_token}}"
    ):
        _validate_bearer_token(token)


def test_validate_bearer_token_raises_invalid_header_no_bearer():
    token = "eyJhbGciO"
    with pytest.raises(AuthError, match="The prefix has to be 'Bearer'"):
        _validate_bearer_token(token)


def test_check_permissions():
    payload = {
        "user_id": 1,
        "permissions": ["get:games", "post:reviews", "patch:reviews"],
    }
    assert check_permissions("post:reviews", payload)


def test_check_permissions_raises_auth_error_empty_claims():
    payload = {"user_id": 1}
    with pytest.raises(AuthError, match="Permissions list not included in JWT"):
        check_permissions("post:reviews", payload)


def test_check_permissions_raises_auth_error_missing_permission():
    payload = {
        "user_id": 1,
        "permissions": ["get:games", "post:reviews", "patch:reviews"],
    }
    with pytest.raises(AuthError, match="Permission not found"):
        check_permissions("patch:genres", payload)


# TODO

# def test_verify_decode_jwt(mocker, jwks, token):  # TODO: (mock jwks)
#     mocker.patch(
#         "app.utils.auth0._retrieve_jwks",
#         return_value=jwks,
#     )
#     verify_decode_jwt(token)
#     # assert equal to payload


# def test_verify_decode_jwt_raises_auth_error():  # (kid not in header)
#     pass


# def test_verify_decode_jwt_raises_claims_error():
#     pass


# def verify_decode_jwt_raises_expired_signature_error():
#     pass


# def test_verify_decode_jwt_raises_auth_error_cannot_parse_token():
#     pass


# def test_verify_decode_jwt_raises_auth_error_missing_rsa_key():
#     pass
