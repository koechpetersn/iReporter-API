
from flask import request, jsonify

# from app.v2.models.incident_models import IncidentModel
# from app.v2.models.user_models import UserModel

class DataValidation():
    """This class validates user inputs"""
    def __init__(self,comment,location):
        self.comment = comment
        self.location = location
        # return [comment,location]

    def validate_whitespace(self,comment,location):
        if len(comment)<1:
            return "whitespace"
        elif len(location)<1:
            return "whitespace"

        return [comment,location]


    def validate_datatype(self,comment,location):


        if not isinstance(comment,str):
            return "invalid comment datatype"
        elif not isinstance(location,str):
            return "invalid location datatype"

        return self.validate_whitespace(self.comment,self.location)



    def submit(self):
        """hdshvchsbsc"""
        return self.validate_datatype(self.comment,self.location)
        
        