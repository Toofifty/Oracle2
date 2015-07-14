#!/user/bin/env python
"""
Oracle 2.0 IRC Bot
db.py

http://oracle.toofifty.me/
"""

import user
import sqlite3, time

CON = sqlite3.connect('../data/data.db')
CON.row_factory = sqlite3.Row
CUR = CON.cursor()

def init():
    with CON:
        CUR.execute(
            'CREATE TABLE users(nick TEXT, last_nick TEXT, seen INT, rank INT, \
            points INT, commands INT)'
        )

        CUR.execute(
            'CREATE TABLE aliases(user TEXT, alias TEXT, command TEXT)'
        )

        CUR.execute(
            'CREATE TABLE alerts(title TEXT, description TEXT, user TEXT, \
            time INT, level INT)'
        )

        CUR.execute(
            'CREATE TABLE twitters(account TEXT, name TEXT)'
        )

def get_twitters():
    with CON:
        CUR.execute(
            'SELECT * FROM twitters'
        )

        return CUR.fetchall()

def save_user(user):
    with CON:
        if load_user(user.name) is None:
            CUR.execute(
                'INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)',
                (user.name, user.last_nick, user.seen, user.rank, user.points,
                user.commands)
            )
            print 'created new record for ' + user.name
            return True

        CUR.execute(
            'UPDATE users SET last_nick=?, seen=?, rank=?, points=?, commands=?\
             WHERE nick=?',
            (user.last_nick, user.seen, user.rank, user.points, user.commands,
            user.nick)
        )

def load_user(name):
    with CON:
        CUR.execute('SELECT * FROM users WHERE nick=? COLLATE NOCASE', (name,))

        ud = CUR.fetchone()

        if ud is None:
            return None

        return user.User(
            ud['nick'], ud['last_nick'], ud['rank'], ud['points'],
            ud['commands'], ud['seen']
        )

def top_scores(n):
    with CON:
        CUR.execute(
            'SELECT * FROM users ORDER BY points DESC'
        )

        top = []

        for ud in CUR.fetchall()[:n]:
            top.append(user.User(
                ud['nick'], ud['last_nick'], ud['rank'], ud['points'],
                ud['commands'], ud['seen']
            ))
        return top

if __name__ == '__main__':
    init()
