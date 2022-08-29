from app.models.board_game import BoardGame, Designer, Genre, Publisher
from app.models.collection import Collection
from app.models.review import Review
from app.models.user import User


def insert_test_data():
    _insert_genres()
    _insert_publishers()
    _insert_designers()
    _insert_board_games()
    _insert_users()
    _insert_reviews()
    _insert_collection()


def _insert_genres():
    genres = [
        Genre(
            name="Engine-builder",
            description="Players slowly build up a system of generating resources, money, or victory points.",
        ),
        Genre(
            name="Cooperative",
            description="Players work with one another in order to achieve a common objective.",
        ),
        Genre(
            name="RPG",
            description="Players take on the roles of imaginary characters who engage in adventures, typically in a particular fantasy setting",
        ),
    ]

    for genre in genres:
        genre.insert()


def _insert_publishers():
    publishers = [
        Publisher("Indie Boards & Cards"),
        Publisher("FryxGames"),
        Publisher("Z-Man Games"),
        Publisher("Keymaster Games"),
        Publisher("Repos Production"),
        Publisher("Stonemaier Games"),
    ]

    for publisher in publishers:
        publisher.insert()


def _insert_designers():
    designers = [
        Designer("Rikki", "Tahta"),
        Designer("Jacob", "Fryxelius"),
        Designer("Matt", "Leacock"),
        Designer("Henry", "Audubon"),
        Designer("Antoine", "Bauza"),
        Designer("Elizabeth", "Hargrave"),
    ]

    for designer in designers:
        designer.insert()


def _insert_board_games():
    games = [
        BoardGame(
            "Wingspan",
            "Attract a beautiful and diverse collection of birds to your aviary.",
            1,
            5,
            50,
            "2019-09-01",
            10,
            2.55,
            1,
            6,
            6,
            "https://boardgamegeek.com/image/4458123/wingspan",
        ),
        BoardGame(
            "7 Wonders Duel",
            "Science? Military? What will you draft to win this head-to-head version of 7 Wonders?",
            2,
            2,
            30,
            "2018-01-01",
            10,
            2.22,
            1,
            5,
            5,
            "https://cf.geekdo-images.com/zdagMskTF7wJBPjX74XsRw__itemrep/img/x5L93n_pSsxfFZ0Ir-JqtjLf-Jw=/fit-in/246x300/filters:strip_icc()/pic2576399.jpg",
        ),
        BoardGame(
            "Parks",
            "Hike through National Parks tiles, collecting memories and admiring gorgeous scenery.",
            1,
            5,
            40,
            "2019-01-01",
            10,
            2.16,
            3,
            4,
            4,
            "https://cf.geekdo-images.com/mF2cSNRk2O6HtE45Sl9TcA__opengraph/img/uoYOX2JqGtmeJ6o5wMmfypahWEs=/fit-in/1200x630/filters:strip_icc()/pic4852372.jpg",
        ),
        BoardGame(
            "Pandemic",
            "Your team of experts must prevent the world from succumbing to a viral pandemic.",
            1,
            4,
            45,
            "2008-06-01",
            8,
            2.41,
            2,
            3,
            3,
            "https://cdn.waterstones.com/override/v5/large/0681/7067/0681706711003.jpg",
        ),
        BoardGame(
            "Terraforming Mars",
            "Compete with rival CEOs to make Mars habitable and build your corporate empire.",
            1,
            5,
            120,
            "2016-01-01",
            12,
            3.25,
            1,
            2,
            2,
            "https://www.boardgamequest.com/wp-content/uploads/2016/11/Terraforming-Mars-300x300.jpg",
        ),
        BoardGame(
            "Coup",
            "Bluff (and call bluffs!) to victory in this card game with no third chances.",
            2,
            6,
            15,
            "2013-11-01",
            10,
            2.1,
            3,
            1,
            1,
            "https://m.media-amazon.com/images/I/61JeFo5pWVL._AC_SY879_.jpg",
        ),
    ]

    for game in games:
        game.insert()


def _insert_users():
    users = [
        User(
            "630638af7fea339f9931f90c",
            "admin",
            "admin@games.io",
            "2022-08-28T3:41:51.0000Z",
        ),
        User(
            "630639007fea339f9931f921",
            "user",
            "user@games.io",
            "2022-08-28T3:43:12.0000Z",
        ),
    ]

    for user in users:
        user.insert()


def _insert_reviews():
    review_1 = Review(
        1,
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        5,
        1,
    )
    review_1._user_likes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    review_1._user_dislikes = [10, 11, 12]

    reviews = [
        review_1,
        Review(
            2,
            "Lectus vestibulum mattis ullamcorper velit sed ullamcorper.",
            4,
            1,
        ),
        Review(
            3,
            "Vivamus at augue eget arcu. Quam pellentesque nec nam aliquam sem et tortor.",
            3,
            1,
        ),
        Review(
            4,
            "Massa sapien faucibus et molestie ac feugiat. Risus in hendrerit gravida rutrum quisque non tellus orci ac.",
            4,
            1,
        ),
        Review(
            1,
            "Id interdum velit laoreet id donec ultrices. Venenatis a condimentum vitae sapien pellentesque.",
            5,
            2,
        ),
        Review(
            2,
            "Diam volutpat commodo sed egestas egestas fringilla phasellus faucibus. Scelerisque fermentum dui faucibus in. In ornare quam viverra orci.",
            2,
            2,
        ),
        Review(
            3,
            "Quis viverra nibh cras pulvinar mattis nunc sed blandit libero. Sit amet commodo nulla facilisi.",
            5,
            2,
        ),
    ]

    for review in reviews:
        review.insert()


def _insert_collection():
    collection_1 = Collection(1)
    collection_1.add(1)
    collection_1.add(2)
    collection_1.add(3)
    collection_2 = Collection(2)
    collection_2.add(2)
    collection_2.add(6)
    collections = [collection_1, collection_2]

    for collection in collections:
        collection.insert()
