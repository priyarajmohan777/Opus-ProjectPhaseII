"""
OPUS Career Management Platform - Main Entry Point
This file integrates all modules: prediction, chatbot, and resume_match
"""

from flask import Flask, session
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Factory function to create and configure the Flask app"""
    
    app = Flask(__name__, 
                static_folder='prediction/static',
                template_folder='prediction/templates')
    
    # Shared secret key for session management across modules
    app.secret_key = os.getenv('SECRET_KEY', 'opus_secret_key_change_in_production')
    
    # Session configuration
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
    
    # Register blueprints from each module
    
    # 1. Prediction Module
    from prediction.app import prediction_bp
    app.register_blueprint(prediction_bp)
    
    # 2. Chatbot Module  
    from chatbot.app import chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    
    # Note: Resume Match module can be added here when ready
    # from resume_match.app import resume_bp
    # app.register_blueprint(resume_bp, url_prefix='/resume')
    
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return {'status': 'healthy', 'modules': ['prediction', 'chatbot']}
    
    return app

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 OPUS Career Management Platform")
    print("=" * 60)
    print("📊 Prediction Module: Active")
    print("🤖 Chatbot Module: Active (Groq API)")
    print("=" * 60)
    print("🌐 Access at: http://localhost:5000")
    print("=" * 60)
    
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)