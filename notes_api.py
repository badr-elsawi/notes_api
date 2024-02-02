from flask import Flask
from flask_restful import Api,Resource,abort,reqparse
from flask_sqlalchemy import SQLAlchemy
# ***********************************************
my_app = Flask(__name__)
api = Api(my_app)
# initiate database **********
my_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(my_app)
class NotesModel(db.Model) :
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(500))
    is_pinned = db.Column(db.Integer)
    in_trash = db.Column(db.Integer)

with my_app.app_context() :
    db.create_all()
# ****************************

# arguments ******************
add_note_args = reqparse.RequestParser()
add_note_args.add_argument('title',type=str,help='task is required',required=True)
add_note_args.add_argument('body',type=str,help='body is required',required=True)
# *****************************

# request *********************
class Notes(Resource) :
    def get(self) :
        notes = []
        return {
            'message' : '',
            'age' : notes,
        }
    
    def post(self) :
        note = add_note_args.parse_args()
        return {
            'title' : note.title ,
            'body' : note.body
        }
    
# *****************************

api.add_resource(Notes,'/notes')
if __name__ == "__main__" :
    my_app.run(debug=True,host="0.0.0.0")