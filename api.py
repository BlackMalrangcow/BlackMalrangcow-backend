import os
import re
import psycopg2
import model
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
db = model.Database(cursor)

@app.route('/news', methods=['GET', 'POST'])
def news():
    if request.method == 'GET':
        amount = int(request.args.get('amount'))
        category = int(request.args.get('category'))

        return jsonify(db.many_news(amount, category))
    elif request.method == 'POST':
        content = request.get_json(cache=False)
        db.add_news(
            content['title'],
            get_image(content['content']),
            content['category'],
            content['content'],
        )
        conn.commit()

        return 'Success!'

@app.route('/news/<int:category>/<string:title>')
def news_by_id(category, title):
    return jsonify(db.news(category, title))

def get_image(content):
    s = re.findall(r"!\[.*\]\(.*\)", content)[0]
    return s[s.find("(")+1:s.find(")")]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'])
