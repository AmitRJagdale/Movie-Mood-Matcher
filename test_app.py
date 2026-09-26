from app import app, movies


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health():
    response = client().get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"


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