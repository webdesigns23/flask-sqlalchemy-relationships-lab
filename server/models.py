from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# TODO: add association table
session_speakers = db.Table('session_speakers', metadata,
    db.Column('session_id', db.Integer, 
        db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('speaker_id', db.Integer,
        db.ForeignKey('speakers.id'), primary_key=True)
)

# TODO: set up relationships for all models
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # O2M Relationship mapping the event to related sessions
    sessions = db.relationship('Session', back_populates="event", cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Event {self.id}, {self.name}, {self.location}>'

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)
    # O2M add Foreign key stores the Event id
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # M2M Relationship mapping the employee to related meetings
    speakers = db.relationship(
        'Speaker', secondary=session_speakers, back_populates='sessions')

    # Relationship mapping the review to related employee
    event = db.relationship('Event', back_populates="sessions")

    def __repr__(self):
        return f'<Session {self.id}, {self.title}, {self.start_time}>'


class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # M2M Relationship mapping the employee to related meetings
    sessions = db.relationship(
        'Session', secondary=session_speakers, back_populates='speakers')
    
    # O2O has one bio, Relationship mapping speaker to related bio
    bio = db.relationship(
        'Bio', uselist=False, back_populates='speaker')    

    def __repr__(self):
        return f'<Speaker {self.id}, {self.name}>'

class Bio(db.Model):
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.Text, nullable=False)
    # O2O belongs to speaker, add Foreign key to store the speaker id
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'))

    # Relationship mapping onboarding to related speaker
    speaker = db.relationship('Speaker', back_populates='bio')

    def __repr__(self):
        return f'<Bio {self.id}, {self.bio_text}>'
