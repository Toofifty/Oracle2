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
        try:
            self.aliases = self.data['aliases']
        except:
            self.aliases = {}
            
    def add_alias(self, alias, command):
        self.aliases[alias] = command
        return True
        
    def get_alias(self, alias):
        return self.aliases.get(alias)
        
    def get_alias_list(self):
        return self.aliases
        
    def rem_alias(self, alias):
        try:
            del self.aliases[alias]
            return True
        except KeyError:
            return False
        
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
    
    def get_commands(self):
        return self.commands
    
    def get_name(self):
        return self.true_name
    
    def set_points(self, am):
        self.points = am
        return self.points
    
    def set_rank(self, rank):
        self.rank = rank
        return self.rank
        
    def set_nick(self, nick):
        self.last_nick = nick
    
    def increment_commands(self):
        self.commands += 1
        return self.commands
    
    def add_points(self, am):
        self.points += am
        return self.points
        
    def has_attribute(self, attr):
        if hasattr(self, attr):
            return True
        return False
            
    def add_attribute(self, attr, value):
        setattr(self, attr, value)
        self.data[attr] = value
        return True
            
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
        
    def update_seen(self):
        self.seen = time.asctime()
        return True
        
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
        
    
    
    