# import mysql.connector  # need to pip install mysql-connector-python for MySQL
# import psycopg2         # need to pip install psycopg2-binary for PostgreSQL
import sqlite3

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
            self.mydb = sqlite3.connect("local_database.db", check_same_thread=False)
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
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            firstname TEXT,
            lastname TEXT,
            password TEXT,
            joiningDate DATETIME
            )
        """)

        # Creates Guild table
        self.run.execute("""
           CREATE TABLE IF NOT EXISTS Guild (
            guildID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            username TEXT,
            creationDate DATETIME,
            description TEXT,
            country TEXT,
            state TEXT,
            city TEXT,
            FOREIGN KEY (username) REFERENCES Users(username)
            )
        """)

        # Creates the GuildUserList
        self.run.execute("""
           CREATE TABLE IF NOT EXISTS GuildUserList (
            name TEXT,
            username TEXT,
            role TEXT,
            datejoined DATETIME,
            FOREIGN KEY (name) REFERENCES Guild(name),
            FOREIGN KEY (username) REFERENCES Users(username)
            )
        """)

        # Creates the Post Table
        self.run.execute("""
           CREATE TABLE IF NOT EXISTS Posts (
            postID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            name TEXT,
            text TEXT,
            pictureID INT,
            creationDate DATETIME,
            likes INT,
            FOREIGN KEY (username) REFERENCES Users(username),
            FOREIGN KEY (name) REFERENCES Guild(name),
            FOREIGN KEY (pictureID) REFERENCES Pictures(pictureID)
            )
        """)

        # Creates the Comments Table
        self.run.execute("""
           CREATE TABLE IF NOT EXISTS Comments (
            commentID INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            postID INT,
            creationDate DATETIME,
            FOREIGN KEY (postID) REFERENCES Posts(postID)
            )
        """)

        # Creates the Pictures table
        self.run.execute("""
            CREATE TABLE IF NOT EXISTS Pictures(
            pictureID INTEGER PRIMARY KEY AUTOINCREMENT
            )
        """)

        # Create Conversations Table
        self.run.execute("""
            CREATE TABLE IF NOT EXISTS Conversations (
            conversationID INTEGER PRIMARY KEY AUTOINCREMENT,
            user1 TEXT,
            user2 TEXT,
            UNIQUE(user1, user2),
            FOREIGN KEY (user1) REFERENCES Users(username),
            FOREIGN KEY (user2) REFERENCES Users(username)
            )
        """)

        # Create Messages Table
        self.run.execute("""
            CREATE TABLE IF NOT EXISTS Messages (
            messageID INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            time DATETIME,
            sender TEXT,
            conversationID INT,
            FOREIGN KEY (conversationId) REFERENCES Conversations(ConversationId),
            FOREIGN KEY (sender) REFERENCES Users(username)
            )
        """)


    def register(self, username, firstname, lastname, password, joiningDate):
        """"
        Function to make a new user.
        """
        self.run.execute(f"INSERT INTO Users (username, firstname, lastname, password, joiningDate) VALUES (?, ?, ?, ?, ?)", (username, firstname, lastname, password, joiningDate))
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
        self.run.execute(f"UPDATE GuildUserList SET role = ? WHERE username = ? AND name = ?", (role, username, guildName))
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
        self.run.execute("INSERT INTO Guild (name, username, creationDate, description, country, state, city) VALUES (?, ?, ?, ?, ?, ?, ?)", (guildName, username, creationDate, description, country, state, city))
        self.mydb.commit()
        self.updateRole(username, guildName, "Owner")
        self.makeGuildConnection(guildName, username,"Owner", creationDate)


    def makeGuildConnection(self, guildName, username, role, datetime):
        """
        Function to update a connection between users and guild.
        """
        self.run.execute("" \
        "INSERT INTO GuildUserList (name, username, role, datejoined) " \
        "VALUES (?, ?, ?, ? )", (guildName, username, role, datetime))
        self.mydb.commit()


    def getAllUsersInGuild(self, guildName):
        """
        Returns all users under a guild as tuples
        """
        self.run.execute(
            """
            SELECT gul.username, u.firstname, u.lastname, gul.role, gul.datejoined
            FROM GuildUserList gul
            INNER JOIN Users u ON gul.username = u.username
            WHERE gul.name = ?
            """, (guildName,))
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
            """, (country,)
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
            """, (state,)
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
            """, (city,)
        )
        guilds = self.run.fetchall()

        return guilds


    def newPost(self, username, guildName, text, creationDate, pictureID = -1):
        """
        Creates a new post in the Posts table.
        """
        self.run.execute("""
            INSERT INTO Posts (username, name, text, creationDate, pictureID)
            VALUES (?, ?, ?, ?, ?)
        """, (username, guildName, text, creationDate, pictureID))
        self.mydb.commit()


    def likePost(self, postID):
        """
        Allows you to like a post.
        """
        self.run.execute(f"UPDATE Posts SET likes = likes + 1 WHERE postID = ?", (postID, ))
        self.mydb.commit()


    def newComment(self, username, text, postID, creationDate):
        """
        Allows you to make new comments on a post.
        """
        self.run.execute("""
            INSERT INTO Comments (username, text, postID, creationDate)
            VALUES (?, ?, ?, ?)
        """, (username, text, postID, creationDate))
        self.mydb.commit()


    def getAllComments(self, postID):
        """
        Shows all comments under a post.
        """
        self.run.execute("""
           SELECT username, text, creationDate
            FROM Comments
            WHERE postID = ?
        """, (postID,))

        comments = self.run.fetchall()

        return comments


    def getAllPostsUser(self, username):
        """
        Returns all posts under a user.
        """
        self.run.execute(f"""
            SELECT postID, username, text, pictureID, creationDate, likes
            FROM Posts
            WHERE username = ?
        """, (username,))
        posts = self.run.fetchall()

        return posts


    def getAllPostsGuild(self, guildName):
        """
        Returns all posts under a guild.
        """
        self.run.execute(f"""
            SELECT postID, name, text, pictureID, creationDate, likes
            FROM Posts
            WHERE name = ?
        """, (guildName,))
        posts = self.run.fetchall()

        return posts


    def newConversation(self, user1, user2):
        """
        Creates a conversation between two people.
        """
        try:
            self.run.execute(f"""
                INSERT INTO Conversations (user1, user2)
                VALUES (?, ?)
                """, (user1, user2))

            self.mydb.commit()
        except sqlite3.IntegrityError:
            print("uh oh spaghetti o this already exists")


    def newMessage(self, conversationID, sender, date, message):
        """
        Creates a new message within a conversation between two people.
        """
        self.run.execute("""
            INSERT INTO Messages (conversationID, sender, time, message)
            VALUES (?, ?, ?, ?)
        """, (conversationID, sender, date, message))

        self.mydb.commit()

    def getGuildsfromUser(self, user):
        """
        gets all the guilds a user has joined
        """
        self.run.execute("""
            SELECT name
            FROM GuildUserList
            WHERE username = ?
        """, (user,))
        guilds = self.run.fetchall()

        return guilds


    def getConversations(self, user1):
        """
        Shows all conversations of a person
        """
        self.run.execute("""
            SELECT conversationID,
            CASE
            WHEN user1 = ? THEN user2
            ELSE user1
            END AS other_user
            FROM Conversations
            WHERE user1 = ? OR user2 = ?
        """, (user1, user1, user1))

        return self.run.fetchall()


    def getMessages(self, user1, user2):
        """
        Shows all messages between two people.
        """
        self.run.execute("""
            SELECT conversationID
            FROM Conversations
            WHERE (user1 = ? AND user2 = ?) OR (user1 = ? AND user2 = ?)
        """, (user1, user2, user2, user1))

        result = self.run.fetchone()
        if not result:
            return []
        conversation_id = result[0]

        self.run.execute("""
            SELECT messageID, sender, message, time
            FROM Messages
            WHERE conversationID = ?
            ORDER BY time ASC
        """, (conversation_id,))

        return self.run.fetchall()
