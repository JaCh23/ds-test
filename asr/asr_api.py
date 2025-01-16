import os
import librosa
import torch

from flask import Flask, request, jsonify
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer


app = Flask(__name__)

tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# PING-PONG test
@app.route('/ping', methods=['GET']) 
def ping():
    return "pong"

# Original supporting single processing
@app.route('/asr', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    audio_file = request.files['file']

    # Check if the file is actually a file and not an empty part
    if audio_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    audio, _ = librosa.load(audio_file, sr=16000)
    duration = librosa.get_duration(y=audio, sr=16000)  # Calculate audio duration

    input_values = tokenizer(audio, return_tensors = 'pt').input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim =-1)
    transcript = tokenizer.decode(predicted_ids[0])

    # Create Flask response object 
    response_data = {'transcription': str(transcript), 'duration': str(duration)}
    return jsonify(response_data)

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=8001)
    app.run(host='0.0.0.0', port=8001)
