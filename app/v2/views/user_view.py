
from flask_api import FlaskAPI
from flask import request, jsonify, abort, make_response


from app.api.v2.models import Incident, User

def incidents():
    # Get the access token from the header
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]

    if access_token:
        # Attempt to decode the token and get the User ID
        user_id = User.decode_token(access_token)
        print('===================================')
        print(user_id)
        print('===================================')
        if not isinstance(user_id, str):
            # If the id is not a string(error), we have a user id
            # Go ahead and handle the request, the user is authenticated

            if request.method == "POST":
                comment = str(request.data.get('comment', ''))
                location = str(request.data.get('location', ''))
                media = str(request.data.get('media', ''))
                if media and comment and location:
                    redflag = Incident(comment=comment,location=location,media=media,created_by=user_id)
                    redflag.save()
                    response = jsonify({
                        'id': redflag.id,
                        'comment':redflag.comment,
                        'location' : redflag.location,
                        'media' : redflag.media,
                        'status' : redflag.status,
                        'incidentType': redflag.incidentType,
                        'date_created': redflag.date_created,
                        'date_modified': redflag.date_modified,
                        'created_by':user_id
                        })
                    response.status_code = 201
                    return make_response(response)
                else:
                    return "lol"
            else:
                # GET
                redflags = Incident.query.filter_by(created_by=user_id)
                
                results = []
                for redflag in redflags:
                    obj = {
                        'id': redflag.id,
                        'comment':redflag.comment,
                        'location' : redflag.location,
                        'media' : redflag.media,
                        'status' : redflag.status,
                        'incidentType': redflag.incidentType,
                        'date_created': redflag.date_created,
                        'date_modified': redflag.date_modified,
                        'created_by':redflag.created_by
                        }
                    
                    results.append(obj)
                return make_response(jsonify(results)), 200
        
        else:
            # user is not legit, so the payload is an error message
            message = user_id
            response = {'messag': message}
            return make_response(jsonify(response)), 401

def incident(id, **kwargs):
    # Get the access token from the header
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]

    if access_token:
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            # Get the bucketlist with the id specified from the URL (<int:id>)

            incident = Incident.query.filter_by(id=id).first()

            if not incident:
                return "not incident", 404

            elif request.method == "PUT":
                incidentType = str(request.data.get('incidentType',''))
                comment = str(request.data.get('comment', ''))
                location = str(request.data.get('location', ''))
                media = str(request.data.get('media', ''))

                incident.incidentType = incidentType
                incident.comment = comment
                incident.location = location
                incident.media = media

                incident.save()
                
                return "edited", 200

            elif request.method == "DELETE":
                incident.delete()
                return "lol deleted", 200
            else:
                response = jsonify({
                    'id':incident.id,
                    'incidentType':incident.incidentType,
                    'comment':incident.comment,
                    'location' : incident.location,
                    'media' : incident.media,
                    'status' : incident.status,
                    'date_created': incident.date_created,
                    'date_modified': incident.date_modified
                })
                response.status_code = 200
                return response
        else:
            message = user_id
            response = {"message":message}
            return make_response(jsonify(response)), 401
