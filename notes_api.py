from flask import Flask
from flask_restful import Api,Resource,abort,reqparse,fields,marshal_with
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
resource_fields = {
    'id' : fields.Integer ,
    'title' : fields.String ,
    'body' : fields.String ,
    'is_pinned' : fields.Integer ,
    'in_trash' : fields.Integer ,
}
# *****************************

# request *********************
class Notes(Resource) :
    @marshal_with(resource_fields)
    def get(self) :
        data = NotesModel.query.all()
        notes = []
        for note in data :
            notes.append(
                {
                    'id' : note.id ,
                    'title' : note.title ,
                    'body' : note.body ,
                    'is_pinned' : note.is_pinned ,
                    'in_trash' : note.in_trash ,
                }
            )
        return notes
    @marshal_with(resource_fields)
    def post(self) :
        args = add_note_args.parse_args()
        note = NotesModel(
            title = args['title'] ,
            body = args['body'] ,
            is_pinned = 0 ,
            in_trash = 0 ,
        )
        db.session.add(note)
        db.session.commit()
        return note , 201
    
# *****************************

api.add_resource(Notes,'/notes')
if __name__ == "__main__" :
    my_app.run(debug=True,host="0.0.0.0")