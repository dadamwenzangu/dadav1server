from email import message
from ntpath import join
from flask import Flask, request, jsonify, make_response
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import bcrypt
import datetime, json
from mongoengine import connect

from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from mongoengine.queryset.visitor import Q
from dotenv import load_dotenv

app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)


load_dotenv()
#connect_string=f'mongodb+srv://admin-s:<password>@dada.d383gqt.mongodb.net/?retryWrites=true&w=majority' 




# JWT Config
app.config['MONGODB_SETTINGS'] = {
    #'host':'mongodb+srv://admin-s:passc^d22@dada.d383gqt.mongodb.net/?retryWrites=true&w=majority'
    'host':'mongodb://localhost/Dada001'
}

app.config["JWT_SECRET_KEY"] = "dada11secrety"

db = MongoEngine(app)



class User(db.Document):
    first_name = db.StringField(required=True)
    last_name = db.StringField()
    email = db.StringField()
    age = db.IntField()
    phone = db.IntField()
    password = db.StringField()
    curr_loc = db.PointField()
    join_date = db.DateTimeField(default=datetime.datetime.utcnow)

@app.route('/',methods=('GET', 'POST'))
def  home():
        return 'Calm Down'


@app.route('/new_user',methods=('GET', 'POST'))
def  create_new_user():
    #users = User.objects()

    if request.method == 'POST':
        body = request.get_json()
        user = User(**body).save()
     
    else:
        users= User.objects()
        print(users.to_json())
        return jsonify(users), 200



   
@app.route('/helpers',methods=('GET', 'POST'))
def  get_helpers():
   
    

    if request.method == 'POST':
        content=request.get_json()
        email = content['user']['email']
        print(email)
        coordinates=[]
        coordinates.append(content['curr_loc']['coordinates'][0])
        coordinates.append(content['curr_loc']['coordinates'][1])
        print(coordinates)

         #users = User.objects()
        #user= User.objects.filter(Q(curr_loc__near={"type": "Point", "coordinates": coordinates} ,curr_loc__max_distance=200)  and Q(email__ne=email))
        user= User.objects.filter(Q(point__near=[coordinates] ,point__max_distance=2)  and Q(email__ne=email))[:3]

      #  print(len(user))
        
        #print(user)
        #print([ i.to_json() for i in user] )
        #print(user)

        user = user.to_json()
        userd = json.loads(user)
        for i in userd:
            del i['age']
            del i['curr_loc']
            del i['join_date']
            del i['password']

        
        result = {}
        #result['user_id'] =  userd['_id']['$oid']
        result = userd[:4]
        

        
        
        return jsonify(result) , 200
     
    
        

        
            
        
        
        
        #print(type(near_user) )

    

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':

        content = request.get_json()
        email = content['email']
        password = content['password']
        hash_pswd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        existing_user = User.objects(email= 'email').first()
        print(existing_user)
        if existing_user:
            return jsonify(message="User Already Exists"), 409
        else:
            first_name = content['fname']
            last_name = content['lname']
            email = content['email']
            password = hash_pswd
            age = content['age']
            phone = content['phone']
            join_date = datetime.datetime.today()
            curr_loc = content['curr_loc']
            new_user = dict(first_name=first_name, last_name=last_name, email=email, phone=phone,
                            age=age, password=password, join_date=join_date, curr_loc=curr_loc)
            User(first_name = content['fname'],
            last_name = content['lname'],
            email = content['email'],
            password = hash_pswd,
            age = content['age'],
            phone = content['phone'],
            join_date = datetime.datetime.today(),
            curr_loc = content['curr_loc']).save()
            return jsonify(message="New User Added Successfully"), 201


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        content = request.get_json()
        email = content['email']
        password = content['password']
        #hash_pswd =  bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        existing_user = User.objects.get_or_404(email= email)
        
        existing_user.to_json()
        e_password = existing_user['password']
        print(e_password)
        print(password.encode('utf-8'))

        if existing_user:
            if bcrypt.checkpw(e_password,password):
                # if bcrypt.hashpw(content['password'].encode('utf-8'), existing_user['password'] == existing_user['password']):
                access_token = create_access_token(identity=email)
                return jsonify(message="Login Successful!", access_token=access_token), 201
            else:
                return jsonify(message="Invalid Email or Password"), 409
    return existing_user 

@app.route('/near_users', methods=('GET', 'POST'))

def get_users_within_radius():
    location = [-1.3035103694033294, 36.78752743970288]
    existing_user = User.objects({'first_name': 'Jackie'})
    print(existing_user)

    rad = 0.3
    METERS_PER_MILE = 1609.34

    """near_users = Users.find()
    print(near_users)
    for i in near_users:
        print(type(i))"""

    
   
    
    response =[doc for doc in Users.find_one({'first-name': 'Sally'})]
    print(response)
    return response
    
