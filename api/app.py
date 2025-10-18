from flask import Flask, request, jsonify
from database import create_database, insert_examples, database_exists, delete_database

app = Flask(__name__)

from routes.user_routes import user_bp
from routes.data_routes import data_bp
from routes.config_routes import config_bp
from routes.alert_routes import alert_bp

app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(data_bp, url_prefix='/api/data')
app.register_blueprint(config_bp, url_prefix='/api/config')
app.register_blueprint(alert_bp, url_prefix='/api/alerts')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Alert System API"})

if __name__ == "__main__":
    cli_response = None
    while cli_response not in ['y', 'n']:
        cli_response = input("Would you want to delete the database (if exists)? (y/n): ")

    if cli_response == 'y': 
        delete_database()

    if not database_exists():
        create_database()
        insert_examples()

    app.run(debug=True, host='0.0.0.0', port=5000)       insert_examples()
