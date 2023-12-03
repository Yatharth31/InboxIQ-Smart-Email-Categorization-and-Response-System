from email import header
from flask import Flask,request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import os
from main import ProcessEmail
app = Flask(__name__)
api = Api(app)
import sys
sys.argv=['']
del sys
import json


# @app.route("/mail",methods=("POST",))
# def create():

#     # try:
#     json_got = request.data
#     print(json_got)
#     # except Exception as e:
#     #     print(e)
#     ProcessEmail()
#     return {'status': "Running"}, 200


class Mail(Resource):
    def get(self):
        return {'data': "get_test"}, 200  # return data and 200 OK code
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True,type=str)
        parser.add_argument('password', required=True,type=str)
        parser.add_argument('test',type=str)
        args = parser.parse_args()
        f1 = open("emailID.txt", "w")
        f1.write(args["id"])
        f1.close()

        f2 = open("password.txt", "w")
        f2.write(args["password"])
        f2.close()

        ProcessEmail(test=args['test'])

        return {'status': "Running"}, 200


api.add_resource(Mail, '/mail/')


if __name__ == '__main__':
    app.run()