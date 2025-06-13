# Plagiarism Detection

An AI-powered plagiarism detection web application that leverages BERT embeddings and machine learning to analyze and detect content plagiarism in text datasets.

## Features

- Upload CSV files containing original and suspect text pairs.
- Uses Sentence-BERT (SBERT) embeddings for semantic similarity.
- Machine learning classifier (Logistic Regression) for plagiarism prediction.
- Interactive frontend with adjustable similarity threshold.
- Displays similarity scores, predictions, and evaluation metrics.
- Export results as JSON.

## Tech Stack

### Frontend

- **React** (with Vite)
- **Axios** (HTTP requests)
- **lucide-react** (icons)
- **PapaParse** (CSV parsing)
- **ESLint** (linting)
- **CSS Modules** (custom styles)

### Backend

- **Flask** (REST API)
- **Flask-CORS** (CORS support)
- **pandas** (data processing)
- **scikit-learn** (cosine similarity, logistic regression)
- **sentence-transformers** (BERT embeddings)
- **joblib** (model persistence)
- **numpy** (numerical operations)

## Getting Started

### Prerequisites

- Node.js (for frontend)
- Python 3.7+ (for backend)

### Backend Setup

1. Navigate to the `backend` directory:
    ```sh
    cd backend
    ```
2. Install Python dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Install `sentence-transformers`:
    ```sh
    pip install sentence-transformers
    ```
4. Start the Flask server:
    ```sh
    python app.py
    ```
    The backend will run at `http://127.0.0.1:5000`.

### Frontend Setup

1. Navigate to the `frontend` directory:
    ```sh
    cd frontend
    ```
2. Install Node.js dependencies:
    ```sh
    npm install
    ```
3. Start the development server:
    ```sh
    npm run dev
    ```
    The frontend will run at `http://localhost:5173` by default.

## Usage

1. Open the frontend in your browser.
2. Upload a CSV file with columns: `Original`, `Suspect`, and optionally `Label`.
3. Adjust the similarity threshold if needed.
4. Click "Analyze for Plagiarism".
5. View results, metrics, and export as JSON.

## Sample Dataset

You can download a sample CSV dataset to test the plagiarism detection system:

[Download suspect_dataset.csv](./backend/suspect_dataset.csv)

## Example CSV Format

```csv
Original,Suspect,Label
"This is the original text.","This is a copied text.","Plagiarized"
"Another example.","Completely different.","Original"
```

## License

This project is for educational purposes.

---

**Developed with ❤️ using React, Flask, and BERT.**