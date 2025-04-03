from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages',methods=['GET'])
def get_messages():
    
    messages=Message.query.order_by(Message.created_at.asc()).all()
    messages_dict=[message.to_dict() for message in messages]
    return jsonify(messages_dict),200

    

@app.route('/messages',methods=['POST'])
def post_message():
    data=request.get_json()
    new_message=Message(
        body=data['body'],
        username=data['username']
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_dict()),201

@app.route('/messages/<int:id>',methods=['PATCH'])
def patch_message(id):
    message=Message.query.filter(Message.id ==id).first()
    data=request.get_json()
    for attr, value in data.items():
        if hasattr(message, attr): 
            setattr(message, attr, value)
    db.session.add(message)
    db.session.commit()

    return jsonify(message.to_dict()),200

@app.route('/messages/<int:id>',methods=['DELETE'])
def delete_message(id):
    
    message=Message.query.filter(Message.id ==id).first()
    db.session.delete(message)
    db.session.commit()

    return make_response({'message': 'Message deleted'}, 200)

if __name__ == '__main__':
    app.run(port=5555)
