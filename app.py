from flask import Flask, request, jsonify, session
from flask_pymongo import PyMongo
from flask_cors import CORS
import json
import ast
from bson import json_util

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb://manisha:manisha123@ds145434.mlab.com:45434/blogpoint"
app.config['SECRET_KEY'] = "manisha"
mongo = PyMongo(app)


@app.route("/")
def home_page():
    return "Welcome"


@app.route("/user/signup", methods=["POST"])
def addUser():
    data = request.get_json()
    user = mongo.db.users
    isUserExist = user.find_one({'userName': data["userName"]})

    if(isUserExist):
        return jsonify(
            {
                "message": "User already exist",
                "success": False,
                # "user": str(isUserExist)
            })
    else:
        user.insert(
            {'userName': data["userName"],
             'passWord': data["passWord"],
             'emailId': data["emailId"]})

        return jsonify(
            {
                "success": True,
                "user": str(user.find_one({'userName': data["userName"]}))
            })


@app.route("/user/login", methods=["POST"])
def userLogin():
    data = request.get_json()
    user = mongo.db.users
    isUserExist=""
    session["isUserExist"] = user.find_one({'userName': data["userName"]})
    #session ["username"]=user.find_one({'userName': data["userName"]})
    if(isUserExist):
        return jsonify(
            {

                "success": True,
                "user": str(isUserExist),

            })
    else:
        return jsonify(
            {
                "success": False
            })


@app.route("/user/feedback", methods=["POST"])
def submitFeeback():
    data = request.get_json()
    feedback = mongo.db.feedbacks
    feedback.insert({
        'feedbackHeading': data["feedbackHeading"],
        'feebackDescription': data["feebackDescription"]})


@app.route("/user/submitBlog", methods=["POST"])
def submitBlog():
    data = request.get_json()
    blogs = mongo.db.blogs
    blogs.insert({
        'blogHeading': data["blogHeading"],
        'blogSummary': data["blogSummary"],
        'blogDescription': data["blogDescription"],
        'blogType': data["blogType"],
        'userName': data["userName"]
    })
    return jsonify(
        {
            "success": True
        }
    )


@app.route("/user/getBlog", methods=["POST", "GET"])
def getBlog():
    data = request.get_json()
    blogs = mongo.db.blogs
    result = blogs.find({})
    results = [results for results in result]

    return jsonify({
        "success": True,
        "results": json.loads(json_util.dumps(results))

    })


@app.route("/user/updatePassword", methods=["POST", "GET"])
def updatePassword():
    data = request.get_json()
    users = mongo.db.users
    users.update({"passWord": data["passWord"]}, {
                 '$set': {"passWord": data["newPassword"]}})
    return jsonify({
        "success": True

    })


@app.route("/user/userBlog", methods=["POST", "GET"])
def getUserBlog():
    data = request.get_json()
    blogs = mongo.db.blogs
    results = []
    result = blogs.find({'userName': data['userName']}, {
                        'blogHeading', 'blogDescription', 'blogType', 'blogSummary'})
    results = [results for results in result]

    return jsonify({
        "success": True,
        "results": json.loads(json_util.dumps(results))

    })


@app.route("/user/logout",methods=["POST", "GET"])
def logOut():
    print("inside logout backend")
    session.pop('isUserExist')
    return jsonify({
        "success": True, })


@app.route("/user/deleteblog", methods=["POST", "GET", "DELETE"])
def deleteBlog():
    data = request.get_json()
    blogs = mongo.db.blogs
    result = blogs.remove({'blogHeading': data['blogHeading']})
    return jsonify({
        "success": True,
    })


if __name__ == '__main__':
    app.run(debug=True)
