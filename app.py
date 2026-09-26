import os
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

movies = [
    {
        "id": 1,
        "title": "3 Idiots",
        "genre": "Comedy",
        "language": "Hindi",
        "mood": "Happy",
        "rating": 8.4
    },
    {
        "id": 2,
        "title": "Queen",
        "genre": "Drama",
        "language": "Hindi",
        "mood": "Happy",
        "rating": 8.1
    },
    {
        "id": 3,
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "language": "English",
        "mood": "Excited",
        "rating": 8.7
    },
    {
        "id": 4,
        "title": "Yeh Jawaani Hai Deewani",
        "genre": "Romance",
        "language": "Hindi",
        "mood": "Romantic",
        "rating": 7.2
    },
    {
        "id": 5,
        "title": "KGF",
        "genre": "Action",
        "language": "Kannada",
        "mood": "Excited",
        "rating": 8.2
    },
    {
        "id": 6,
        "title": "Premam",
        "genre": "Romance",
        "language": "Malayalam",
        "mood": "Romantic",
        "rating": 8.3
    },
    {
        "id": 7,
        "title": "Sairat",
        "genre": "Romance",
        "language": "Marathi",
        "mood": "Romantic",
        "rating": 8.0
    }
]


COMMIT = os.getenv(
    "RENDER_GIT_COMMIT",
    os.getenv("GIT_SHA", "local")
)[:7]


@app.route("/")
def home():
    mood = request.args.get("mood", "").strip()
    genre = request.args.get("genre", "").strip()
    language = request.args.get("language", "").strip()

    recommended = movies

    if mood:
        recommended = [
            movie for movie in recommended
            if movie["mood"].lower() == mood.lower()
        ]

    if genre:
        recommended = [
            movie for movie in recommended
            if movie["genre"].lower() == genre.lower()
        ]

    if language:
        recommended = [
            movie for movie in recommended
            if movie["language"].lower() == language.lower()
        ]

    return render_template(
        "index.html",
        movies=recommended,
        selected_mood=mood,
        selected_genre=genre,
        selected_language=language,
        commit=COMMIT
    )


@app.route("/add", methods=["POST"])
def add_movie():
    title = request.form.get("title", "").strip()
    genre = request.form.get("genre", "").strip()
    language = request.form.get("language", "").strip()
    mood = request.form.get("mood", "").strip()
    rating_text = request.form.get("rating", "").strip()

    if not title or not genre or not language or not mood or not rating_text:
        return "All fields are required", 400

    try:
        rating = float(rating_text)
    except ValueError:
        return "Rating must be a number", 400

    if rating < 0 or rating > 10:
        return "Rating must be between 0 and 10", 400

    new_movie = {
        "id": len(movies) + 1,
        "title": title,
        "genre": genre,
        "language": language,
        "mood": mood,
        "rating": rating
    }

    movies.append(new_movie)

    return redirect("/")


@app.route("/api/movies")
def api_movies():
    return jsonify(movies)


@app.route("/health")
def health():
    return {
        "status": "ok",
        "commit": COMMIT
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )