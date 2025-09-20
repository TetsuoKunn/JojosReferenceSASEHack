
class User: 
    def __init__(self, username, password, role = "Normal"):
        self.username = username
        self.password = password
        self.role = role


    def getUsername(self):
        return self.username
    

    def getPassword(self):
        return self.password
    

    def getRole(self):
        return self.role
    

    def setUsername(self, username):
        self.username = username


    def setPassword(self, password):
        self.password = password


    def setRole(self, role):
        self.role = role