from datetime import datetime

from app.models.user import User


def test_create_user():
    user = User(
        auth0_id="0001",
        username="admin",
        email="admin@games.io",
        updated_at="2022-01-01T09:00:00.0001Z",
    )

    assert user.auth0_id == "0001"
    assert user.username == "admin"
    assert user.email == "admin@games.io"
    assert user.updated_at == datetime(
        year=2022, month=1, day=1, hour=9, minute=0, second=0, microsecond=100
    )
