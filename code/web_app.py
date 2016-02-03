from collections import namedtuple

import numpy as np
import pandas as pd
import graphlab as gl
from flask import Flask, abort, jsonify, render_template, request

Suggestion = namedtuple('Suggestion', ['brewery', 'name', 'id'])


app = Flask(__name__)

'''
todo
- add autocomplete to find beers you want
- replace weird characters in beer names
- look into sudo command to get gl running
- clean up ui
'''

@app.route("/")
def main():
    return render_template('index.html')


@app.route("/recommend", methods=['POST'])
def recommend():
    user_input = str(request.form['beer_input']).split(',')
    user_input = [int(fig) for fig in user_input]
    user_input = pd.DataFrame({'a': [20000 for _ in user_input], 'b': user_input})
    user_input.columns = ['user_id', 'item_id']
    user_input = gl.SFrame(user_input)
    model = gl.load_model('../models/item_similarity_model')
    pred = list(model.recommend(users=[20000], new_observation_data=user_input, diversity=3)['item_id'])

    beers = pd.read_csv('../data/raw_data/beers.csv')
    beer_recs = beers[beers['ID']
                .isin(pred)] \
                .to_html(columns=['Name', 'Style', 'Brewery Name'],index=False) \
                .replace('border="1" class="dataframe"','class=table table-hover')

    return render_template('index.html', recommend=True, beer_recs=beer_recs)


@app.route("/suggest")
def suggest():
        user_input = request.args.get("input")
        if not user_input:
            return abort(400)

        suggestions = [
            Suggestion("Russian River Brewing", "Pliny the Elder", 12345),
            Suggestion("Russian River Brewing", "Pliny the Younger", 54321),
            Suggestion("Ballast Point Brewing", "Sculpin", 3333),
        ]

        suggestions_dict = [suggestion._asdict() for suggestion in suggestions]

        return jsonify(
            suggestions=suggestions_dict,
        )


if __name__ == "__main__":
    ### load app here
    app.run(host='0.0.0.0', port=8080, debug=True)
