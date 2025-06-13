# from flask import Flask, request, jsonify
# from flask_cors import CORS   
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# app = Flask(__name__)
# CORS(app)  

# def compute_cosine_similarity(text1, text2):
#     vectorizer = CountVectorizer(stop_words='english')
#     vectors = vectorizer.fit_transform([text1, text2])
#     return cosine_similarity(vectors[0], vectors[1])[0][0]

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     try:
#         file = request.files['file']
#         threshold = float(request.form['threshold'])
#         df = pd.read_csv(file)

#         similarity_scores = []
#         predictions = []
#         for index, row in df.iterrows():
#             score = compute_cosine_similarity(row['Original'], row['Suspect'])
#             similarity_scores.append(score)
#             predictions.append(1 if score > threshold else 0)

#         actual_labels = [1 if label.lower() == 'plagiarized' else 0 for label in df['Label']]

#         # Calculate metrics
#         true_positives = sum(1 for a, p in zip(actual_labels, predictions) if a == p == 1)
#         false_positives = sum(1 for a, p in zip(actual_labels, predictions) if a == 0 and p == 1)
#         true_negatives = sum(1 for a, p in zip(actual_labels, predictions) if a == p == 0)
#         false_negatives = sum(1 for a, p in zip(actual_labels, predictions) if a == 1 and p == 0)

#         accuracy = (true_positives + true_negatives) / len(actual_labels)
#         precision = true_positives / (true_positives + false_positives) if true_positives + false_positives > 0 else 0
#         recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives > 0 else 0
#         f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

#         report = {
#             'accuracy': accuracy,
#             'precision': precision,
#             'recall': recall,
#             'f1_score': f1_score
#         }

#         return jsonify({
#             'similarity_scores': similarity_scores,
#             'predictions': predictions,
#             'report': report,
#             'file_name': file.filename,
#             'threshold': threshold
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# if __name__ == '__main__':
#     app.run(debug=True)


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

# Load Sentence-BERT model
sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load or train Logistic Regression model
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

        # Get threshold from query param or default
        threshold = float(request.args.get('threshold', 0.7))

        if 'Original' not in df.columns or 'Suspect' not in df.columns:
            return jsonify({'error': "CSV must contain 'Original' and 'Suspect' columns"}), 400

        # Generate embeddings and compute cosine similarity
        emb1 = sbert_model.encode(df['Original'].astype(str).tolist())
        emb2 = sbert_model.encode(df['Suspect'].astype(str).tolist())
        cosine_scores = [cosine_similarity([e1], [e2])[0][0] for e1, e2 in zip(emb1, emb2)]

        df['cosine_similarity'] = cosine_scores

        # Use threshold to classify
        predictions = [1 if score >= threshold else 0 for score in cosine_scores]
        df['prediction'] = predictions

        # Evaluation metrics if 'Label' is present
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

