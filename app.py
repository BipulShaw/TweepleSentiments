from crypt import methods
from flask import Flask, url_for, render_template, request
import pickle
import tp

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/search", methods=['POST', 'GET'])
def search():
    # render_template('index.html', search_keyword = "_empty_")
    search_term = request.form["item"]
    scores = tp.mainfunction(search_term)
    return render_template('index.html',search_keyword = search_term, n_o_t = scores[0], n_p = scores[1], p_p = scores[2], p = scores[3], s = scores[4])


if __name__ == "__main__":
    app.run(debug=True)