from typing import Any
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import (cursor as Cursor, connection as Connection, ISOLATION_LEVEL_AUTOCOMMIT)

from config import (USER, PASSWORD, HOST, PORT)


class Connecting():
    def __init__(self) -> None:
        try:
            self.connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT
            )
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print('Connection successful')
            cur = self.connection.cursor()
            cur.execute('CREATE DATABASE homework5;')
            print('Database was created!')
        except (Exception, Error) as e:
            print('ERROR {}'.format(e))

    def __new__(cls: type[Any]) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connecting, cls).__new__(cls)
        
        return cls.instance


    def connect_db(self):
        try:
            self.connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                database='homework5'
            )
        except (Exception, Error) as e:
            print('ERROR {}'.format(e))
            
    def create_table(self):
        with self.connection.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL, 
                    name VARCHAR(20) PRIMARY KEY, 
                    login VARCHAR(20) UNIQUE, 
                    password VARCHAR(20));
                
                CREATE TABLE IF NOT EXISTS articles(
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(50) NOT NULL,
                    article text NOT NULL,
                    name VARCHAR(20) REFERENCES users(name));
            """)
        self.connection.commit()
        print('Table is successful created!')

    def reg_user(self, name: str, login: str, password: str):
        with self.connection.cursor() as cur:
            cur.execute(f"""
                INSERT INTO users (name, login, password)
                VALUES ('{name}', '{login}', '{password}');
            """)
        self.connection.commit()
        print('User successful created!')

    def get_all_users(self):
        data: list[tuple] = []
        with self.connection.cursor() as cur:
            cur.execute("""
                SELECT * FROM users;
            """)
            data = cur.fetchall()

        self.connection.commit()
        return data

    def check_users(self, login: str):
        data: list[tuple] = []
        with self.connection.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM users WHERE login='{login}';
            """)
            data = cur.fetchall()

        return data == []

    def check_auth(self, login, password):
        data: list[tuple] = []
        with self.connection.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM users WHERE login='{login}' and password='{password}';
            """)
            data = cur.fetchall()

        return data != []

    def create_article(self, title, article, name):
        with self.connection.cursor() as cur:
            cur.execute(f"""
                INSERT INTO articles (title, article, name)
                VALUES ('{title}', '{article}', '{name}');
            """)
        self.connection.commit()
        print('Article successfuly created!')

    def get_articles(self):
        data: list[tuple] = []
        with self.connection.cursor() as cur:
            cur.execute("SELECT * FROM articles;")
            data = cur.fetchall()

        self.connection.commit()
        return data

    def get_current_user(self, login, password):
        data: list[tuple] = []
        with self.connection.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM users WHERE login='{login}' and password='{password}';
            """)
            data = cur.fetchall()

        return data