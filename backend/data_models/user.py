from enum import Enum

class Role(Enum):
    """
    Represents the possible roles a user can have.
    """
    ADMIN = "admin"
    GUEST = "guest"

    def __str__(self):
        return self.value

class User: 
    """ check import
    """


    def __init__(self, user_id: int, username: str, email: str, user_role: Role):
        """
        Constructor for the User class.

        Args:
        user_id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        user_role (str): IAM for the feature
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.user_role = user_role
    
    def __repr__(self):
        """
        Returns a string representation of the User object.
        """
        return f"User(user_id={self.user_id}, username='{self.username}', email='{self.email}', user_role={self.user_role})"
    



    
def main():
    user1 = User(user_id=1, username="alice", email="alice@example.com", user_role= Role.ADMIN)
    user2 = User(user_id=2, username="bob", email="bob@example.com", user_role = Role.GUEST)

    print(user1)
    print(user2)

if __name__ == "__main__":
    main()

