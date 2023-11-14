import sqlite3
from random import randint as rand


class DB:

	def __init__(self):
	    self.conn = sqlite3.connect('db\\sqlitebot.db')
	    self.cursor = self.conn.cursor()


	def add_user(self, userid):
	    self.cursor.execute("INSERT INTO 'users' ('userid') VALUES (?)", (userid,))
	    return self.conn.commit()


	def add_film(self, key, img_id, name, duration, score, genre,  year, country, desc):
		self.cursor.execute("INSERT INTO 'films' ('key', 'img_id', 'name', 'duration', 'score', 'genre', 'year', 'country', 'desc') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (key,  img_id, name, duration, score, genre,  year, country, desc,))
		print(f'[INF] New film #{key} has been succesfully added to database!')
		return self.conn.commit()

	def get_user(self, userid):
	    result = self.cursor.execute("SELECT * FROM 'users' WHERE userid=?", (userid,))
	    return result.fetchone()


	def get_film(self, key):
		film = self.cursor.execute("SELECT * FROM 'films' WHERE key=?", (key,))
		return film.fetchone()

	def get_randfilm(self):
		random_film = self.cursor.execute("SELECT * FROM 'films' ORDER BY RANDOM() LIMIT 1")
		return random_film.fetchone()

	def get_keysfilms(self):
		all_films = self.cursor.execute("SELECT * from 'films'")
		return all_films.fetchall()


	def close(self):
		self.conn.close()
