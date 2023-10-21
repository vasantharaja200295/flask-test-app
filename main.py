from flask import Flask, send_from_directory, render_template, request, redirect
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import os

uri = f"mongodb+srv://{os.getenv("MONGOUSERNAME")}:{os.getenv("PASSWORD")}@cluster0.vpzkuqi.mongodb.net/mydb?retryWrites=true&w=majority"
mongoClient = MongoClient(uri, server_api=ServerApi('1'))

app = Flask(__name__)

try:
    mongoClient.admin.command('ping')
    print(">> Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



db = mongoClient.get_database('mydb').get_collection('todos')

@app.route("/")
def main():
    todos = db.find()
    return render_template('index.html', todos = todos, complete_todo=complete_todo)

@app.route('/add_todo', methods=["POST"])
def add_todo():
    data = request.form.get("todo")
    payload = {"todoItem": data, 
               "completed":False}
    db.insert_one(payload)
    return redirect("/")

@app.route("/complete-todo/<id>")
def complete_todo(id):
    db.update_one({'_id':ObjectId(id)}, {"$set": {"completed": True}})
    return redirect("/")


@app.route("/delete-todo/<id>")
def delete_todo(id):
    db.delete_one({'_id':ObjectId(id)})
    return redirect("/")


@app.route("/update/<id>", methods=["POST"])
def update_todo(id):
    data = request.form.get('update_todo')
    db.update_one({'_id':ObjectId(id)}, {"$set": {"todoItem": data}})
    return redirect("/")


@app.route('/cdn/<path:file>')
def serve(file):
    path = "./static"
    return send_from_directory(path, file)




if (__name__) == "__main__":
    app.run()