from flask import Flask,render_template,request
import pickle
import numpy as np
import json
import urllib.request


new11 = pickle.load(open('popular2.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
rating_with_movie = pickle.load(open('rating_with_movie.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                        movie_name = list(new11['Title'].values),
                        movie_genre = list(new11['Genre'].values),
                        image = list(new11['Poster'].values),
                        votes = list(new11['Movie-Rating'].values),
                        rating = list(new11['IMDB Score'].values))

@app.route('/recommender')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recmd_movie' ,methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    # index fetch
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:13]
    data = []

    for i in similar_items:
        item = []
        temp_df = (rating_with_movie[rating_with_movie['Title'] == pt.index[i[0]]])
        item.extend(list(temp_df.drop_duplicates('Title')['Title'].values))
        item.extend(list(temp_df.drop_duplicates('Title')['Genre'].values))
        item.extend(list(temp_df.drop_duplicates('Title')['Poster'].values))

        data.append(item)
    print(data)
    return render_template('recommend.html', data=data)

@app.route('/trending') #FOR Trending MOVIES
def get_movies():
    url = "https://api.themoviedb.org/3/discover/movie?api_key=18a017b1725a276ac9a9838ec5345147"
    response = urllib.request.urlopen(url)
    data = response.read()
    jsondata = json.loads(data)

    return render_template("latest.html", movies=jsondata["results"])


@app.route("/movies")  ## FOR UPCOMING/RELEASE MOVIES
def get_movies_list():
    url = "https://api.themoviedb.org/3/movie/upcoming?api_key=18a017b1725a276ac9a9838ec5345147"

    response = urllib.request.urlopen(url)
    data = response.read()
    jsondata1 = json.loads(data)

    movie_json = []

    for movie in jsondata1["results"]:
        movie = {
            "title": movie["title"],
            "overview": movie["overview"],
        }

        movie_json.append(movie)
    print(movie_json)
    #return {"movie title": movie_json}
    return render_template("upcoming.html",movie=jsondata1["results"])

if __name__=='__main__':
    app.run(debug=True)