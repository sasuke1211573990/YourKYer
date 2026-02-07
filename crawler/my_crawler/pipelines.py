import psycopg2
from .settings import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_SERVER, POSTGRES_PORT

class PostgresPipeline:
    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host=POSTGRES_SERVER,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            dbname=POSTGRES_DB,
            port=POSTGRES_PORT
        )
        self.cur = self.connection.cursor()
        
        # Create table if not exists (Though backend should handle this, good for safety)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS crawled_data (
            id SERIAL PRIMARY KEY,
            title TEXT,
            link TEXT UNIQUE,
            publish_date TIMESTAMP,
            content TEXT,
            source TEXT,
            category TEXT,
            university TEXT
        );
        """)
        self.connection.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute(
                """
                INSERT INTO crawled_data (title, link, publish_date, content, source, category, university)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (link) DO NOTHING
                """,
                (
                    item.get('title'),
                    item.get('link'),
                    item.get('publish_date'),
                    item.get('content'),
                    item.get('source'),
                    item.get('category'),
                    item.get('university')
                )
            )
            self.connection.commit()
        except Exception as e:
            spider.logger.error(f"Error saving item: {e}")
            self.connection.rollback()
        return item
