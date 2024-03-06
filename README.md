# Notes API
## about
A simple Flask-RESTful API allows the client to create, edit and delete notes .
## endpoints
There is only one endpoint to reach all methods .
## methods
### /GET
##### code :
``` python

    def get(self) :
        data = NotesModel.query.all()
        notes = []
        for note in data :
            notes.append(
                {
                    'id' : note.id ,
                    'title' : note.title ,
                    'body' : note.body ,
                    'date' : note.date ,
                    'is_pinned' : note.is_pinned ,
                    'in_trash' : note.in_trash ,
                }
            )
        return notes
    
```
##### response :
Response is a list of note item
``` json

[
    {
        "id": 1,
        "title": " first title ",
        "body": " this is the first notes body ",
        "date": "10/12/2024",
        "is_pinned": 0,
        "in_trash": 0
    },
    {
        "id": 2,
        "title": " second note ",
        "body": " this is the notes body  of the second note ",
        "date": "10/12/2024",
        "is_pinned": 0,
        "in_trash": 0
    }
]

```
If ther is no notes yet, the response will be an empty list
```json
[]
```
__________________________________________________

### /POST
##### body :
It is required to send all needed data in the query
``` json

{
    "title" : " second note " ,
    "body" : " this is the notes body  of the second note " ,
    "date" : "10/12/2024"
}

```
##### code :
``` python

def post(self) :
        args = add_note_args.parse_args()
        note = NotesModel(
            title = args['title'] ,
            body = args['body'] ,
            date = args['date'] ,
            is_pinned = 0 ,
            in_trash = 0 ,
        )
        db.session.add(note)
        db.session.commit()
        return note , 201

```
##### response :
The response is the note item with details
``` json

{
    "id": 2,
    "title": " second note ",
    "body": " this is the notes body  of the second note ",
    "date": "10/12/2024",
    "is_pinned": 0,
    "in_trash": 0
}

```
__________________________________________________

### /PUT
##### body :
All the fields are optional except the note's id
``` json

{
    "id" : 2,
    "title" : " second title " ,
    "body" : " this is the first notes body " ,
    "date" : "10/12/2024"
}

```
##### code :
``` python

    def put(self) :
        args = put_note_args.parse_args()
        note = NotesModel.query.filter_by(id = args['id']).first()
        if not note :
            abort(404,message='Oooops!, we couldn\'t find this note')
        if args['title'] :
            note.title = args['title']
        if args['body'] :
            note.body = args['body']
        if args['is_pinned'] == 0:
            note.is_pinned = 1
        if args['is_pinned'] == 1:
            note.is_pinned = 0
        if args['in_trash'] == 0:
            note.in_trash = 1
        if args['in_trash'] == 1:
            note.in_trash = 0
        db.session.commit()
        return note

```
##### response :
Response is the updated note's details
``` json

{
    "id": 2,
    "title": " second title ",
    "body": " this is the first notes body ",
    "date": "10/12/2024",
    "is_pinned": 0,
    "in_trash": 0
}

```
If the note is not exist
```json
{
    "message": "Oooops!, we couldn't find this note"
}
```
__________________________________________________

### /DELETE
##### body :
To delete a note all you just need is the id .
``` json

{
    "id" : 7
}

```
##### code :
``` python

def delete(self) :
        args = delete_note_args.parse_args()
        note = NotesModel.query.filter_by(id = args['id']).first()
        if not note :
            abort(404,message='Oooops!, we couldn\'t find this note')
        db.session.delete(note)
        db.session.commit()
        return {
            'message' : 'note deleted successfully'
        }

```
##### response :
If the note is not exist
``` json
{
    "message": "Oooops!, we couldn't find this note"
}
```
Else
``` json
{
    "message": "note deleted successfully"
}
```
__________________________________________________
## issues in development
#### issue !
  As of Flask-SQLAlchemy 3.0, all access to db.engine (and db.session) requires an active Flask application context. db.create_all uses db.engine .
  - so create database function should be called as shown below
```python
with app.app_context():
    db.create_all()
```
__________________________________________________
## Dockerizing
### How to dockerize ?
#### steps : 
  - Use Ubuntu as a base image
  - update packages
  - install python
  - instal flask
  - install flask-restful
  - install flask-sqlalchemy
  - copy project file to container
  - run the source code
#### Dockerfile
```Dockerfile
FROM ubuntu
RUN apt update
RUN apt install python3-pip -y
RUN pip3 install flask
RUN pip3 install flask-restful
RUN pip3 install flask-sqlalchemy
RUN pip3 install flask-cors
WORKDIR /app
COPY . .
CMD ["python3","/app/notes_api.py"]
```
_______________________________________________________________________
_______________________________________________________________________
## Thank you for reading
