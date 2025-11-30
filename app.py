from flask import Flask, render_template, request, jsonify
import pickle
import joblib
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from src.load_models import load_lstm
from src.text_preprocessing import preprocess_text
import os

app = Flask(__name__)

# Load pre-trained LSTM model and tokenizer
# Ensure we are in the correct directory or use absolute paths if needed.
# Assuming run from the project root.
try:
    model = load_lstm()
    # loaded_cv = joblib.load('./count_vectorizer.pkl') # Not used in LSTM path in original code, but kept if needed later
    tokenizer = pickle.load(open('./tokenizer.pkl', 'rb'))
    print("Models loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")

def classify_sentiment_text_lstm(text, model, tokenizer, max_len=900):
    sent_dict = {
        "0": "negative",
        "1": "neutral",
        "2": "positive"
    }
    text_sequence = tokenizer.texts_to_sequences([text])
    encoded_text = pad_sequences(text_sequence, maxlen=max_len)
    predictions = model.predict(encoded_text, verbose=0)
    prediction = np.argmax(predictions, axis=1)[0]
    sentiment = sent_dict[str(prediction)]
    sentiment_probabilities = {
        "negative": float(predictions[0][0]),
        "neutral": float(predictions[0][1]),
        "positive": float(predictions[0][2])
    }
    return sentiment, sentiment_probabilities

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'Please enter some text.'}), 400
            
        preprocessed_text = preprocess_text(text)
        sentiment, probs = classify_sentiment_text_lstm(preprocessed_text, model, tokenizer)
        
        return jsonify({
            'sentiment': sentiment,
            'probabilities': probs
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

