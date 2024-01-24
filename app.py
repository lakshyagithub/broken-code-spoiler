from flask import Flask, request, jsonify, render_template
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/token')
def generate_token():
    #add your twilio credentials 
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_SYNC_SERVICE_SID = os.getenv('TWILIO_SYNC_SERVICE_SID')
    TWILIO_API_KEY = os.getenv('TWILIO_API_KEY')
    TWILIO_API_SECRET = os.getenv('TWILIO_API_SECRET')

    username = request.args.get('username', fake.user_name())
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())



if __name__ == "__main__":
    app.run(host='127.0.0.1', port='81')

