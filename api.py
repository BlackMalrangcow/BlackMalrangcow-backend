import os
import psycopg2
import model
from datetime import date
from flask import Flask, request, jsonify
from flask.json import JSONEncoder

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
app.json_encoder = CustomJSONEncoder

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
db = model.Database(cursor)

@app.route('/news', methods=['GET', 'POST'])
def news():
    if request.method == 'GET':
        random = True if request.args.get('random') == 't' else False
        amount = int(request.args.get('amount'))

        return jsonify(db.many_news(amount, random))
    elif request.method == 'POST':
        db.add_news(
            request.form['title'],
            request.form['preview'],
            request.form['content'],
        )
        conn.commit()

        return 'Success!'

@app.route('/news/<int:id>')
def news_by_id(id):
    return jsonify(db.news(id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'])
