import sqlite3
import time

class database:

    def __init__(self):

        path = "./database.db"
        global conn
        conn = sqlite3.connect(path)

        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS channels (
                            guild_id integer NOT NULL,
                            channel_id integer NOT NULL,
                            user_id integer NOT NULL,
                            expiry integer NOT NULL
                        );""")
        conn.commit()

    def get(self, guild_id, user_id):
        c = conn.cursor()
        t = (guild_id, user_id)
        c.execute("SELECT channel_id FROM channels WHERE guild_id=? AND user_id=?;", t)
        channel = c.fetchone()
        if not channel:
            return None
        return channel[0]

    def get_all(self, guild_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("SELECT channel_id FROM channels WHERE guild_id=?;", t)
        channel_ids = []
        for channel_id in c.fetchall():
            channel_ids.append(channel_id[0])
        return channel_ids

    def add(self, guild_id, channel_id, user_id):
        c = conn.cursor()
        t = (guild_id, channel_id, user_id, time.time() + 60 * 60 * 24 * 30)
        c.execute("""INSERT INTO channels (
                            guild_id, channel_id, user_id, expiry
                        )
                        VALUES (
                            ?, ?, ?, ?
                        );""", t)
        conn.commit()

    def interact(self, channel_id):
        c = conn.cursor()
        t = (time.time() + 60 * 60 * 24 * 30, channel_id)
        c.execute(f"UPDATE channels SET expiry=? WHERE channel_id=?;", t)
        conn.commit()

    def remove(self, guild_id, user_id):
        c = conn.cursor()
        t = (guild_id, user_id)
        c.execute("DELETE FROM channels WHERE guild_id=? AND user_id=?;", t)
        conn.commit()