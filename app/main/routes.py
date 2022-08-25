from flask import abort, jsonify, request, session
from numpy import mean

from app.models.board_game import BoardGame, Designer, Genre, Publisher
from app.models.review import Review
from app.models.review import User

from ..utils.auth0 import requires_auth
from ..utils.authentication import check_user_id, get_current_user_id
from ..utils.requests import paginate_items
from . import main

GAMES_PER_PAGE = 10
REVIEWS_PER_PAGE = 5


# ========================
#  Board Game Enpoints
# ========================


@main.route("/games")
def get_all_games():
    games = BoardGame.query.order_by(BoardGame.id).all()
    current_games = paginate_items(request, games, GAMES_PER_PAGE)

    if not current_games:
        abort(404)

    games_with_avg_rating = []
    for game in current_games:
        reviews = Review.query.filter_by(board_game=game.id).all()
        game["avg_rating"] = (
            mean([r for r in game.rating]) if len(reviews) > 0 else None
        )
        games_with_avg_rating.append(game)

    return jsonify({"success": True, "games": games_with_avg_rating, "total_games": len(games)})


@main.route("/games/<int:game_id>")
def get_game_by_id(game_id):
    game = BoardGame.query.filter_by(id=game_id)

    reviews_for_game = Review.query.filter_by(board_game=game_id).all()
    average_rating = (
        mean([r.rating for r in reviews_for_game]) if reviews_for_game else None
    )

    if game is None:
        abort(404)

    return jsonify(
        {"success": True, "game": game.format(), "average_rating": average_rating}
    )


@main.route("/games/<int:game_id>/reviews")
def get_reviews_for_game(game_id):
    reviews_for_game = Review.query.filter_by(board_game=game_id).all()

    if not reviews_for_game:
        abort(404)

    average_rating = mean([r.rating for r in reviews_for_game])
    reviews = paginate_items(request, reviews_for_game, REVIEWS_PER_PAGE)

    return jsonify(
        {
            "success": True,
            "game_id": game_id,
            "reviews": reviews,
            "average_rating": average_rating,
            "total_review": len(reviews_for_game),
        }
    )


@main.route("/games", methods=["POST"])
@requires_auth("post:games")
def create_game():
    body = request.get_json()

    try:
        game = BoardGame(
            title=body.get("title"),
            description=body.get("description"),
            min_player_count=body.get("min_player_count"),
            max_player_count=body.get("max_player_count"),
            play_time=body.get("play_time"),  # TODO: convert to time
            release_date=body.get("release_date"),  # TODO: convert to date
            age=body.get("age"),
            weight=body.get("weight"),
            genre_id=body.get("genre_id"),
            designer_id=body.get("designer_id"),
            publisher_id=body.get("publisher_id"),
            image_link=body.get("image_link"),
        )
        game.insert()

        games = BoardGame.query.order_by(BoardGame.id).all()
        formatted_games = paginate_items(request, games, GAMES_PER_PAGE)

        return jsonify(
            {
                "success": True,
                "created": game.id,
                "games": formatted_games,
                "total_games": len(games),
            }
        )

    except:
        abort(422)


@main.route("/games/<int:game_id>", methods=["PATCH"])
@requires_auth("patch:games")
def update_game(game_id):
    game = BoardGame.query.filter_by(id=game_id).one_or_none()

    if game is None:
        abort(404)

    updates = request.get_json()

    try:
        game.title = updates.get("title", game.title)
        game.description = updates.get("description", game.description)
        game.min_player_count = updates.get("min_player_count", game.min_player_count)
        game.max_player_count = updates.get("max_player_count", game.max_player_count)
        game.play_time = updates.get(
            "play_time", game.play_time
        )  # TODO: convert to time?
        game.release_date = updates.get(
            "release_date", game.release_date
        )  # TODO: convert to date?
        game.age = updates.get("age", game.age)
        game.weight = updates.get("weight", game.weight)
        game.genre = updates.get("genre", game.genre)
        game.designer = updates.get("designer", game.designer)
        game.publisher = updates.get("publisher", game.publisher)
        game.image_link = updates.get("image_link", game.image_link)
        game.update()

        games = BoardGame.query.order_by(BoardGame.id).all()
        formatted_games = paginate_items(request, games, GAMES_PER_PAGE)

        return jsonify(
            {
                "success": True,
                "updated": game.id,
                "games": formatted_games,
                "total_games": len(games),
            }
        )
    except:
        abort(422)


@main.route("/games/<int:game_id>", methods=["DELETE"])
@requires_auth("delete:games")
def delete_game(game_id):
    game = BoardGame.query.filter_by(id=game_id).one_or_none()

    if game is None:
        abort(404)

    reviews = Review.query.filter_by(board_game=game_id).all()

    try:
        for review in reviews:
            review.delete()
        game.delete()

        return jsonify({"success": True, "deleted": game.id})
    except:
        abort(422)


# ========================
#  Review Endpoints
# ========================


@main.route("/reviews")
def get_all_reviews():
    reviews = Review.query.all()
    current_reviews = paginate_items(request, reviews, REVIEWS_PER_PAGE)

    if not current_reviews:
        abort(404)

    return jsonify(
        {"success": True, "reviews": current_reviews, "total_reviews": len(reviews)}
    )


@main.route("/reviews/<int:review_id>")
def get_review_by_id(review_id):
    review = Review.query.filter_by(id=review_id).one_or_none()

    if review is None:
        abort(404)

    return jsonify({"success": True, "review": review})


@main.route("/reviews", methods=["POST"])
@requires_auth("post:reviews")
def create_review():
    body = request.get_json()

    try:
        review = Review(
            game_id=body.get("game_id"),
            review_text=body.get("review_text"),
            rating=body.get("rating"),
            user_id=get_current_user_id(session),
        )
        review.insert()

        reviews = (
            Review.query.filter_by(board_game=body.get("game_id"))
            .order_by(Review.id)
            .all()
        )
        formatted_reviews = paginate_items(request, reviews, REVIEWS_PER_PAGE)

        return jsonify(
            {
                "success": True,
                "created": review.id,
                "reviews": formatted_reviews,
                "total_reviews_for_game": len(reviews),
            }
        )

    except:
        abort(422)


@main.route("/reviews/<int:review_id>", methods=["PATCH"])
@requires_auth("patch:reviews")
def update_review(review_id):
    review = Review.query.filter_by(id=review_id).one_or_none()

    if review is None:
        abort(404)

    if not check_user_id(review.user):
        abort(401)

    updates = request.get_json()
    try:
        review.review_text = updates.get("review_text", review.review_text)
        review.rating = updates.get("rating", review.rating)
        review.update()

        reviews = (
            Review.query.filter_by(board_game=review.get("board_game"))
            .order_by(Review.id)
            .all()
        )
        formatted_reviews = paginate_items(request, reviews, REVIEWS_PER_PAGE)

        return jsonify(
            {
                "success": True,
                "updated": review.id,
                "reviews": formatted_reviews,
                "total_reviews_for_game": len(reviews),
            }
        )
    except:
        abort(422)


@main.route("/reviews/<int:review_id>", methods=["DELETE"])
@requires_auth("delete:reviews")
def delete_review(review_id):
    review = Review.query.filter_by(id=review_id).one_or_none()

    if review is None:
        abort(404)

    if not check_user_id(review.user):
        abort(401)

    try:
        review.delete()
        return jsonify({"success": True, "deleted": review.id})
    except:
        abort(422)


@main.route("/reviews/<int:review_id>/reactions")
def get_reactions_for_review(review_id):
    review = Review.query.filter_by(id=review_id).one_or_none()

    if review is None:
        abort(404)

    return jsonify(
        {
            "success": True,
            "review_id": review.id,
            "likes": review.likes,
            "dislikes": review.dislikes,
        }
    )


@main.route("/reviews/<int:review_id>/reactions", methods=["PATCH"])
@requires_auth("patch:reactions")
def react_to_review(review_id):
    review = Review.query.filter_by(id=review_id).one_or_none()
    user_id = get_current_user_id(session)

    if review is None:
        abort(404)

    if not check_user_id(review.user):
        abort(401)

    body = request.get_json()
    try:
        if body.get("like"):
            review.like_post(user_id)
        elif body.get("dislikes"):
            review.dislike_post(user_id)
        return jsonify(
            {
                "success": True,
                "review_id": review.id,
                "likes": review.likes,
                "dislikes": review.dislikes,
            }
        )
    except:
        abort(422)


# ========================
#  Genre Endpoints
# ========================


@main.route("/genres", methods=["GET"])
def get_genres():
    genres = Genre.query.order_by(Genre.id).all()
    formatted_genres = {genre.id: genre.name for genre in genres}

    if len(formatted_genres) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "genres": formatted_genres,
            "total_genres": len(formatted_genres),
        }
    )


@main.route("/genres/<int:genre_id>")
def get_genre_by_id(genre_id):
    genre = Genre.query.filter_by(id=genre_id).one_or_none()

    if genre is None:
        abort(404)

    games = BoardGame.query.filter_by(genre=genre_id).all()

    return jsonify(
        {"success": True, "genre": genre.format(), "total_games": len(games)}
    )


@main.route("/genres/<int:genre_id>/games")
def get_games_for_genre(genre_id):
    genre = Genre.query.filter_by(id=genre_id).one_or_none()

    if genre is None:
        abort(404)

    games = BoardGame.query.filter_by(genre=genre_id).all()
    current_games = paginate_items(request, games, GAMES_PER_PAGE)

    return jsonify(
        {
            "Success": True,
            "genre": genre.format(),
            "games": current_games,
            "total_games": len(games),
        }
    )


@main.route("/genres", methods=["POST"])
@requires_auth("post:genres")
def create_genre():
    body = request.get_json()

    try:
        genre = Genre(name=body.get("name"), description=body.get("description"))
        genre.insert()

        genres = Genre.query.order_by(Genre.id).all()
        formatted_genres = {genre.id: genre.name for genre in genres}

        return jsonify(
            {"success": True, "created": genre.id, "genres": formatted_genres}
        )

    except:  # TODO: specific exception
        abort(422)


@main.route("/genres/<int:genre_id>", methods=["PATCH"])
@requires_auth("patch:genres")
def update_genre(genre_id):
    genre = Genre.query.filter_by(id=genre_id).one_or_none()

    if genre is None:
        abort(404)

    updates = request.get_json()

    try:
        genre.name = updates.get("name", genre.name)
        genre.description = updates.get("description", genre.description)
        genre.update()

        genres = Genre.query.order_by(Genre.id).all()
        formatted_genres = {genre.id: genre.name for genre in genres}

        return jsonify(
            {"success": True, "updated": genre.id, "genres": formatted_genres}
        )
    except:
        abort(422)


# ========================
#  Publisher Endpoints
# ========================


@main.route("/publishers", methods=["GET"])
def get_publishers():
    publishers = Publisher.query.order_by(Publisher.id).all()
    formatted_publishers = {publisher.id: publisher.name for publisher in publishers}

    if len(formatted_publishers) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "publishers": formatted_publishers,
            "total_publishers": len(formatted_publishers),
        }
    )


@main.route("/publishers/<int:publisher_id>")
def get_publisher_by_id(publisher_id):
    publisher = Publisher.query.filter_by(id=publisher_id).one_or_none()

    if publisher is None:
        abort(404)

    games = BoardGame.query.filter_by(publisher=publisher_id).all()

    return jsonify(
        {"success": True, "publisher": publisher.format(), "total_games": len(games)}
    )


@main.route("/publishers/<int:publisher_id>/games")
def get_games_for_publisher(publisher_id):
    publisher = Publisher.query.filter_by(id=publisher_id).one_or_none()

    if publisher is None:
        abort(404)

    games = BoardGame.query.filter_by(publisher=publisher_id).all()
    current_games = paginate_items(request, games, GAMES_PER_PAGE)

    return jsonify(
        {
            "Success": True,
            "publisher": publisher.format(),
            "games": current_games,
            "total_games": len(games),
        }
    )


@main.route("/publishers", methods=["POST"])
@requires_auth("post:publishers")
def create_publisher():
    body = request.get_json()

    try:
        publisher = Publisher(name=body.get("name"))
        publisher.insert()

        publishers = Publisher.query.order_by(Publisher.id).all()
        formatted_publishers = {
            publisher.id: publisher.name for publisher in publishers
        }

        return jsonify(
            {
                "success": True,
                "created": publisher.id,
                "publishers": formatted_publishers,
            }
        )

    except:  # TODO: specific exception
        abort(422)


@main.route("/publishers/<int:publisher_id>", methods=["PATCH"])
@requires_auth("patch:publishers")
def update_publisher(publisher_id):
    publisher = Publisher.query.filter_by(id=publisher_id).one_or_none()

    if publisher is None:
        abort(404)

    updates = request.get_json()

    try:
        publisher.name = updates.get("name", publisher.name)
        publisher.update()

        publishers = Publisher.query.order_by(Publisher.id).all()
        formatted_publishers = {
            publisher.id: publisher.name for publishers in publishers
        }

        return jsonify(
            {
                "success": True,
                "updated": publisher.id,
                "publishers": formatted_publishers,
            }
        )
    except:
        abort(422)


# ========================
#  Designer Endpoints
# ========================


@main.route("/designers", methods=["GET"])
def get_designers():
    designers = Designer.query.order_by(Designer.id).all()
    formatted_designers = {designer.id: designer.name for designer in designers}

    if len(formatted_designers) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "designers": formatted_designers,
            "total_designers": len(formatted_designers),
        }
    )


@main.route("/designers/<int:designer_id>")
def get_designer_by_id(designer_id):
    designer = Designer.query.filter_by(id=designer_id).one_or_none()

    if designer is None:
        abort(404)

    games = BoardGame.query.filter_by(designer=designer_id).all()

    return jsonify(
        {"success": True, "designer": designer.format(), "total_games": len(games)}
    )


@main.route("/designers/<int:designer_id>/games")
def get_games_for_designer(designer_id):
    designer = Designer.query.filter_by(id=designer_id).one_or_none()

    if designer is None:
        abort(404)

    games = BoardGame.query.filter_by(designer=designer_id).all()
    current_games = paginate_items(request, games, GAMES_PER_PAGE)

    return jsonify(
        {
            "Success": True,
            "designer": designer.format(),
            "games": current_games,
            "total_games": len(games),
        }
    )


@main.route("/designers", methods=["POST"])
@requires_auth("post:designers")
def create_designer():
    body = request.get_json()

    try:
        designer = Designer(
            first_name=body.get("first_name"), last_name=body.get("last_name")
        )
        designer.insert()

        designers = Designer.query.order_by(Designer.id).all()
        formatted_designers = {
            designer.id: {
                "first_name": designer.first_name,
                "last_name": designer.last_name,
            }
            for designer in designers
        }

        return jsonify(
            {"success": True, "created": designer.id, "designers": formatted_designers}
        )

    except:  # TODO: specific exception
        abort(422)


@main.route("/designers/<int:designer_id>", methods=["PATCH"])
@requires_auth("patch:designers")
def update_designer(designer_id):
    designer = Designer.query.filter_by(id=designer_id).one_or_none()

    if designer is None:
        abort(404)

    updates = request.get_json()

    try:
        designer.first_name = updates.get("first_name", designer.first_name)
        designer.last_name = updates.get("last_name", designer.last_name)
        designer.update()

        designers = Designer.query.order_by(Designer.id).all()
        formatted_designers = {
            designer.id: {
                "first_name": designer.first_name,
                "last_name": designer.last_name,
            }
            for designer in designers
        }

        return jsonify(
            {"success": True, "updated": designer.id, "designers": formatted_designers}
        )

    except:
        abort(422)


# ===========================
#  User Endpoints
# ===========================


@main.route("users/<username>/reviews")
def get_reviews_by_user(username):
    user = User.query.filter_by(username=username).one_or_none()

    if user is None:
        abort(404)

    reviews = Review.query.filter_by(user=user.id).all()
    current_reviews = paginate_items(request, reviews, REVIEWS_PER_PAGE)

    if not current_reviews:
        abort(404)

    return jsonify(
        {"success": True, "username": user.name, "user_id": user.id, "reviews": current_reviews, "total_reviews_by_user": len(reviews)}
    )


# ===========================
#  Search Endpoints
# ===========================

@main.route("/search", methods=["POST"])
def search_games():
    body = request.get_json()
    search_term = request.get_json().get("search_term", "")
    

    search_results = Question.query.filter(
        Question.question.ilike(f"%{search_term}%")
    ).all()
    questions = [question.format() for question in search_results]

    return jsonify(
        {
            "success": True,
            "search_term": search_term,
            "questions": questions,
            "total_results": len(questions),
        }
    )
