#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = [{'id': event.id,'name': event.name, 'location': event.location} for event in events]
    return jsonify(events_list), 200

@app.route('/events/<int:id>/sessions', methods=['GET'])
def get_event_sessions(id):
    event = db.session.get(Event, id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    session_data = [{
        'id': session.id, 
        'title': session.title, 
        'start_time': session.start_time.isoformat()
        }
        for session in event.sessions]
    return jsonify(session_data), 200

@app.route('/speakers', methods=['GET'])
def get_speakers():
    speakers = Speaker.query.all()
    speakers_list = [{'id': speaker.id,'name': speaker.name} for speaker in speakers]
    return jsonify(speakers_list), 200

@app.route('/speakers/<int:id>', methods=['GET'])
def get_speaker(id):
    speaker = db.session.get(Speaker, id)
    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404
    bio_text = speaker.bio.bio_text if speaker.bio else "No bio available"
    response_data = {'id': speaker.id, 'name': speaker.name, 'bio_text': bio_text}
    return jsonify(response_data), 200

@app.route('/sessions/<int:id>/speakers', methods=['GET'])
def get_session_speakers(id):
   session = db.session.get(Session, id)
   if not session:
       return jsonify({"error": "Session not found"}), 404
   
   speaker_data = [{
       'id': speaker.id, 
       'name': speaker.name, 
       'bio_text': speaker.bio.bio_text if speaker.bio else "No bio available"
       }
       for speaker in session.speakers]
   return jsonify(speaker_data), 200
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)