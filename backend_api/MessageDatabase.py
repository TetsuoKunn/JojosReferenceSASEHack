# import mysql.connector  # need to pip install mysql-connector-python for MySQL 
# import psycopg2         # need to pip install psycopg2-binary for PostgreSQL 
import sqlite3
import User.py

class DatabaseHelper:
    # Constructor for DatabaseHelper Object 
    def __init__(self):
        mydb = None
        run = None


    def connectToDataBase(self):
        """
        Method to connect to the database. Call this on a new Database Helper object to initialize the database. 
        """
        try: 
            self.mydb = sqlite3.connect("local_database.db")
            self.run = self.mydb.cursor() 
        except Exception as e: 
            print(f"Connection to the Database failed due to {e}")


    def createTables(self): 
        """
        Method to create / initialize all tables in the database. If they exist, then they're not touched. 
        """
        # Create Users Table 
        self.run.execute("""
            CREATE TABLE IF NOT EXISTS Users (
            userID INT AUTO_INCREMENT PRIMARY KEY, 
            username VARCHAR(15) UNIQUE, 
            password VARCHAR(100),
            joiningDate DATETIME
            )
        """)
        
        # Creates Guild table 
        self.run.execute("""
           CREATE TABLE IF NOT EXISTS Guild (
            guildID INT AUTO_INCREMENT PRIMARY KEY, 
            name TEXT, 
            username VARCHAR(15), 
            creationDate DATETIME, 
            description TEXT,
            country TEXT, 
            state TEXT, 
            city TEXT, 
            FOREIGN KEY username REFERENCES Users(username)
            )              
        """)
        
        # Creates the GuildUserList
        self.run.execute(""" 
           CREATE TABLE IF NOT EXISTS GuildUserList (
            name TEXT, 
            username VARCHAR(15), 
            role VARCHAR(100), 
            datejoined DATETIME, 
            FOREIGN KEY name REFERENCES Guild(name), 
            FOREIGN KEY username REFERENCES Users(username)
            )              
        """)

        # Creates the Post Table
        self.run.execute("""
           CREATE TABLE IF NOT EXISTS Posts (
            postID INT AUTO_INCREMENT PRIMARY KEY, 
            username VARCHAR(15), 
            guildID INT DEFAULT -1, 
            text TEXT, 
            pictureID INT, 
            creationDate DATETIME, 
            likes INT,
            FOREIGN KEY (username) REFERENCES Users(username), 
            FOREIGN KEY (guildID) REFERENCES Guild(guildID), 
            FOREIGN KEY (pictureID) REFERENCES Pictures(pictureID), 
            )             
        """)

        # Creates the Comments Table
        self.run.execute("""
           CREATE TABLE IF NOT EXISTS Comments (
            commentID INT AUTO_INCREMENT PRIMARY KEY, 
            text TEXT, 
            postID INT, 
            creationDate DATETIME, 
            FOREIGN KEY (userID) REFERENCES Posts(postID), 
            )             
        """)

        # Creates the Pictures table
        self.run.execute(""" 
            CREATE TABLE IF NOT EXISTS ProgressImages (
            pictureID INT PRIMARY KEY AUTO_INCREMENT
            )
        """)

        # Create Conversations Table
        self.run.execute("""
            CREATE TABLE IF NOT EXISTS Conversations (
            conversationID INT AUTO_INCREMENT PRIMARY KEY, 
            user1 VARCHAR(15), 
            user2 VARCHAR(15), 
            UNIQUE(user1, user2), 
            FOREIGN KEY (user1) REFERENCES Users(userId), 
            FOREIGN KEY (user2) REFERENCES Users(userId)
            )
        """)
        
        # Create Messages Table 
        self.run.execute("""
            CREATE TABLE IF NOT EXISTS Messages (
            messageID INT AUTO_INCREMENT PRIMARY KEY, 
            message TEXT, 
            time INT, 
            sender VARCHAR(15), 
            conversationID INT,  
            FOREIGN KEY (conversationId) REFERENCES Conversations(ConversationId),
            FOREIGN KEY (sender) REFERENCES Users(userId)           
            )
        """)

    
    def register(self, username, password, joiningDate): 
        """"
        Function to make a new user. 
        """
        self.run.execute(f"INSERT INTO Users (username, password, joiningDate) VALUES ({username}, {password}), {joiningDate}")
        self.mydb.commit()
        

    def login(self, username, password): 
        """
        Function that checks for a user's existance. 
        """
        self.run.execute("SELECT 1 FROM Users WHERE username = ? AND password = ? LIMIT 1", (username, password))
        exists = self.run.fetchone() is not None
 
        return exists   # True if login is successful, False otherwise. 
    
    
    def updateRole(self, username, guildName, role): 
        """
        Function to update the Role of a person.
        """
        self.run.execute(f"UPDATE GuildUserList SET role = ? WHERE username = ? AND guildName = ?", (role, username, guildName))
        self.mydb.commit()


    def joinGuild(self, username, guildName, joiningDate):
        """
        Function to join a pre-existing guild.
        """
        self.run.execute("INSERT INTO GuildUserList (name, username, role, datejoined) VALUES (?, ?,'Novice', ?)", (guildName, username, joiningDate))
        self.mydb.commit()


    def registerGuild(self, guildName, username, creationDate, description, country, state, city): 
        """
        Function to register a new guild. 
        """
        self.run.execute("INSERT INTO Guild (guildName, username, creationDate, description, country, state, city) VALUES (?, ?, ?, ?, ?, ?, ?)", (guildName, username, creationDate, description, country, state, city))
        self.mydb.commit()
        self.updateRole(username, guildName, "Owner")


    def getAllUsersInGuild(self, guildName): 
        """
        Returns all users under a guild as tuples
        """
        self.run.execute(
            """
            SELECT username, role, datejoined
            FROM GuildUserList
            WHERE guildName = ?
            """, (guildName))
        users = self.run.fetchall()

        return users


    def getAllGuildsCountry(self, country): 
        """
        Returns all guilds under a country as tuples
        """
        self.run.execute(
            """
            SELECT name, description 
            FROM Guild
            WHERE country = ? 
            """, (country)
        )
        guilds = self.run.fetchall()

        return guilds


    def getAllGuildsState(self, state): 
        """
        Returns all guilds in a state as tuples
        """
        self.run.execute(
            """
            SELECT name, description 
            FROM Guild
            WHERE state = ? 
            """, (state)
        )
        guilds = self.run.fetchall()

        return guilds


    def getAllGuildsCity(self, city): 
        """
        Returns all guilds under a city as tuples
        """
        self.run.execute(
            """
            SELECT name, description 
            FROM Guild
            WHERE city = ? 
            """, (city)
        )
        guilds = self.run.fetchall()

        return guilds


    def newPost(self, username, guildName, text, creationDate, pictureID = -1): 
        """
        Creates a new post in the Posts table. 
        """
        self.run.execute("""
            INSERT INTO Posts (username, )
        """)


    def likePost(self, postID): 
        """
        Allows you to like a post. 
        """
    

    def getAllPostsUser(self, username): 
        """
        Returns all posts under a user. 
        """
    

    def getAllPostsGuild(self, guildName): 
        """
        Returns all posts under a guild. 
        """


    def newConversation(self, user1, user2): 
        """
        Creates a conversation between two people. 
        """


    def newMessage(self, conversationID, sender, receiver, date, message): 
        """
        Creates a new message within a conversation between two people. 
        """
        
    

    
