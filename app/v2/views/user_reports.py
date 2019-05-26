from . import view_blueprint

from flask.views import MethodView
from flask import request, jsonify, abort, make_response

from .base_view import Base
from .validations import DataValidation
from app.v2.models.incident_models import IncidentModel
from app.v2.models.user_models import UserModel

class IncidentReport(MethodView,Base):
    """This class creates and manipulates an incident"""
    def post(self):
        """Handle POST request for this view. Url ---> /incidents/report"""
        user_id = IncidentReport.helper()
        if not isinstance(user_id,str):
            # User_id is not string error, we have a valid user
            user_data = request.data
            if user_data:
                datam = DataValidation(**user_data)
                data = DataValidation.submit(datam)

                if data == "whitespace":
                    resp = {"message":"Missing fields, Please supply data for all fields"}

                elif data == "invalid comment datatype":
                    resp = {"message":"Please provide a brief comment excluding numbers"}

                elif data == "invalid location datatype":
                    resp = {"message":"Please provide precise and valid location name"}
                else:
                    comment = data[0]
                    location = data[1]
                    incident = IncidentModel(comment=comment,location=location,created_by=user_id)
                    incident.add_incident()
                    resp = {"message":"Incident has been reported successfully"}
                    return make_response(jsonify(resp)), 201

                return make_response(jsonify(resp)),404

            else:
                return {"message":"Please fill the form before submiting"},404
        else:
            # user is not legit, so the payload is an error message
            response = {'message': user_id}
            return make_response(jsonify(response)), 401

class IncidentFetchAll(MethodView,Base):
    """This class handles how incidents are fetched"""

    def get(self):
        """Users can fetch their own incidents"""

        payload = IncidentFetchAll.helper()
        if isinstance(payload,int):
            #we have an int id, thus a valid user
            incidents = IncidentModel.get_all_by(payload)
            if incidents:

                incidents = [IncidentModel.view(incident) for incident in incidents]
                return {"reported incidents":incidents},200

            else:
                return {"message":"You have no reported incidents"},404
        else:
            # user is not legit, so the payload is an error message
            message = payload
            response = {'message': message}
            return make_response(jsonify(response)), 401
class IncidentFetchBy(MethodView,Base):
    """This class handles how incidents are fetched"""
    def get(self,incident_id):
        """get a single incident"""
        payload = IncidentFetchBy.helper()

        if not isinstance(payload,str):
            incidents = IncidentModel.get_all_by(payload)
            
            if incidents:

                incident = [IncidentModel.view(incident) for incident in incidents if incident["id"]==incident_id]
                if not incident == None:
                    return incident,200
                return "river gulu no incident match"
            return "you have no incidents at all"
                
        else:
            # user is not legit, so the payload is an error message
            message = payload
            response = {'message': message}
            return make_response(jsonify(response)), 401
class IncidentEdit(MethodView,Base):
    """class"""
    def edit(self):
        """edit incident"""
        pass

class IncidentDel(MethodView,Base):
    """class"""
    def delete(self,incident_id):
        """delete incident"""
        payload = IncidentDel.helper()
        if not isinstance(payload,str):
            # get own incidents first
            incidents = IncidentModel.get_all_by(payload)
            if incidents:
                for incident in incidents:
                    if incident["id"] == incident_id:
                        IncidentModel.delete_incident(incident_id)
                        return {"message":"Deleted successfully"},200
                    return {"message":"incident not found"},404
            return {"message":"You have no reported incidents"},404
        return {"message":"Operation not allowed, Please log in first"}

report_view = IncidentReport.as_view('report_view')
get_view = IncidentFetchAll.as_view('get_view')
get_by_view = IncidentFetchBy.as_view('get_by_view')
edit_view = IncidentEdit.as_view('edit_view')
del_view = IncidentDel.as_view('del_view')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
view_blueprint.add_url_rule(
    '/v2/user/report/incident',
    view_func=report_view,
    methods=['POST'])

view_blueprint.add_url_rule(
    '/v2/user/get/incidents',
    view_func=get_view,
    methods=['GET'])

view_blueprint.add_url_rule(
    '/v2/user/get/incident/<int:incident_id>',
    view_func=get_by_view,
    methods=['GET'])

view_blueprint.add_url_rule(
    '/v2/user/edit/incident/<int:incident_id>',
    view_func=edit_view,
    methods=['EDIT'])

view_blueprint.add_url_rule(
    '/v2/user/del/incident/<int:incident_id>',
    view_func=del_view,
    methods=['DELETE'])
