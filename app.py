from flask import Flask,request
from flask_pymongo import MongoClient
from bson import ObjectId
import os
app=Flask(__name__)
datastore=MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],port=27017)
db=datastore.tasks
@app.route('/',methods=['POST',"GET"])
def home():
    if request.method == "GET":
        return str(list(db.task.find()))
    else:
        got=request.args
        tasks=dict(got)
        db.task.insert_one(tasks)
        return "success"


@app.route('/search',methods=["GET"])
def search():
    if request.method=="GET":
        search_values=request.args
        return str(list(db.task.find(search_values,{"_id":0})))
@app.route('/update/<id>',methods=["GET"])
def update(id):
    id=ObjectId(id)
    if request.method=='GET':

        curr=db.task.find_one({"_id":id})
        updates=dict(request.args)
        db.task.update({"_id":id},{"$set":updates})
        return "sucess"
@app.route('/delete/<id>',methods=["GET"])
def delete(id):
    id=ObjectId(id)
    if request.method=="GET":
        db.task.remove({"_id":id})
        return "success"






if (__name__=="__main__"):
    app.run(debug=True,host='0.0.0.0',port=5000)
