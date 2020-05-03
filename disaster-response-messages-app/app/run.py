from flask import Flask
from flask import render_template, request, jsonify
from sqlalchemy import create_engine

import json
import plotly
import pandas as pd

from plotly.graph_objs import Bar
from sklearn.externals import joblib

# Pickled model requires custom tokenizer
from tokenizer import tokenizer


app = Flask(__name__)

engine = create_engine('sqlite:///../data/disaster_project.db')
df = pd.read_sql_table('messages_categories', engine)
clf_label_names = df.columns[4:]
model = joblib.load("../models/model.pkl")

@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    class_imb = df[df.columns[4:]].sum()/df.shape[0]
    categories = class_imb.index
    class_imb_counts = class_imb.round(2).values
    
    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of message source',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Source"
                }
            }
        },
        {
            'data': [
                Bar(
                    x=categories,
                    y=class_imb_counts
                )
            ],

            'layout': {
                'title': 'Class imbalance of dataset',
                'yaxis': {
                    'title': "% messages"
                },
                'xaxis': {
                    'title': "Category"
                }
            }
        }
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    print(classification_labels)

    # Render the go.html. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()