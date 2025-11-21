import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pickle
import json
import os

class MLTrainer:
    def __init__(self):
        self.knn_model = None
        self.scaler = StandardScaler()
        
    def load_data(self, file_path: str):
        """Load data restoran"""
        print("📁 Memuat data restoran...")
        df = pd.read_csv(file_path)
        print(f"✅ Data loaded: {len(df)} restoran")
        return df
    
    def preprocess_data(self, df):
        """Preprocessing data untuk ML"""
        print("🔧 Preprocessing data...")
        
        # Hapus data yang tidak valid
        df = df.dropna(subset=['latitude', 'longitude', 'rating', 'review_count'])
        
        # Feature engineering
        df['popularity'] = np.log1p(df['review_count'])  # Log transform untuk review count
        df['quality_score'] = df['rating'] / 5.0  # Normalize rating
        
        # Hitung weighted score (kombinasi rating dan popularity)
        df['weighted_score'] = 0.7 * df['rating'] + 0.3 * (df['popularity'] / df['popularity'].max() * 5)
        
        print("✅ Feature engineering completed")
        return df
    
    def preprocess_excel_data(self, df):
        """Preprocessing khusus untuk data dari Excel"""
        print("🔧 Preprocessing Excel data...")
        
        # Handle missing values
        df = df.dropna(subset=['name', 'latitude', 'longitude'])
        
        # Fill missing ratings dengan reasonable values
        if 'rating' in df.columns:
            df['rating'] = df['rating'].fillna(3.8)  # Default rating
        else:
            df['rating'] = 3.8  # Add rating column jika tidak ada
        
        # Fill missing review counts
        if 'review_count' in df.columns:
            df['review_count'] = df['review_count'].fillna(100)
        else:
            df['review_count'] = 100  # Add review_count jika tidak ada
        
        # Feature engineering (sama seperti sebelumnya)
        df['popularity'] = np.log1p(df['review_count'])
        df['quality_score'] = df['rating'] / 5.0
        df['weighted_score'] = 0.7 * df['rating'] + 0.3 * (df['popularity'] / df['popularity'].max() * 5)
        
        print("✅ Excel data preprocessing completed")
        return df
    
    def prepare_features(self, df):
        """Siapkan features untuk training ML"""
        features = df[['latitude', 'longitude', 'rating', 'review_count', 'popularity', 'weighted_score']].values
        
        print("🤖 Menyiapkan features untuk Machine Learning...")
        print(f"   - Dimensi features: {features.shape}")
        print(f"   - Fitur: latitude, longitude, rating, review_count, popularity, weighted_score")
        
        return features
    
    def train_knn_model(self, features, n_neighbors=20):
        """Train K-Nearest Neighbors model"""
        print("🧠 Training K-Nearest Neighbors Model...")
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Train KNN model
        self.knn_model = NearestNeighbors(
            n_neighbors=min(n_neighbors, len(features)),
            metric='euclidean',
            algorithm='auto'
        )
        self.knn_model.fit(features_scaled)
        
        print(f"✅ KNN Model trained dengan {len(features)} samples")
        return self.knn_model
    
    def save_models(self, model_dir='data/models/'):
        """Save model dan scaler"""
        os.makedirs(model_dir, exist_ok=True)
        
        # Save KNN model
        with open(os.path.join(model_dir, 'knn_model.pkl'), 'wb') as f:
            pickle.dump(self.knn_model, f)
        
        # Save scaler
        with open(os.path.join(model_dir, 'scaler.pkl'), 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # Save model info
        model_info = {
            'model_type': 'K-Nearest Neighbors',
            'trained_samples': len(self.knn_model._fit_X),
            'n_neighbors': self.knn_model.n_neighbors,
            'metric': 'euclidean',
            'features': ['latitude', 'longitude', 'rating', 'review_count', 'popularity', 'weighted_score']
        }
        
        with open(os.path.join(model_dir, 'model_info.json'), 'w') as f:
            json.dump(model_info, f, indent=2)
        
        print("💾 Model ML berhasil disimpan")
    
    def detect_data_source(self, df):
        """Detect sumber data untuk pilih preprocessing yang tepat"""
        if 'source' in df.columns:
            source_type = df['source'].iloc[0] if len(df) > 0 else 'unknown'
            print(f"📊 Data source detected: {source_type}")
            return source_type
        else:
            print("📊 Data source: unknown (using standard preprocessing)")
            return 'standard'
    
    def train_complete_pipeline(self, data_path: str):
        """Complete ML training pipeline"""
        print("=" * 50)
        print("🚀 MACHINE LEARNING TRAINING PIPELINE")
        print("=" * 50)
        
        # 1. Load data
        df = self.load_data(data_path)
        
        # 2. Detect data source dan pilih preprocessing
        data_source = self.detect_data_source(df)
        
        if data_source == 'excel_import':
            df_processed = self.preprocess_excel_data(df)
        else:
            df_processed = self.preprocess_data(df)
        
        # 3. Prepare features
        features = self.prepare_features(df_processed)
        
        # 4. Train model
        self.train_knn_model(features)
        
        # 5. Save models
        self.save_models()
        
        # 6. Save processed data
        df_processed.to_csv('data/processed/malang_restaurants_ml_ready.csv', index=False)
        
        print("\n🎉 TRAINING BERHASIL!")
        print("📊 Model Summary:")
        print(f"   - Training samples: {len(features)}")
        print(f"   - Features: {features.shape[1]} dimensi")
        print(f"   - Algorithm: K-Nearest Neighbors")
        print(f"   - Neighbors: {self.knn_model.n_neighbors}")
        print(f"   - Data source: {data_source}")
        
        return df_processed

def main():
    """Main function untuk training ML"""
    trainer = MLTrainer()
    
    # Otomatis detect file yang ada
    data_files = [
        'data/raw/malang_restaurants_real.csv',  # Prioritas 1: Excel converted
        'data/raw/malang_restaurants_google.csv', # Prioritas 2: Google Maps
        'data/raw/malang_restaurants_osm.csv'     # Prioritas 3: OpenStreetMap
    ]
    
    data_path = None
    for file_path in data_files:
        if os.path.exists(file_path):
            data_path = file_path
            print(f"📁 Using data file: {file_path}")
            break
    
    if data_path is None:
        print("❌ No data file found! Please run one of:")
        print("   - python src/utils/excel_to_csv.py (for Excel data)")
        print("   - python src/scraping/openstreetmap_malang.py (for web scraping)")
        print("   - python src/scraping/create_sample_data.py (for sample data)")
        return
    
    # Jalankan training pipeline
    trainer.train_complete_pipeline(data_path)

if __name__ == "__main__":
    main()