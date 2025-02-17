from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from models import db, User
from flask_session import Session
from config import ApplicationConfig



app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/@me")
def get_user_info():
   user_id = session.get("user.id")
   
   if user_id is None:
       return {"message": "User not logged in"}, 401

   user = User.query.filter_by(id=user_id).first()
   return jsonify({
     "id": user.id,
     "email": user.email,
     "message": "Welcome!"
   })



@app.route('/register', methods=['POST'])
def register_user():
    email = request.json['email']
    password = request.json['password']

    user_exist = User.query.filter_by(email=email).first() is not None

    if user_exist:
        return {"message": "User already exists"}, 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return ({"message": "User registered successfully"}), 201

    
@app.route('/login', methods=['POST'])
def login_user():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return {"message": "Invalid credentials"}, 401

    session['user.id'] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email,
        "Message": "Welcome Back!",
    })







if __name__ == "__main__":
    app.run(debug=True)

print(app.url_map)

