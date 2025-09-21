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
            name VARCHAR(MAX), 
            userID INT, 
            creationDate DATETIME, 
            description TEXT,
            country TEXT, 
            state TEXT, 
            city TEXT, 
            FOREIGN KEY userID REFERENCES Users(userID)
            )              
        """)
        
        # Creates the GuildUserList
        self.run.execute(""" 
           CREATE TABLE IF NOT EXISTS GuildUserList (
            guildID INT, 
            userID INT, 
            role VARCHAR(100), 
            datejoined DATETIME, 
            FOREIGN KEY guildID REFERENCES Guild(guildID)
            )              
        """)

        # Creates the Post Table
        self.run.execute("""
           CREATE TABLE IF NOT EXISTS Posts (
            postID INT AUTO_INCREMENT PRIMARY KEY, 
            userID INT, 
            guildID INT DEFAULT -1, 
            text TEXT, 
            pictureID INT, 
            creationDate DATETIME, 
            likes INT,
            FOREIGN KEY (userID) REFERENCES Users(userID), 
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


    def register(username, password, joiningDate): 
        """"
        Function to make a new user. 
        """

        
    def login(username, password): 
        """
        Function that checks for a user's existance. 
        """


    def updateRole(username, role): 
        """
        Function to update the Role of a person.
        """


    def joinGuild(username, guildName):
        """
        Function to join a pre-existing guild.
        """


    def registerGuild(guildName, username, creationDate, description, country, state, city): 
        """
        Function to register a new guild. 
        """


    def getAllUsersInGuild(guildName): 
        """
        Returns all users under a guild. 
        """


    def getAllGuildsCountry(country): 
        """
        Returns all guilds under a country
        """
    

    def getAllGuildsState(state): 
        """
        Returns all guilds in a state. 
        """
    

    def getAllGuildsCity(city): 
        """
        Returns all guilds under a city: 
        """


    def newPost(username, guildName, text, creationDate, pictureID = -1): 
        """
        Creates a new post in the Posts table. 
        """


    def likePost(postID): 
        """
        Allows you to like a post. 
        """
    

    def getAllPostsUser(username): 
        """
        Returns all posts under a user. 
        """
    

    def getAllPostsGuild(guildName): 
        """
        Returns all posts under a guild. 
        """


    def newConversation(user1, user2): 
        """
        Creates a conversation between two people. 
        """


    def newMessage(conversationID, sender, receiver, date, message): 
        """
        Creates a new message within a conversation between two people. 
        """
    

    
