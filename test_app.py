from app import app, movies


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health():
    response = client().get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert "commit" in response.json


def test_movies_api():
    response = client().get("/api/movies")

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_add_movie():
    c = client()

    before = len(movies)

    response = c.post(
        "/add",
        data={
            "title": "Test Movie",
            "genre": "Comedy",
            "language": "Hindi",
            "mood": "Happy",
            "rating": "8"
        }
    )

    assert response.status_code == 302
    assert len(movies) == before + 1


def test_invalid_movie():
    response = client().post(
        "/add",
        data={
            "title": "",
            "genre": "Comedy",
            "language": "Hindi",
            "mood": "Happy",
            "rating": "8"
        }
    )

    assert response.status_code == 400


def test_movie_filter():
    response = client().get(
        "/?mood=Happy&genre=Comedy&language=Hindi"
    )

    assert response.status_code == 200
    assert b"3 Idiots" in response.data
    assert b"Interstellar" not in response.data


def test_movies_api_contains_required_fields():
    response = client().get("/api/movies")

    assert response.status_code == 200
    assert len(response.json) > 0

    movie = response.json[0]

    assert "id" in movie
    assert "title" in movie
    assert "genre" in movie
    assert "language" in movie
    assert "mood" in movie
    assert "rating" in movie
