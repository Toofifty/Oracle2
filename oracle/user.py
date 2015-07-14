import db
import json, os, time, traceback

def get_user(name):
    user = db.load_user(name)
    if user is None:
        print 'creating new user: ' + name
        return User(name, name, 1, 0, 0)
    return user

class User:
    def __init__(self, nick, last_nick, rank, points, commands, seen=0):
        self.name = nick
        self.nick = nick
        self.last_nick = last_nick
        self.rank = rank
        self.points = points
        self.commands = commands
        self.seen = seen
        if self.seen == 0:
            self.update_seen()

    def update(self):
        self.update_seen()
        db.save_user(self)

    def get_rank(self):
        return self.rank

    def get_seen(self):
        return [time.asctime(time.gmtime(self.seen)), time.time() - self.seen]

    def get_last_nick(self):
        return self.last_nick

    def get_path(self):
        return self.path

    def get_points(self):
        return self.points

    def get_commands(self):
        return self.commands

    def get_name(self):
        return self.name

    def set_points(self, am):
        self.points = int(am)
        db.save_user(self)
        return self.points

    def set_rank(self, rank):
        self.rank = rank
        db.save_user(self)
        return self.rank

    def set_nick(self, nick):
        self.last_nick = nick
        db.save_user(self)

    def increment_commands(self):
        self.commands += 1
        db.save_user(self)
        return self.commands

    def add_points(self, am):
        self.points += int(am)
        if not isinstance(self.points, int):
            self.points = int(self.points)
        db.save_user(self)
        return self.points

    def update_seen(self):
        self.seen = time.time()
        return True

    def part(self):
        try:
            self.seen = time.time()
            db.save_user(self)
            return True
        except Exception, e:
            traceback.print_exc()

    def join(self):
        # may want to do something on user join.
        pass
