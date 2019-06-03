
import re

class DataValidation():
    """This class validates user inputs"""
    def __init__(self,description=None,location=None):
        self.description = description
        self.location = location

    def validate_special_char(self,description,location):
        regex = re.compile(r'\A[a-zA-Z0-9*]+\Z')
        if not re.match(r"[A-Za-z]",description):
            return "Special characters not allowed!"
        elif not regex.match(location):
            return "Special characters not allowed!"

        # elif not re.match(r"[A-Za-z]",location):
        #     return "Special characters not allowed!"

        return [description,location]

    def validate_whitespace(self,description,location):
        if location.isspace():
            return "Location cannot be left blank"
        elif description.isspace():
            return "Description cannot be left blank"

        return self.validate_special_char(self.description,self.location)

    def validate_datatype(self,description,location):

        if not isinstance(description,str):
            return "Description must be a string and not integer"
        elif not isinstance(location,str):
            return "Location must be a string and not integer"

        return self.validate_whitespace(self.description,self.location)

    def submit(self):
        """pass data through validation checks"""
        if not self.location:
            return "Location cannot be blank"
        elif not self.description:
            return "Description cannot be blank"

        return self.validate_datatype(self.description,self.location)
        
        