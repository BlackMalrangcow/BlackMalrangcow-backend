class Database:
    def __init__(self, cursor):
        self.cursor = cursor

    def many_news(self, amount, random):
        if random:
            self.cursor.execute("SELECT * FROM news ORDER BY random() LIMIT %s", (amount,))
        else:
            self.cursor.execute("SELECT * FROM news LIMIT %s", (amount,))

        return [{
            "id": news[0],
            "title": news[1],
            "preview": news[2],
        } for news in self.cursor.fetchall()]

    def news(self, id):
        self.cursor.execute("SELF * FROM news WHERE id = %s", (id,))

        _, title, _, content, _ = self.cursor.fetchone()

        return {
            "title": title,
            "content": content,
        }

    def add_news(self, title, preview, content):
        self.cursor.execute("""
        INSERT INTO news (title, preview, content, category)
        VALUES (%s, %s, %s, %s)""", (title, preview, content, 5))
