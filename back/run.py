from flask import Flask, request, Response
from flask_cors import CORS
from waitress import serve

import utils

TEXT_CSV = 'text/csv'

app = Flask(__name__)
cors = CORS(app)


@app.route('/measure', methods=['POST'])
def measure():
    df = utils.get_prepared_df(request)
    df = utils.get_extended_df(df)
    df = df.sort_values(by=['Steps'])
    return Response(df.to_csv(sep=',', index=True, header=True), mimetype=TEXT_CSV)


if __name__ == '__main__':
    print('yMeter ready!')
    serve(app,
          host='0.0.0.0',
          port=8080)
