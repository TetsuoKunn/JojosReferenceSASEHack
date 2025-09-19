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
            role VARCHAR(MAX)
            )
        """)
        
        self.run.execute("""
           CREATE TABLE IF NOT EXISTS RoommateProfile (
            profileID AUTO_INCREMENT PRIMARY KEY, 
            userID INT, 
            lifestyle VARCHAR(MAX), 
            wants VARCHAR(MAX), 
            FOREIGN KEY userID REFERENCES Users(userID)    
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
            message VARCHAR(MAX), 
            time INT, 
            sender VARCHAR(15), 
            conversationID INT,  
            FOREIGN KEY (conversationId) REFERENCES Conversations(ConversationId),
            FOREIGN KEY (sender) REFERENCES Users(userId)           
            )
        """)
        
        # Creates Pages Table
        self.run.execute("""
            CREATE TABLE IF NOT EXISTS Pages (
            pageID INT AUTO_INCREMENT PRIMARY KEY, 
            userId VARCHAR(MAX), 
            FOREIGN KEY (userId) REFERENCES Users(userId),     
            )
        """)
        
        # Creates Hobbies Table
        self.run.execute("""
            CREATE TABLE IF NOT EXISTS Hobbies (
            title VARCHAR(MAX),
            hobbyID INT AUTO_INCREMENT, 
            pageID INT,   
            FOREIGN KEY (pageID) REFERENCES Pages(pageID)        
            )
        """)
        
        # Creates the Progress Table 
        self.run.execute("""
            CREATE TABLE IF NOT EXISTS Progress (
            progressID INT AUTO_INCREMENT PRIMARY KEY, 
            hobbyID INT, 
            pageID INT, 
            description VARCHAR(MAX), 
            time DATETIME DEFAULT CURRENT_TIMESTAMP, 
            FOREIGN KEY (hobbyID) REFERENCES Hobbies(hobbyID), 
            FOREIGN KEY (pageID) REFERENCES Pages(pageID)
            )     
        """)

        # Creates the Progress Images Table
        self.run.execute(""" 
            CREATE TABLE IF NOT EXISTS ProgressImages (
            imageID INT PRIMARY KEY AUTO_INCREMENT, 
            imageName VARCHAR(MAX)
            path VARCHAR(MAX) 
            progressID INT,
            FOREIGN KEY (progressID) REFERENCES Progress(progressID)
            )
        """)
    

    def register (User user): 
        pass

    def login (User user): 
        pass


    def showPage(String username):
        pass

