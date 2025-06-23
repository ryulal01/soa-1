from clickhouse_driver import Client
from datetime import datetime
import os
import time

class Storage:
    def __init__(self):
        for attempt in range(10):
            try:
                self.client = Client(
                    host=os.getenv('CLICKHOUSE_HOST', 'clickhouse'),
                    port=int(os.getenv('CLICKHOUSE_PORT', 9000)),
                    user=os.getenv('CLICKHOUSE_USER', 'default'),
                    password=os.getenv('CLICKHOUSE_PASSWORD', 'default_password')
                )
                self.create_table()
                print("[Storage] Successfully connected to ClickHouse.")
                break
            except Exception as e:
                print(f"[Storage] Attempt {attempt + 1}: Failed to connect to ClickHouse: {e}")
                time.sleep(3)
        else:
            raise RuntimeError("Failed to connect to ClickHouse after 10 attempts.")

    def create_table(self):
        self.client.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_date Date,
                event_time DateTime,
                event_type String,
                post_id String,
                user_id String
            ) ENGINE = MergeTree()
            PARTITION BY toYYYYMM(event_date)
            ORDER BY (event_date, post_id, user_id)
        """)

    def insert_event(self, event_type, post_id, user_id, event_time=None):
        if event_time is None:
            event_time = datetime.utcnow()
        self.client.execute(
            """
            INSERT INTO events (event_date, event_time, event_type, post_id, user_id) VALUES
            """,
            [(event_time.date(), event_time, event_type, post_id, user_id)]
        )

    def get_post_stats(self, post_id):
        query = """
            SELECT
                sum(event_type = 'view') AS views,
                sum(event_type = 'like') AS likes,
                sum(event_type = 'comment') AS comments
            FROM events
            WHERE post_id = %(post_id)s
        """
        result = self.client.execute(query, {'post_id': post_id})[0]
        return result

    def get_dynamics(self, post_id, event_type):
        query = """
            SELECT event_date, count() AS cnt
            FROM events
            WHERE post_id = %(post_id)s AND event_type = %(event_type)s
            GROUP BY event_date
            ORDER BY event_date
        """
        rows = self.client.execute(query, {'post_id': post_id, 'event_type': event_type})
        return rows

    def get_top_posts(self, event_type):
        query = """
            SELECT post_id, count() AS cnt
            FROM events
            WHERE event_type = %(event_type)s
            GROUP BY post_id
            ORDER BY cnt DESC
            LIMIT 10
        """
        rows = self.client.execute(query, {'event_type': event_type})
        return rows

    def get_top_users(self, event_type):
        query = """
            SELECT user_id, count() AS cnt
            FROM events
            WHERE event_type = %(event_type)s
            GROUP BY user_id
            ORDER BY cnt DESC
            LIMIT 10
        """
        rows = self.client.execute(query, {'event_type': event_type})
        return rows

