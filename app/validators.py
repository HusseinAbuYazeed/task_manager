import re 

class Validator:
    
    @staticmethod
    def validate_username(username: str) -> str | bool: 
        """it makes sure that the username doesn't have less than 3 letters
        and doesn't contain weird symbols"""
        username = username.strip()

        if len(username) < 3:
            return "it should be 3 or more"
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return "it can contain letters or numbers or underscore only"
        return True

    @staticmethod 
    def validate_email(email: str) -> str | bool:
        """checks if the email is valid for example: test@example.com"""
        email = email.strip()
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            return "email format is not valid"
        return True

    @staticmethod
    def validate_password(password: str) -> str | bool: 
            """it makes sure that the password doesn't have less than 6 letters"""
            password = password.strip()
    
            if len(password) < 6:
                return "it should be 6 or more"
            return True
