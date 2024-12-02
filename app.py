from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "hs.456.king@gmail.com"
app.config['MAIL_PASSWORD'] = 'obop kuzc dlnd xygi'

db = SQLAlchemy(app)
mail = Mail(app)

# Database Models
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    project_type = db.Column(db.String(50))
    timeline = db.Column(db.String(50))
    description = db.Column(db.Text)
    budget = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def serve_index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

@app.route('/<path:path>')
def serve_files(path):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), path)

@app.route('/api/contact', methods=['POST'])
def handle_contact():
    data = request.json
    try:
        # Save to database
        new_contact = Contact(
            name=data['name'],
            email=data['email'],
            message=data['message']
        )
        db.session.add(new_contact)
        db.session.commit()

        # Send email notification
        msg = Message('New Contact Form Submission',
                     sender=app.config['MAIL_USERNAME'],
                     recipients=[app.config['MAIL_USERNAME']])
        msg.body = f"""
        New contact form submission:
        Name: {data['name']}
        Email: {data['email']}
        Message: {data['message']}
        """
        mail.send(msg)
        return jsonify({"message": "Message sent successfully"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/service-request', methods=['POST'])
def handle_service_request():
    data = request.json
    try:
        # Save to database
        new_request = ServiceRequest(
            name=data['name'],
            email=data['email'],
            project_type=data['projectType'],
            timeline=data['timeline'],
            description=data['description'],
            budget=data['budget']
        )
        db.session.add(new_request)
        db.session.commit()

        # Send email notification
        msg = Message('New Service Request',
                     sender=app.config['MAIL_USERNAME'],
                     recipients=[app.config['MAIL_USERNAME']])
        msg.body = f"""
        New service request:
        Name: {data['name']}
        Email: {data['email']}
        Project Type: {data['projectType']}
        Timeline: {data['timeline']}
        Description: {data['description']}
        Budget: {data['budget']}
        """
        mail.send(msg)
        return jsonify({"message": "Service request submitted successfully"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(
        host='0.0.0.0',
        port=443,
        ssl_context=('cert.pem', 'key.pem')
    )

