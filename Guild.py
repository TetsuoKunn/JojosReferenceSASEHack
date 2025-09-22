import json
from datetime import datetime
from Post import Post
from User import User
from Role import Role



class Guild:
    def __init__(self, name, owner, description, locations):
        # Generate guild_id based on creation timestamp
        self.creation_date = datetime.now()
        self.guild_id = self.guild_id = self.creation_date.strftime("%Y%m%d%H%M%S%f")

        self.name = name
        self.owner = owner            # user_id of the owner
        self.description = description
        self.locations = list(locations)        # list of strings

        self.roles = []     # list of role objects
        self.members = []   # list User objects
        self.posts = []     # list Post objects



    # ----
    # Getters
    # ----
    def get_guild_id(self):
        return self.guild_id


    def get_name(self):
        return self.name


    def get_owner(self):
        return self.owner


    def get_description(self):
        return self.description


    def get_locations(self):
        return self.locations


    def get_roles(self):
        return self.roles


    def get_members(self):
        return self.members
    

    def get_members_by_user_ids(self, user_ids: list[str]):
        """Return User objects that match the given user IDs."""

        matched_members = []
        for member in self.members:
            if member.user_id in user_ids:
                matched_members.append(member)
        return matched_members
    

    def get_members_by_roles(self, role_names: list[str]):
        """Return all members who have any of the given roles."""

        matched_members = []
        for member in self.members:
            for role in member.roles:
                if role.name in role_names:
                    matched_members.append(member)
                    break   # stop after finding one matching role
        return matched_members


    def get_posts(self):
        return self.posts
    

    def get_posts_by_members(self, users: list[User]):
        """Return all posts created by certain members (by user_id)."""
        user_ids = []
        for user in users:
            user_ids.append(user.user_id)

        posts_by_members = []
        for post in self.posts:
            if post.user_id in user_ids:
                posts_by_members.append(post)

        return posts_by_members


    def get_creation_date(self):
        """Return datetime object"""

        return self.creation_date



    # ----
    # Setters
    # ----
    def set_guild_id(self, guild_id):
        self.guild_id = guild_id


    def set_name(self, name):
        self.name = name


    def set_owner(self, owner):
        self.owner = owner


    def set_description(self, description):
        self.description = description
  

    def set_creation_date(self, creation_date):
        self.creation_date = creation_date


    def add_location(self, new_location):
        self.locations.append(new_location)


    def add_role(self, role):
        self.roles.append(role)


    def add_members(self, new_members: list[User]):
        """Add new members if they are not already in the guild."""

        for member in new_members:
            already_exists = False
            for existing_member in self.members:
                if existing_member.user_id == member.user_id:
                    already_exists = True
                    break
            if not already_exists:
                self.members.append(member)


    def add_post(self, new_post: Post):
        # Check if the post's author is in the guild
        if not any(member.user_id == new_post.user_id for member in self.members):
            raise ValueError(f"Cannot add post because user_id {new_post.user_id} is not part of {self.name} guild.")

        # Check if post_id already exists
        if any(post.post_id == new_post.post_id for post in self.posts):
            raise ValueError(f"Post ID {new_post.post_id} already exists in {self.name} guild.")

        # Sync the post's guild_id with this guild
        new_post.set_guild_id(self.guild_id)

        # Add the post
        self.posts.append(new_post)



    # ----
    # Delete
    # ----
    def delete_roles(self, role_names: list[str]):
        """Delete certain roles from guild and strip them from all members."""

        # Remove roles from guild's role list
        updated_roles = []
        for role in self.roles:
            if role.name not in role_names:
                updated_roles.append(role)
        self.roles = updated_roles

        # Remove roles from each member's role list
        for member in self.members:
            updated_member_roles = []
            for role in member.roles:
                if role.name not in role_names:
                    updated_member_roles.append(role)
            member.roles = updated_member_roles


    def delete_members_by_roles(self, role_names: list[str]):
        """Delete members (from guild's member list) who have any of the given roles.
        Their roles are cleared before removal, and their posts are detached
        from the guild."""

        user_ids_to_delete = set()
        updated_members = []

        for member in self.members:
            has_forbidden_role = False

            # See if this member has any of the forbidden roles
            for role in member.roles:
                if role.name in role_names:
                    has_forbidden_role = True
                    break

            # Decide whether to remove or keep this member
            if has_forbidden_role:
                member.roles = [] 
                user_ids_to_delete.add(member.user_id)
            else:
                updated_members.append(member)

        # Clean up posts by affected members
        for post in self.posts:
            if post.user_id in user_ids_to_delete:
                post.delete_guild_id()

        # Update the guild’s member list
        self.members = updated_members


    def delete_members_by_user_ids(self, users: list[User]):
        """Delete members whose user IDs match the given User objects.
        Their roles are cleared automatically by removing the member object,
        and their posts are detached from the guild."""

        user_ids_to_delete = set()

        # Gather all user IDs to delete
        for user in users:
            user_ids_to_delete.add(user.user_id)

        updated_members = []

        # Filter out members that should be deleted
        for member in self.members:
            if member.user_id not in user_ids_to_delete:
                updated_members.append(member)

        # Clean up posts by affected members
        for post in self.posts:
            if post.user_id in user_ids_to_delete:
                post.delete_guild_id()

        # Update the guild’s member list
        self.members = updated_members

    
    def delete_posts_by_members(self, members: list[User]):
        """Delete all posts belonging to certain members (by user_id).
        Posts are detached from the guild."""

        user_ids = []
        for member in members:
            user_ids.append(member.user_id)

        updated_posts = []
        for post in self.posts:
            if post.user_id not in user_ids:
                updated_posts.append(post)
            else:
                post.delete_guild_id()

        self.posts = updated_posts


    def delete_all_members(self):
        """Delete all members from the guild.
        Their roles are cleared before removal, and their posts are detached
        from the guild."""

        for member in self.members:
            member.roles = []

        for post in self.posts:
            post.delete_guild_id(-1)

        self.members = []


    def delete_all_posts(self):
        """Delete all posts in the guild and clear their guild_id.
        Posts are detached from the guild before removal."""

        for post in self.posts:
            post.delete_guild_id()

        self.posts = []


    
    # ----
    # JSON
    # ----
    def to_dict(self):
        """Return Python dict"""

        guild_data = {}

        # Basic fields
        guild_data["guild_id"] = self.guild_id
        guild_data["name"] = self.name
        guild_data["owner"] = self.owner
        guild_data["description"] = self.description
        guild_data["locations"] = self.locations

        # Nested objects
        guild_data["roles"] = []
        for role in self.roles:
            guild_data["roles"].append(role.to_dict())

        guild_data["members"] = []
        for member in self.members:
            guild_data["members"].append(member.to_dict())

        guild_data["posts"] = []
        for post in self.posts:
            guild_data["posts"].append(post.to_dict())

        # Date
        guild_data["creation_date"] = self.creation_date.isoformat()

        return guild_data


    def to_json(self):
        """Return JSON string"""

        return json.dumps(self.to_dict())

