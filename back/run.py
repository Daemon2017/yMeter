from flask import Flask, request, Response
from flask_cors import CORS
from waitress import serve

import utils

TEXT_CSV = 'text/csv'

app = Flask(__name__)
cors = CORS(app)


@app.route('/measure', methods=['POST'])
def measure():
    df = utils.get_df(request.data)
    df = utils.get_solved_na_df(df, request.headers)
    df = utils.get_solved_duplications_df(df)
    df = df.dropna(axis=1, how='all')
    df.index.name = 'Kit'
    df = utils.get_solved_composites_df(df, request.headers)
    df = utils.get_solved_palindromes_df(df, request.headers)
    df = utils.get_solved_deletions_df(df)
    str_count = len(df.columns)
    df = utils.get_subtracted_df(df)
    df = utils.get_tmrca_df(df, str_count, request.headers)
    df = df.drop(df.index[0])
    df = df.sort_values(by=['Steps'])
    limit = int(request.headers['limit'])
    if limit != 0:
        df = df.iloc[:limit]
    return Response(df.to_csv(sep=',', index=True, header=True), mimetype=TEXT_CSV)


if __name__ == '__main__':
    print('yMeter ready!')
    serve(app,
          host='0.0.0.0',
          port=8080)
