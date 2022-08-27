"""
Examples of role-based access control tests for various endpoints.

Users can write reviews, so can admins
Admins can create board games, users cannot
"""


def test_user_can_submit_review(client, review):
    pass


def test_admin_cannot_submit_review(client, review):
    pass


def test_user_cannot_add_game(client, game):
    pass


def test_admin_can_add_game(client, game):
    pass
