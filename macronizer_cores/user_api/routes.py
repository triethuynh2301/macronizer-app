from flask import Blueprint, request, jsonify, flash
from flask_login import login_required, current_user
from macronizer_cores import db
from macronizer_cores.models import User
user_api = Blueprint('user_api', __name__)

# SECTION - routes
@user_api.route('/api/user/edit' , methods=['PUT'])
# @login_required
def update_user():
    '''
    PUT /api/user/edit
    ----------------------------------------------------------------
    Update user info

    Returns
    ----------------
    User info in JSON format and status code 201
    '''

    try:
        user_to_edit = User.query.get_or_404(current_user.id)
        user_to_edit.name = request.json.get('name')
        user_to_edit.email = request.json.get('email')
        user_to_edit.username = request.json.get('username')

        db.session.commit()

        res = jsonify(user=user_to_edit.serialize())
        flash('Your changes have been saved', 'success')
        return (res, 201)
    except:
        res = {"message": "Can't update user"}
        return (res, 500)

    