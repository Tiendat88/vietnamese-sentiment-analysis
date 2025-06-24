import os
import re
import pickle
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

class VietnameseSentimentAnalyzer:
    def __init__(self, model_path: str):
        self.model = None
        self.vectorizer = None
        self.model_path = model_path
        self.is_loaded = False
        self.load_model()
        
        # Vietnamese text preprocessing mappings
        self.vietnamese_replacements = {
            r'\b2day\b': 'hôm nay',
            r'\bko\b': 'không',
            r'\bk\b': 'không', 
            r'\br\b': 'rồi',
            r'\bdc\b': 'được',
            r'\bvs\b': 'với',
            r'\bmk\b': 'mình',
            r'\bt\b': 'tôi',
            r'\bny\b': 'này',
            r'\bsp\b': 'sản phẩm',
            r'\bshop\b': 'cửa hàng'
        }
        
        self.label_mapping = {
            'POS': 'positive',
            'NEG': 'negative', 
            'NEU': 'neutral'
        }
    
    def load_model(self) -> bool:
        try:
            if not Path(self.model_path).exists():
                logger.error(f"Model file not found: {self.model_path}")
                return False
            
            abs_path = os.path.abspath(self.model_path)
            logger.info(f"Loading model from: {abs_path}")
            
            with open(abs_path, 'rb') as f:
                model_data = pickle.load(f)
            
            if 'model' not in model_data or 'vectorizer' not in model_data:
                logger.error("Invalid model file format")
                return False
            
            self.model = model_data['model']
            self.vectorizer = model_data['vectorizer']
            self.is_loaded = True
            
            logger.info(f"✅ Model loaded successfully!")
            logger.info(f"   Model type: {type(self.model).__name__}")
            logger.info(f"   Vectorizer type: {type(self.vectorizer).__name__}")
            logger.info(f"   Model classes: {self.model.classes_}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error loading model: {str(e)}")
            self.is_loaded = False
            return False
    
    def preprocess_text(self, text: str) -> str:
        if not isinstance(text, str) or not text.strip():
            return ""
        
        text = text.lower().strip()
        
        # Apply Vietnamese replacements
        for pattern, replacement in self.vietnamese_replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Remove URLs and emails
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\S+@\S+', '', text)
        
        # Clean punctuation but preserve Vietnamese chars
        text = re.sub(r'[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩùúụủũưừứựửữòóọỏõôồốộổỗơờớợởỡỳýỵỷỹđ]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def predict_sentiment(self, text: str) -> dict:
        if not self.is_loaded or self.model is None or self.vectorizer is None:
            logger.error("Model not loaded")
            return None
        
        try:
            processed_text = self.preprocess_text(text)
            
            if not processed_text:
                logger.warning("Empty text after preprocessing")
                return None
            
            # Use trained model for prediction
            text_vector = self.vectorizer.transform([processed_text])
            prediction = self.model.predict(text_vector)[0]
            probabilities = self.model.predict_proba(text_vector)[0]
            
            sentiment = self.label_mapping.get(prediction, 'unknown')
            confidence = float(max(probabilities))
            
            # Create probability dictionary
            prob_dict = {}
            classes = self.model.classes_
            for i, class_label in enumerate(classes):
                mapped_label = self.label_mapping.get(class_label, class_label)
                prob_dict[mapped_label] = float(probabilities[i])
            
            result = {
                'sentiment': sentiment,
                'confidence': confidence,
                'probabilities': prob_dict,
                'processed_text': processed_text,
                'original_text': text,
                'model_info': {
                    'model_type': type(self.model).__name__,
                    'classes': list(self.model.classes_),
                    'feature_count': text_vector.shape[1]
                }
            }
            
            logger.info(f"Prediction: '{text}' -> {sentiment} ({confidence:.3f})")
            return result
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            return None

# Initialize analyzer
MODEL_PATH = "/vietnamese_sentiment_model.pkl"
analyzer = VietnameseSentimentAnalyzer(MODEL_PATH)

@app.route('/')
def home():
    """Simple home page without complex template"""
    if analyzer.is_loaded:
        status = "✅ Model loaded successfully!"
        model_type = type(analyzer.model).__name__
        classes = list(analyzer.model.classes_)
    else:
        status = "❌ Model not loaded"
        model_type = "N/A"
        classes = []
    
    html = f"""
    <html>
    <head>
        <title>Vietnamese Sentiment Analysis API</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
            .status {{ padding: 15px; border-radius: 8px; margin: 20px 0; }}
            .success {{ background: #d4edda; color: #155724; }}
            .error {{ background: #f8d7da; color: #721c24; }}
            .code {{ background: #f8f9fa; padding: 10px; border-radius: 5px; font-family: monospace; }}
        </style>
    </head>
    <body>
        <h1>🧠 Vietnamese Sentiment Analysis API</h1>
        
        <div class="status {'success' if analyzer.is_loaded else 'error'}">
            <strong>Status:</strong> {status}
        </div>
        
        <h3>📊 Model Information:</h3>
        <ul>
            <li><strong>Model Type:</strong> {model_type}</li>
            <li><strong>Classes:</strong> {', '.join(classes)}</li>
            <li><strong>Ready:</strong> {'Yes' if analyzer.is_loaded else 'No'}</li>
        </ul>
        
        <h3>🔗 API Endpoints:</h3>
        
        <h4>1. POST /api/analyze</h4>
        <div class="code">
        curl -X POST http://localhost:5001/api/analyze \\<br>
        &nbsp;&nbsp;-H "Content-Type: application/json" \\<br>
        &nbsp;&nbsp;-d '{{"text": "Sản phẩm tuyệt vời!"}}'
        </div>
        
        <h4>2. GET /api/status</h4>
        <div class="code">curl http://localhost:5001/api/status</div>
        
        <h4>3. POST /api/batch</h4>
        <div class="code">
        curl -X POST http://localhost:5001/api/batch \\<br>
        &nbsp;&nbsp;-H "Content-Type: application/json" \\<br>
        &nbsp;&nbsp;-d '{{"texts": ["Text 1", "Text 2"]}}'
        </div>
    </body>
    </html>
    """
    return html

@app.route('/api/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing text field',
                'message': 'Please provide: {"text": "your text"}'
            }), 400
        
        text = data['text']
        
        if not isinstance(text, str) or not text.strip():
            return jsonify({
                'error': 'Invalid text',
                'message': 'Text must be a non-empty string'
            }), 400
        
        # Analyze with trained model
        result = analyzer.predict_sentiment(text)
        
        if result is None:
            return jsonify({
                'error': 'Analysis failed',
                'message': 'Could not analyze text. Check if model is loaded.'
            }), 500
        
        # Add metadata
        result['api_version'] = '1.0'
        result['timestamp'] = datetime.now().isoformat()
        result['model_file'] = 'vietnamese_sentiment_model.pkl'
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in analyze_sentiment: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    try:
        return jsonify({
            'api_status': 'running',
            'model_loaded': analyzer.is_loaded,
            'model_path': MODEL_PATH,
            'model_type': type(analyzer.model).__name__ if analyzer.is_loaded else None,
            'classes': list(analyzer.model.classes_) if analyzer.is_loaded else None,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch', methods=['POST'])
def batch_analyze():
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({
                'error': 'Missing texts field',
                'message': 'Please provide: {"texts": ["text1", "text2"]}'
            }), 400
        
        texts = data['texts']
        
        if not isinstance(texts, list) or len(texts) > 100:
            return jsonify({
                'error': 'Invalid texts',
                'message': 'texts must be a list with max 100 items'
            }), 400
        
        results = []
        for i, text in enumerate(texts):
            if isinstance(text, str) and text.strip():
                result = analyzer.predict_sentiment(text)
                if result:
                    result['index'] = i
                    results.append(result)
                else:
                    results.append({'index': i, 'error': 'Analysis failed', 'text': text})
            else:
                results.append({'index': i, 'error': 'Invalid text', 'text': text})
        
        return jsonify({
            'results': results,
            'total_processed': len(results),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    print("🚀 Vietnamese Sentiment Analysis API")
    print("=" * 50)
    
    if not analyzer.is_loaded:
        print("❌ CRITICAL: Model could not be loaded!")
        print(f"Model path: {MODEL_PATH}")
        return
    
    print("✅ Model loaded successfully!")
    print(f"Model type: {type(analyzer.model).__name__}")
    print(f"Classes: {', '.join(analyzer.model.classes_)}")
    print(f"URL: http://localhost:5001")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)

if __name__ == '__main__':
    main()