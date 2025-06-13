
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
from sentence_transformers import SentenceTransformer
import numpy as np
import joblib
import os

app = Flask(__name__)
CORS(app)
 
sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
 
MODEL_PATH = "logreg_model.pkl"

if not os.path.exists(MODEL_PATH):
    dummy_X = np.array([[0.1], [0.9], [0.5], [0.8]])
    dummy_y = [0, 1, 0, 1]
    clf = LogisticRegression()
    clf.fit(dummy_X, dummy_y)
    joblib.dump(clf, MODEL_PATH)

clf = joblib.load(MODEL_PATH)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        df = pd.read_csv(file)
 
        threshold = float(request.args.get('threshold', 0.7))

        if 'Original' not in df.columns or 'Suspect' not in df.columns:
            return jsonify({'error': "CSV must contain 'Original' and 'Suspect' columns"}), 400
 
        emb1 = sbert_model.encode(df['Original'].astype(str).tolist())
        emb2 = sbert_model.encode(df['Suspect'].astype(str).tolist())
        cosine_scores = [cosine_similarity([e1], [e2])[0][0] for e1, e2 in zip(emb1, emb2)]

        df['cosine_similarity'] = cosine_scores
 
        predictions = [1 if score >= threshold else 0 for score in cosine_scores]
        df['prediction'] = predictions
 
        report = {}
        if 'Label' in df.columns:
            actual = [1 if str(lbl).strip().lower() == 'plagiarized' else 0 for lbl in df['Label']]
            pred = predictions

            tp = sum(1 for a, p in zip(actual, pred) if a == p == 1)
            fp = sum(1 for a, p in zip(actual, pred) if a == 0 and p == 1)
            tn = sum(1 for a, p in zip(actual, pred) if a == p == 0)
            fn = sum(1 for a, p in zip(actual, pred) if a == 1 and p == 0)

            accuracy = (tp + tn) / len(actual) if len(actual) > 0 else 0
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            report = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1
            }

        return jsonify({
            'similarity_scores': [float(score) for score in cosine_scores],
            'predictions': predictions,
            'report': report,
            'file_name': file.filename,
            'threshold': threshold
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

