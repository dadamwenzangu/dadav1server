from email import message
from ntpath import join
from flask import Flask, request, jsonify, make_response
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import bcrypt, uuid
import datetime, json
from mongoengine import connect

from werkzeug.security import generate_password_hash, check_password_hash

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
    'host':'mongodb+srv://admin-s:passc^d22@dada.d383gqt.mongodb.net/?retryWrites=true&w=majority'
    #'host':'mongodb://localhost/Dada001'
}

app.config["JWT_SECRET_KEY"] = "dada11secrety"

db = MongoEngine(app)



class User(db.Document):
    userid=name = db.StringField(required=True)
    name = db.StringField(required=True)
    #last_name = db.StringField()
    email = db.StringField()
    age = db.IntField()
    phone = db.IntField()
    idnum = db.IntField()
    password = db.StringField()
    curr_loc = db.PointField()
    date_created = db.DateTimeField(default=datetime.datetime.utcnow)
    date_edited = db.DateTimeField(default=datetime.datetime.utcnow)

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


@app.route('/single_user/<userid>',methods=('GET', 'POST'))
def get_user_by_id(userid: str):
    user = User.objects(userid=userid).first()

    user = user.to_json()
    userd = json.loads(user)
    

    del userd['curr_loc']
    del userd['date_created']
    del userd['password']
    del userd['_id']

    print(userd)

    return jsonify(userd), 200
   
@app.route('/edit_single_user/<userid>', methods=['PUT'])
def update_user(userid):
    content = request.get_json()

    user = User.objects(userid=userid)
    
    user.update(name = content['user']['name'],
            #last_name = content['lname'],
            email = content['user']['email'],
            age = content['user']['age'],
            phone = content['user']['phone'],
            idnum = content['user']['idnum'],
            date_edited= datetime.datetime.today(),)


    
    user = user.to_json()
    userd = json.loads(user)
    print(userd)
    

    del userd[0]['curr_loc']
    del userd[0]['date_created']
    del userd[0]['date_edited']
    del userd[0]['password']
    del userd[0]['_id']

    return jsonify(userd), 200
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
            del i['date_created']
            del i['date_edited']
            del i['password']
            del i['_id']

        
        result = {}
        #result['user_id'] =  userd['_id']['$oid']
        result = userd[:4]
        

        
        
        return jsonify(result) , 200
     
    
        

        
            
        
        
        
        #print(type(near_user) )

    

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':

        content = request.get_json()
        print(content)
        email = content['user']['email']
        password = content['user']['password']
        
        existing_user = User.objects(email= email).first()
        print(existing_user)
        if existing_user:
            return jsonify(message="User Already Exists"), 409
        else:
            
            name = content['user']['name']
            #last_name = content['lname']
            email = content['user']['email']
            password = password
            age = content['user']['age']
            phone = content['user']['phone']
            idnum = content['user']['idnum']
            date_created = datetime.datetime.today()
            curr_loc = content['user']['curr_loc']
            new_user = dict(name=name, email=email, phone=phone,idnum=idnum,
                            age=age, password = generate_password_hash(password), date_created=date_created, curr_loc=curr_loc)
            User(userid = str(uuid.uuid4()),name = content['user']['name'],
            #last_name = content['lname'],
            email = content['user']['email'],
            password = generate_password_hash(password),
            age = content['user']['age'],
            phone = content['user']['phone'],
            idnum = content['user']['idnum'],
            date_created = datetime.datetime.today(),
            curr_loc = content['user']['curr_loc']).save()
            return jsonify(message="User Created Successfully"), 201


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        content = request.get_json()
        email = content['user']['email']
        password = content['user']['password']
        #hash_pswd =  bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        existing_user = User.objects.get_or_404(email= email)
        
        existing_user.to_json()
        e_password = existing_user['password']
   

        if existing_user:
            if check_password_hash(e_password, password):
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
    
