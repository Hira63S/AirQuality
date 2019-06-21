"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from decouple import config
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

api = openaq.OpenAQ()

@APP.route('/')
def root():
    """Base view."""

#    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    records = Record.query.filter(Record.value >10).all()
    list_of_t = []
    for record in records:
        t = (record.datetime, record.value)
        list_of_t.append(t)
    return str(list_of_t)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<date {} --- value {}>'.format(self.datetime, self.value) #this comes from < Time 2019-03-07T23:00:00.000Z --- Value 3.0 >

@APP.route('/refresh')

def refresh():
    """ Resets the database """
#    DB.drop_all()
    DB.create_all()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    for a in range(0,100):
        t = (body['results'][a]['date']['utc'], body['results'][a]['value']) #should look like having date, utz, and then value.
        r = Record(datetime=str(t[0]), value=str(t[1]))
    DB.session.add(r)
    DB.session.commit()
    return 'data refreshed!'
