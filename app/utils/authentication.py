from flask import session


# TODO: may not need to pass in session?
def get_current_user_id(session: session) -> str:
    return session["user"]["userinfo"]["sub"].split("|")[-1]


def check_user_id(user_id: str) -> bool:
    return user_id == get_current_user_id(session)
