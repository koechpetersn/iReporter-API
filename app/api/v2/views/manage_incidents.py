from . import v2_blueprint

from flask import request, jsonify, abort, make_response
from flask.views import MethodView

#local imports
from .base import Base
from app.api.validations import DataValidation
from app.api.v2.models.models import IncidentModel

class IncidentPost(MethodView,Base):
    """class to handle incident post requests"""
    def post(self):
        """handle post request"""
        payload = IncidentPost.helper()
        if not isinstance(payload,str):
            description = request.data['description']
            location = request.data['location']
            validate_items = DataValidation(description=description,location=location)
            validation = validate_items.submit()

            if not isinstance(validation,str):
                description = validation[0]
                location = validation[1]
                incident = IncidentModel(
                    description=description,
                    location=location,
                    created_by=payload)
                incident.save()
                response = incident.view()
                return make_response({
                    "message":"Incident reported succesfully",
                    "incident":response
                    }),201
            return {"message":validation},401
        return{
            "message":"Not allowed. Ensure you are logged in as a user"
            },401

            # description = str(request.data.get('description', ''))
            # location = str(request.data.get('location', ''))

class IncidentsAdminFetch(MethodView,Base):
    """class to handle fetching of incidents by users or admin"""
    def get(self):
        """Fetch incidents by specific user or all incidents"""
        payload = IncidentsAdminFetch.helper()
        if payload == "admin":
            incidents = IncidentModel.admin_get_all()
            if incidents:
                results=[]
                for incident in incidents:
                    obj=IncidentModel.view(incident)
                    results.append(obj)
                return {"reported incidents":results},200
            return {"message":"There are no reported incidents"},404
        return {"message":"Not allowed. Ensure you are logged in as an admin"},401

class IncidentsFetch(MethodView,Base):
    """class"""
    def get(self):
        payload =IncidentsFetch.helper()
        if not isinstance(payload,str):
            incidents = IncidentModel.get_all(payload)
            # import pdb; pdb.set_trace()
            if incidents:
                results=[]
                for incident in incidents:
                    obj=IncidentModel.view(incident)
                    results.append(obj)
                return {"reported incidents":results},200
            return {"message":"You have no incidents at the moment"},404
        return {"message":"Not allowed. Ensure you are logged in as a user"},401

class IncidentAdminFetch(MethodView,Base):
    """Handle fetching of a specific incident by admin and owner"""
    def get(self,incident_id):
        """def"""
        payload = IncidentAdminFetch.helper()
        if payload == "admin":
            incident = IncidentModel.admin_get_specific(incident_id)
            if incident:
                result=IncidentModel.view(incident)
                return {
                    "message":"Incident found",
                    "Incident": result},200
            return{"message":"Incident not found"},404
        return {"message":"Not allowed. Ensure you are logged in as an admin"},401

class IncidentFetch(MethodView,Base):
    """class"""
    def get(self,incident_id):
        """def"""
        payload = IncidentFetch.helper()
        if not isinstance(payload,str):
            incidents = IncidentModel.get_all(payload)
            if incidents:
                results=[]
                for incident in incidents:
                    if incident.id==incident_id:
                        obj=IncidentModel.view(incident)
                        results.append(obj)
                        return {
                            "message":"Incident found",
                            "Incident": results},200
            return{"message":"Incident not found"},404
        return {
            "message":"Not allowed. Ensure you are logged in as a user"
            },401

class IncidentDel(MethodView,Base):
    """class to handle deletion of an incident by owner"""
    def delete (self,incident_id):
        """def"""
        payload = IncidentDel.helper()
        if not isinstance (payload,str):
            incidents = IncidentModel.get_all(payload)
            if incidents:
                incident = [incident for incident in incidents if incident.id==incident_id]

                if incident:
                    IncidentModel.delete(incident[0])
                    return {
                        "message":"Incident deleted successfully"
                        },200
                return {
                    "message":"Incident does not exist"
                },404
            return {"message":"You have no reported incidents"},404
        return {
            "message":"Not allowed. Ensure you are logged in as a user"
            },401

class IncidentEdit(MethodView,Base):
    """class to handle modification of an existing record"""
    def put(self,incident_id):
        """def"""
        payload = IncidentEdit.helper()
        if not isinstance(payload,str):
            description = str(request.data.get('description', ''))
            location = str(request.data.get('location', ''))
            incidents = IncidentModel.get_all(payload)
            if incidents:
                for incident in incidents:
                    if incident.id==incident_id:
                        if incident.status == "Draft":
                            validate_items = DataValidation(description=description,location=location)
                            validation = validate_items.submit()
                            if not isinstance(validation,str):
                                description = validation[0]
                                location = validation[1]
                                incident.description = description
                                incident.location = location
                                incident.save()
                                return {
                                    "message":"Record updated"
                                },200
                            return{
                                "message":validation
                                },401
                        return{
                                "message":"Only 'draft' records are available for edit"
                                },401
                    return {"message":"Record not found"},404
            return {"message":"You have no reported incidents"},404
        return {
            "message":"Not allowed. Ensure you are logged in as a user"
        },401
                        
class IncidentStatusEdit(MethodView,Base):
    """class to handel modification of an existing record"""
    def put(self,incident_id):
        """def"""
        payload = IncidentStatusEdit.helper()
        if payload == "admin":
            status = str(request.data.get('status', ''))
            incident = IncidentModel.admin_get_specific(incident_id)
            if incident:
                incident.status = status
                incident.save()
                return {"message":"Record upated"},200
            return {"message":"Record not found"},404
        return {
            "message":"Not allowed. Ensure you are logged in as an admin"
        },401    


# Define the rule for the registration url
# Then add the rule to the blueprint
post_incident = IncidentPost.as_view('post_incident')
fetch_incidents = IncidentsFetch.as_view('fetch_incidents')
fetch_incidents_admin = IncidentsAdminFetch.as_view('fetch_incidents_admin')
fetch_incident = IncidentFetch.as_view('fetch_incident')
fetch_incident_admin = IncidentAdminFetch.as_view('fetch_incident_admin')
del_incident = IncidentDel.as_view("del_incident")
edit_incident = IncidentEdit.as_view('edit_incident')
edit_status = IncidentStatusEdit.as_view("edit_status")

v2_blueprint.add_url_rule(
    '/v2/user/post/incident',
    view_func=post_incident,
    methods=['POST'])

v2_blueprint.add_url_rule(
    '/v2/user/get/incidents',
    view_func=fetch_incidents,
    methods=['GET'])

v2_blueprint.add_url_rule(
    '/v2/admin/get/incidents',
    view_func=fetch_incidents_admin,
    methods=['GET'])

v2_blueprint.add_url_rule(
    '/v2/user/get/incident/<int:incident_id>',
    view_func=fetch_incident,
    methods=['GET'])

v2_blueprint.add_url_rule(
    '/v2/admin/get/incident/<int:incident_id>',
    view_func=fetch_incident_admin,
    methods=['GET'])

v2_blueprint.add_url_rule(
    '/v2/user/del/incident/<int:incident_id>',
    view_func=del_incident,
    methods=['DELETE'])

v2_blueprint.add_url_rule(
    '/v2/admin/put/incident/<int:incident_id>',
    view_func=edit_status,
    methods=['PUT'])

v2_blueprint.add_url_rule(
    '/v2/user/put/incident/<int:incident_id>',
    view_func=edit_incident,
    methods=['PUT'])

