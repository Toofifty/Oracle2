import json, os, time, traceback

class User:
    def __init__(self, name):
        print 'Creating user object for %s...' % name
        self.true_name = name
        self.nick = name
        self.path = os.path.join('..', 'files', 'users', '%s.json' % name)
        if not os.path.exists(self.path):
            self.create_file()
        with open(self.path) as f:
            self.data = json.load(f)
        self.get_json_data()
            
    def get_json_data(self):
        self.seen = self.data['seen']
        self.last_nick = self.data['last_nick']
        self.rank = self.data['rank']
        self.points = self.data['points']
        self.commands = self.data['commands']
        
    def get_rank(self):
        return self.rank
    
    def get_seen(self):
        return self.seen
    
    def get_last_nick(self):
        return self.last_nick
    
    def get_path(self):
        return self.path
    
    def get_points(self):
        return self.points
    
    def set_points(self, am):
        self.points = am
        return self.points
    
    def set_rank(self, rank):
        self.rank = rank
        
    def set_nick(self, nick):
        self.last_nick = nick
    
    def increment_commands(self):
        self.commands += 1
        return self.commands
    
    def add_points(self, am):
        self.points += am
        return self.points
            
    def create_file(self):
        print 'Creating user file for %s...' % self.true_name
        with open(self.path, 'w') as f:
            f.write('{"seen": 0, "last_nick": "%s", "rank": "user", "points": 0, '
                    '"commands": 0}' % self.nick)
            
    def get_user_data(self):
        udata = {}
        for key in self.data:
            udata[key] = getattr(self, key)
            print key, udata[key]
        return udata
        
    def part(self):
        try:
            self.seen = time.asctime()
            with open(self.path, 'w') as o:
                json.dump(self.get_user_data(), o)
            return True
        except Exception, e:
            traceback.print_exc()
        
    def join(self):
        pass
        
    
    
    