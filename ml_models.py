import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
import numpy as np
import pandas as pd
import joblib as jb
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.cluster import KMeans

# Lazy global model load to optimize startup time
_sbert_model = None

def get_sbert_model():
    """
    Singleton getter for the SBERT sentence transformer model.
    Downloads/loads the model only when first required.
    """
    global _sbert_model
    if _sbert_model is None:
        print("Loading SBERT model (all-MiniLM-L6-v2)...")
        _sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _sbert_model

def calculate_similarity(answer: str, explanation: str) -> float:
    """
    Calculates the cosine similarity between the student's answer and the ideal explanation.
    """
    try:
        model = get_sbert_model()
        # Encode answers and explanations
        embeddings = model.encode([answer, explanation])
        # Calculate cosine similarity
        score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return float(max(0.0, min(1.0, score)))
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0

def train_and_save_kmeans(model_path="kmeans_model.joblib"):
    """
    Generates synthetic data and trains the KMeans clustering pipeline,
    then saves it to disk.
    """
    print("Training new KMeans clustering model...")
    np.random.seed(42)
    n_samples = 150
    
    anomalies = ['None', 'Looking Left', 'Looking Right', 'Looking Up', 'Looking Down', 'No Face Detected', 'Phone Detected']
    levels = ['EASY', 'MEDIUM', 'HARD']
    
    data_list = []
    for _ in range(n_samples):
        lvl = np.random.choice(levels)
        anom = np.random.choice(anomalies, p=[0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
        
        # Heuristically set similarity based on anomalies
        if anom == 'None':
            sim = np.random.uniform(0.65, 0.95)
        elif anom == 'Phone Detected':
            sim = np.random.uniform(0.1, 0.4)
        else:
            sim = np.random.uniform(0.35, 0.75)
            
        data_list.append({
            'anamoly': anom,
            'level': lvl,
            'Answer_similarity': sim
        })
        
    df = pd.DataFrame(data_list)
    
    # Establish ColumnTransformer for categorical data mapping
    categories = [anomalies, levels]
    encoder = OrdinalEncoder(categories=categories, handle_unknown='use_encoded_value', unknown_value=-1)
    ct = ColumnTransformer(
        transformers=[("ordenc", encoder, ["anamoly", "level"])],
        remainder='passthrough'
    )
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    pipeline = Pipeline([('ct', ct), ('kmeans', kmeans)])
    
    # Fit KMeans
    pipeline.fit(df)
    
    # Map clusters to top / average / poor based on similarity mean
    df['Cluster'] = pipeline.predict(df)
    means = df.groupby('Cluster')['Answer_similarity'].mean().sort_values(ascending=False)
    
    # Save mapping to pipeline attributes
    pipeline.cluster_mapping_ = {
        means.index[0]: 'top',
        means.index[1]: 'average',
        means.index[2]: 'poor'
    }
    
    jb.dump(pipeline, model_path)
    print(f"KMeans model trained and saved successfully to {model_path}.")
    return pipeline

def get_kmeans_pipeline():
    """
    Retrieves or trains the KMeans clustering pipeline.
    """
    model_path = "kmeans_model.joblib"
    if os.path.exists(model_path):
        try:
            pipeline = jb.load(model_path)
            return pipeline
        except Exception as e:
            print(f"Error loading KMeans model: {e}. Re-training...")
            
    return train_and_save_kmeans(model_path)

def predict_performance_cluster(anomaly: str, level: str, avg_similarity: float) -> str:
    """
    Runs the KMeans pipeline to predict the performance category ('top' | 'average' | 'poor')
    of the candidate.
    """
    try:
        pipeline = get_kmeans_pipeline()
        
        # Standardize categories
        anomalies = ['None', 'Looking Left', 'Looking Right', 'Looking Up', 'Looking Down', 'No Face Detected', 'Phone Detected']
        if anomaly not in anomalies:
            anomaly = 'None'
            
        level_upper = level.upper()
        if level_upper not in ['EASY', 'MEDIUM', 'HARD']:
            level_upper = 'EASY'
            
        pred_df = pd.DataFrame([{
            'anamoly': anomaly,
            'level': level_upper,
            'Answer_similarity': avg_similarity
        }])
        
        cluster_id = pipeline.predict(pred_df)[0]
        mapping = getattr(pipeline, 'cluster_mapping_', {0: 'average', 1: 'top', 2: 'poor'})
        
        return mapping.get(cluster_id, 'average')
    except Exception as e:
        print(f"Error predicting performance cluster: {e}")
        return "average"
