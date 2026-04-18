from flask import Flask, render_template, request, jsonify
from config import Config
from services.validator import Validator
from services.ai_service import AIService
from services.parser import ResponseParser

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    """Serve the frontend."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze incident using Groq API."""
    data = request.get_json()
    
    if not data or 'incident' not in data:
        return jsonify({'error': 'Missing incident description'}), 400
    
    incident = data['incident'].strip()
    
    # 1. Validate
    valid, error_msg = Validator.validate_incident(incident)
    if not valid:
        return jsonify({'error': error_msg}), 400
    
    # 2. Call AI Service
    api_response = AIService.analyze_incident(incident)
    
    # 3. Parse & Respond
    if api_response:
        parsed = ResponseParser.parse_json(api_response)
        if parsed:
            return jsonify({
                'success': True,
                'data': parsed
            })
    
    # 4. Fallback if API fails or parsing fails
    return jsonify({
        'success': True,
        'data': Config.FALLBACK_RESPONSE,
        'fallback': True
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
