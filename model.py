class Database:
    def __init__(self, cursor):
        self.cursor = cursor

    def many_news(self, amount, category):
        self.cursor.execute("SELECT * FROM news WHERE category = %s ORDER BY random() LIMIT %s", (category, amount))

        return [{
            "title": news[0],
            "preview": news[1],
        } for news in self.cursor.fetchall()]

    def news(self, category, title):
        self.cursor.execute("SELECT * FROM news WHERE category = %s AND title = %s", (category, title))

        content = self.cursor.fetchone()[2]

        return {
            "content": content,
        }

    def add_news(self, title, preview, category, content):
        self.cursor.execute("""
        INSERT INTO news (title, preview, content, category)
        VALUES (%s, %s, %s, %s)""", (title, preview, content, category))
