import json
from datetime import datetime


class Role:
    def __init__(self, name, description="", requirements=None, permissions=None):
        # Generate role_id based on timestamp (with microseconds to avoid duplicates)
        self.creation_date = datetime.now()
        self.role_id = self.creation_date.strftime("%Y%m%d%H%M%S%f")

        self.name = name
        self.description = description

        # Requirements are conditions a user must meet to qualify for this role
        if requirements is None:
            self.requirements = []
        else:
            self.requirements = requirements

        # Permissions are actions that certain roles are allowed to do
        if permissions is None:
            self.permissions = []
        else:
            self.permissions = permissions



    # ----
    # Getters
    # ----
    def get_role_id(self):
        return self.role_id


    def get_name(self):
        return self.name


    def get_description(self):
        return self.description


    def get_requirements(self):
        return self.requirements


    def get_permissions(self):
        return self.permissions


    def get_creation_date(self):
        return self.creation_date



    # ----
    # Setters
    # ----
    def set_name(self, name):
        self.name = name


    def set_description(self, description):
        self.description = description

    
    def set_requirements(self, requirements: list[str]):
        self.requirements = requirements


    def add_requirements(self, requirements: list[str]):
        """Add one or more requirements. Must be a list of strings."""

        if not isinstance(requirements, list):
            raise TypeError("requirements must be a list of strings")

        for req in requirements:
            if not isinstance(req, str):
                raise TypeError("each requirement must be a string")
            if req not in self.requirements:
                self.requirements.append(req)


    def set_permissions(self, permissions: list[str]):
        self.permissions = permissions


    def add_permissions(self, permissions: list[str]):
        """Add one or more permissions. Must be a list of strings."""

        if not isinstance(permissions, list):
            raise TypeError("permissions must be a list of strings")

        for perm in permissions:
            if not isinstance(perm, str):
                raise TypeError("each permission must be a string")
            if perm not in self.permissions:
                self.permissions.append(perm)



    # ----
    # Delete
    # ----
    def delete_name(self):
        self.name = None


    def delete_description(self):
        self.description = None


    def delete_requirements(self):
        self.requirements = []


    def delete_permissions(self):
        self.permissions = []



    # ----
    # JSON
    # ----
    def to_dict(self):
        """Return Python dict"""

        role_dict = {}

        role_dict["role_id"] = self.role_id
        role_dict["name"] = self.name
        role_dict["description"] = self.description
        role_dict["requirements"] = self.requirements
        role_dict["permissions"] = self.permissions
        role_dict["creation_date"] = self.creation_date.isoformat()

        return role_dict


    def to_json(self):
        """Return JSON string"""

        return json.dumps(self.to_dict())

