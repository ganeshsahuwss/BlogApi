import json
from flask import Flask, Response, flash, request, jsonify,render_template, url_for,redirect
from flask_mongoengine import MongoEngine



app = Flask(__name__)


app.config['MONGODB_SETTINGS'] = {'db': 'employee','host': 'localhost','port': 27017}
#myclient=MongoEngine.MongoClient("mongodb+srv://admin:admin123.@demo.6qr8ysp.mongodb.net/test")
#app.config["MONGO_URI"]="mongodb+srv://admin:<password>@demo2.hksrhf2.mongodb.net/?retryWrites=true&w=majority"

db = MongoEngine()
db.init_app(app)

#table create

class my(db.Document):
    id =db.StringField(primary_key=True)                                                   
    header = db.StringField(max_length=10)
    img=db.StringField()
    short_Description =db.StringField(max_length=20)
    Article =db.StringField(max_length=1020)
    
    def to_json(self):
        return {"id":self.id,
                "header":self.header,
                "img":self.img,
                "short_Descripation":self.short_Description,
                "Aartical":self. Article
                }

#----------------------------------------login--------------------------------------------------   
class login(db.Document):
    email=db.StringField()
    password=db.StringField(max_length=10)

    def to_json(self):
        return {"email":self.email,
                "password":self.password}
#--------------comment----------------------------------------------------------        
class comment(db.Document):
    # id =db.StringField(primary_key=True)
     comment=db.StringField(max_length=120)
     count=db.StringField()
     
     
     def to_json(self):
        return {#"id":self.id,
                "comment":self.comment,
                "count":self.count}  
#--------------------------------------------like-----------------------------------------------------
# class Like(db.Document):
#     id = db.StringField(primary_key=True)
#     recipe_id = db.ForeignKeyField(my, backref='comment', lazy_load=False)
    
    
#     def to_json(self):
#         return {"id":self.id,
#                 "recipe_id":self.recipe_id} 
#--------------------------------------------like-----------------------------------------------------
class like(db.Document):
    id=db.StringField(primary_key=True)


     
     
#home page    
@app.route("/index")
def index():
    return render_template('index.html')

#get data
@app.route('/show',methods=["GET"])
def get():
    user = my.objects().to_json()
    return Response(user,mimetype="application/json")

#post data
@app.route('/addrecord', methods=['POST'])
def create_record():
    record = json.loads(request.data)
    user = my(id=record["id"],
                 header=record["header"],
                 img=record["img"],
                 short_Description=record["short_Description"],
                 Article=record["Article"])
    user.save()
    response = {
                'status': 'success',
                'message': 'record add successfully',
                'data':[]
            }
    
    return jsonify(user.to_json(),response)

#update
@app.route("/edit/<id>",methods=["PUT"])
def editview(id):
   
    record=json.loads(request.data)
    my.objects.get(id=id).update(**record)

    
    return jsonify({'status': 'success','message': ' edit successfully',})    


#delete
@app.route("/delete/<id>",methods=["DELETE"])
def deleteview(id):
    my.objects.get(id=id).delete()
    
    return jsonify({'status': 'success','message': 'delete successfully'})   


#login api
@app.route("/login",methods=["POST"])
def log():
    record=json.loads(request.data)
    user=login(email=record["email"],
               password=record["password"])
    user.save()
    response = {
                'status': 'success',
                'message': 'login successfully',
                'data':[]
            }
    return jsonify(user.to_json(),response)


    


#comment api
@app.route("/comment/<id>",methods=["POST"])
def commentview(id):
    my.objects.get(id=id)                 #.update(**record)
    record=json.loads(request.data)
    user=comment(comment=record["comment"]) #id=record["id"],
    user.save()
    response = {
                'status': 'success',
                'message': 'login successfully',
                'data':[]
            }
    return jsonify(user.to_json(),response)



#like
@app.route("/like/<id>",methods=["POST"])
def like_view(id):
    #my.objects.get(id=id)
    my.objects.count(id=id)
    record=json.loads(request.data)
    user=comment(like=record["like"]) #id=record["id"]
    user.save()
    return jsonify(user.to_json())






if __name__=="__main__":
    app.run(debug=True)

