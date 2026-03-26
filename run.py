from app import create_app
from app.extensions import db
from flask_security.utils import hash_password
from flask import Flask, session, render_template
from flask_security import SQLAlchemyUserDatastore
from app.models import User, Role
from app import create_app, user_datastore

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        # your code here to do things before first request
        @app.before_request
        def create_all():
            # The following line will remove this handler, making it only run on the first request
            app.before_request_funcs[None].remove(create_all)
            # Create any database tables that don't exist yet.
            db.create_all()
 
            # Create the Roles "admin" and "end-user" -- unless they already exist
            user_datastore.find_or_create_role(name='admin', description='Administrator')
            user_datastore.find_or_create_role(name='end-user', description='End user')
 
            # Create two Users for testing purposes -- unless they already exists.
            # In each case, use Flask-Security utility function to encrypt the password.
            #encrypted_password = utils.encrypt_password('password')
            encrypted_password = hash_password('password') 
            if not user_datastore.find_user(email='juan@example.com'):
                user_datastore.create_user(name='Juan', email='juan@example.com', password=encrypted_password)
            if not user_datastore.find_user(email='admin@example.com'):
                user_datastore.create_user(name='Emmanuel', email='admin@example.com', password=encrypted_password)
 
            # Commit any database changes; the User and Roles must exist before we can add a Role to the User
            db.session.commit()
 
            # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
            # Users already have these Roles.) Again, commit any database changes.
            user_datastore.add_role_to_user(user_datastore.find_user(email='juan@example.com'), 'end-user')
            user_datastore.add_role_to_user(user_datastore.find_user(email='admin@example.com'), 'admin')
            db.session.commit()

            @app.before_request
            def make_session_permanent():
                session.permanent = True
                app.logger.debug("Sesión renovada")
    app.run(debug=True)