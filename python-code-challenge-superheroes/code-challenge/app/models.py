from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from app import db, Hero,HeroPower,Power

db = SQLAlchemy()

hero_powers = db.Table(
    'hero_powers',
    db.Column('hero_id', db.Integer, db.ForeignKey('heroes.id'), primary_key=True),
    db.Column('power_id', db.Integer, db.ForeignKey('powers.id'), primary_key=True)
)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define the many-to-many relationship using the hero_powers table
    powers = db.relationship('Power', secondary=hero_powers, backref=db.backref('heroes', lazy='dynamic'))

    def serialize(self):
        serial_powers = [power.serialize() for power in self.powers]
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
            'powers': serial_powers
        }

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define the many-to-many relationship using the hero_powers table
    heroes = db.relationship('Hero', secondary=hero_powers, backref=db.backref('powers', lazy='dynamic'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
    @validates('description')
    def validates_description(self, key, description):
        if len(description) < 20:
            raise ValueError('Invalid: Description must be at least 20 characters')
        return description

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero =  db.relationship('Hero')
    power = db.relationship('Power')

    def serialize(self):
        return self.hero.serialize()
    
    @validates('strength')
    def validate_strength(self, key, strength):
        allowed_strength = ['Strong', 'Weak', 'Average']
        if strength not in allowed_strength:
            raise ValueError(f"{key} must be one of: {', '.join(allowed_strength)}")
        return strength