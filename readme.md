# 🔍 Plagiarism Detection

A powerful and interactive web-based application for detecting textual plagiarism using SBERT (Sentence-BERT) with cosine similarity, along with machine learning models like Logistic Regression. This project provides detailed performance evaluation using common classification metrics and supports flexible, user-friendly features for in-depth analysis.

## 🚀 Features

- 📁 **File Upload** – Upload CSV files containing original and suspect text pairs for analysis.
- 🧠 **SBERT + Cosine Similarity** – Semantic similarity scoring using transformer-based embeddings.
- 🤖 **ML Integration** – Logistic Regression model for classification and performance comparison.
- 🎯 **Evaluation Metrics** – Automatic computation of Accuracy, Precision, Recall, and F1 Score.
- 🎛️ **Adjustable Threshold** – Tune similarity threshold to control sensitivity of plagiarism detection.
- 📊 **Visual Insights** – Color-coded similarity scores and metric-based feedback.
- 🌗 **Dark/Light Theme** – Toggle UI themes for better accessibility and user preference.
- 📱 **Responsive Design** – Works seamlessly across desktops, tablets, and mobile devices.
- 📤 **Export Results** – Option to export plagiarism analysis for reporting or further study.

## 📂 Input Format

Upload a `.csv` file with the following required columns:

| Column Name | Description                          |
|-------------|--------------------------------------|
| Original    | The original reference text          |
| Suspect     | The text to be checked for plagiarism|
| Label       | Ground truth: Plagiarized/Not Plagiarized (optional) |

**Example:**
```csv
Original,Suspect,Label
"This is the original text.","This is a copied text.","Plagiarized"
"Another example.","Completely different.","Original"
```

## Sample Dataset

You can download a sample CSV dataset to test the plagiarism detection system:

[Download suspect_dataset.csv](./backend/suspect_dataset.csv)

## 🛠️ Tech Stack

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

## 🚦 Getting Started

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

## 💡 Usage

1. Open the frontend in your browser.
2. Upload a CSV file with columns: `Original`, `Suspect`, and optionally `Label`.
3. Adjust the similarity threshold if needed.
4. Click "Analyze for Plagiarism".
5. View results, metrics, and export as JSON.

## 📜 License

This project is for educational purposes.

---

**Developed with ❤️ using React, Flask, and BERT.**
