from app import db
from datetime import datetime
from sqlalchemy import func


class Measurement(db.Model):
    __tablename__ = "measurements"

    id = db.Column(db.Integer, primary_key=True)
    humidity = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    pollution = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, temperature, humidity, pollution):
        self.temperature = temperature
        self.humidity = humidity
        self.pollution = pollution

    def __repr__(self):
        return f'Temperature: {self.temperature}; Humidity: {self.humidity}; Pollution: {self.pollution};'
