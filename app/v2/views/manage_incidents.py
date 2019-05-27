from . import view_blueprint

from flask.views import MethodView
from flask import request, jsonify, abort, make_response

from .base_view import Base
from app.v2.models.incident_models import IncidentModel
from app.v2.models.user_models import UserModel


class IncidentAdminFetchAll(MethodView,Base):
    """This class handles admin users fetch incidents"""
    def get(self):
        """Admin users can fetch all incidents reported by other users"""
        payload = IncidentAdminFetchAll.helper()
        if payload == "admin":
            #we have a valid admin user
            incidents= IncidentModel.get_all()
            if incidents:
                results=[]
                for incident in incidents:
                    obj=IncidentModel.view(incident)
                    results.append(obj)
                return {"reported incidents":results},200
            else:
                return {"message":"There are no reported incidents"},404

        else:
            # user is not admin
            message = payload
            response = {'message': message}
            return make_response(jsonify(response)), 401
class IncidentAdminFetchOne(MethodView,Base):
    """This class handles how admin user fetch a single incident"""
    def get(self,incident_id):
        """get a single incident"""
        payload = IncidentAdminFetchOne.helper()
        if payload == "admin":
            incident = IncidentModel.get(id=incident_id)
            if incident:
                    result = {
                        "message":"incident found",
                        "Incident":IncidentModel.view(incident)
                    }
                    return result,200
            return {"message": "Incident not found"},200
                
        else:
            # user is not legit, so the payload may be an error message
            message = payload
            response = {'message': message}
            return make_response(jsonify(response)), 401

class IncidentEditStatus(MethodView,Base):
    """Admin can edit status of an incident"""
    def put(self):
        """edit status only"""
        pass

class IncidentDel(MethodView,Base):
    """Admin can delete incidents marked as 'solved"""
    def delete(self,incident_id):
        """delete incident"""
        payload = IncidentDel.helper()
        if payload == "admin":
            incident = IncidentModel.get(id=incident_id)
            if incident:
                IncidentModel.delete_incident(incident_id)
                return{"message":"Incident deleted successfuly"},200
            return {"message":"Incident not found"},404
        return {"message":"Operation not allowed, Please log in first"}

admin_get = IncidentAdminFetchAll.as_view('admin_get')
admin_get_by = IncidentAdminFetchOne.as_view('admin_get_by')
admin_edit = IncidentEditStatus.as_view('admin_edit')
admin_del = IncidentDel.as_view('admin_del')

view_blueprint.add_url_rule(
    '/v2/admin/get/incidents',
    view_func=admin_get,
    methods=['GET'])

view_blueprint.add_url_rule(
    '/v2/admin/get/incident/<int:incident_id>',
    view_func=admin_get_by,
    methods=['GET'])

view_blueprint.add_url_rule(
    '/v2/admin/edit/incident/<int:incident_id>',
    view_func=admin_edit,
    methods=['PUT'])

view_blueprint.add_url_rule(
    '/v2/admin/del/incident/<int:incident_id>',
    view_func=admin_del,
    methods=['DELETE'])