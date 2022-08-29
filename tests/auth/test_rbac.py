"""
Examples of role-based access control tests for various endpoints.

Users can write reviews, so can admins
Admins can create board games, users cannot
"""


def test_missing_authorization_header():
    pass


"""
Remaining tests can be found in attached Postman collection.
"""


"""
User
- get all games
- post a game
- update a game
- delete a game

Admin
- get all games
- post a game
- update a game
- delete a game
"""
