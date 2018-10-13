import os
import psycopg2
import model
from datetime import date
from flask import Flask, request, jsonify
from flask.json import JSONEncoder
from flask_cors import CORS

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
CORS(app)
app.json_encoder = CustomJSONEncoder

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
db = model.Database(cursor)

@app.route('/news', methods=['GET', 'POST'])
def news():
    if request.method == 'GET':
        amount = int(request.args.get('amount'))

        return jsonify(db.many_news(amount))
    elif request.method == 'POST':
        content = request.get_json()
        from pprint import pprint; pprint(content)
        db.add_news(
            content['title'],
            content['preview'],
            content['content'],
        )
        conn.commit()

        return 'Success!'

@app.route('/news/<int:id>')
def news_by_id(id):
    return jsonify(db.news(id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'])
