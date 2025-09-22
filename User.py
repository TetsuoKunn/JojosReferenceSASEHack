from Role import Role
from Post import Post

class User: 
    def __init__(self, user_id, username, password, roles=None):
        self.user_id = user_id
        self.username = username
        self.password = password

        if roles is None:
            self.roles = ["Normal"]
        else:
            self.roles = roles

        self.posts = []


    def getUserID(self):
        return self.user_id


    def getUsername(self):
        return self.username
    

    def getPassword(self):
        return self.password
    

    def getRoles(self):
        return self.roles
    
    def getPosts(self):
        return self.posts
    

    def setUsername(self, username):
        self.username = username


    def setPassword(self, password):
        self.password = password


    def setRoles(self, roles):
        self.roles = roles


    def setPosts(self, posts):
        self.posts = posts