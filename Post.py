import json
from datetime import datetime



class Post:
    def __init__(self, user_id, text, guild_id=-1, picture_id=None):
        # Generate post_id based on creation timestamp
        self.creation_date = datetime.now()
        self.post_id = self.creation_date.strftime("%Y%m%d%H%M%S%f")

        self.user_id = user_id
        self.text = text
        self.guild_id = guild_id
        self.picture_id = picture_id



    # ----
    # Getters
    # ----
    def get_post_id(self):
        return self.post_id


    def get_user_id(self):
        return self.user_id


    def get_guild_id(self):
        return self.guild_id


    def get_text(self):
        return self.text


    def get_picture_id(self):
        return self.picture_id


    def get_creation_date(self):
        return self.creation_date



    # ----
    # Setters
    # ----
    def set_user_id(self, user_id):
        self.user_id = user_id


    def set_guild_id(self, guild_id):
        self.guild_id = guild_id


    def set_text(self, text):
        self.text = text


    def set_picture_id(self, picture_id):
        self.picture_id = picture_id



    # ----
    # Delete
    # ----
    def delete_user_id(self):
        self.user_id = None


    def delete_guild_id(self):
        self.guild_id = -1


    def delete_text(self):
        self.text = None


    def delete_picture_id(self):
        self.picture_id = None



    # ----
    # JSON
    # ----
    def to_dict(self):
        """Return Python dict"""

        return {
            "post_id": self.post_id,
            "user_id": self.user_id,
            "guild_id": self.guild_id,
            "text": self.text,
            "picture_id": self.picture_id,
            "creation_date": self.creation_date.isoformat()
        }


    def to_json(self):
        """Return JSON string"""

        return json.dumps(self.to_dict())

