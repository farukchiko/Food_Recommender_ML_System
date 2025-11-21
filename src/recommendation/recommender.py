import pandas as pd
import numpy as np
import pickle
import os
from geopy.distance import geodesic
from sklearn.preprocessing import StandardScaler

class MalangFoodRecommender:
    def __init__(self):
        self.df = None
        self.knn_model = None
        self.scaler = None
        self.load_models()
    
    def load_models(self):
        """Load model ML yang sudah ditraining"""
        try:
            # Load processed data
            self.df = pd.read_csv('data/processed/malang_restaurants_ml_ready.csv')
            
            # Load KNN model
            with open('data/models/knn_model.pkl', 'rb') as f:
                self.knn_model = pickle.load(f)
            
            # Load scaler
            with open('data/models/scaler.pkl', 'rb') as f:
                self.scaler = pickle.load(f)
                
            print("✅ AI System loaded successfully!")
            print(f"   - Restaurants: {len(self.df)}")
            print(f"   - Model: K-Nearest Neighbors")
            
        except Exception as e:
            print(f"❌ Error loading AI system: {e}")
            print("💡 Pastikan sudah run: python src/training/ml_trainer.py")
    
    def get_recommendations(self, user_lat: float, user_lon: float, top_k: int = 10, max_distance_km: float = 25):
        """Dapatkan rekomendasi menggunakan model ML"""
        if self.knn_model is None or self.df is None:
            return []
        
        # Prepare user features
        user_features = np.array([[user_lat, user_lon, 4.0, 100, 1.0, 0.8]])
        user_features_scaled = self.scaler.transform(user_features)
        
        # Cari restoran terdekat menggunakan KNN
        distances, indices = self.knn_model.kneighbors(user_features_scaled)
        
        recommendations = []
        
        for i, idx in enumerate(indices[0]):
            restaurant = self.df.iloc[idx]
            
            # Hitung jarak sebenarnya
            actual_distance = geodesic(
                (user_lat, user_lon),
                (restaurant['latitude'], restaurant['longitude'])
            ).kilometers
            
            if actual_distance <= max_distance_km:
                recommendation = {
                    'name': restaurant['name'],
                    'rating': restaurant['rating'],
                    'review_count': restaurant['review_count'],
                    'distance_km': round(actual_distance, 2),
                    'address': restaurant.get('address', 'Malang'),
                    'area': restaurant.get('area', 'Malang'),
                    'cuisine': restaurant.get('cuisine', 'Indonesian'),
                    'weighted_score': round(restaurant['weighted_score'], 3),
                    'popularity': restaurant.get('popularity', 0)
                }
                recommendations.append(recommendation)
            
            if len(recommendations) >= top_k:
                break
        
        # Urutkan berdasarkan weighted score (AI score)
        recommendations.sort(key=lambda x: x['weighted_score'], reverse=True)
        
        return recommendations
    
    def recommend_by_place_name(self, place_name: str, top_k: int = 10):
        """Rekomendasi berdasarkan nama tempat (user-friendly)"""
        from src.utils.gps_helper import GPSHelper
        
        # Convert nama tempat ke koordinat
        gps_helper = GPSHelper()
        lat, lon = gps_helper.get_coordinates_from_place(place_name)
        
        if lat is None or lon is None:
            print(f"❌ Tidak bisa menemukan lokasi: {place_name}")
            return []
        
        print(f"📍 Lokasi: {place_name} ({lat:.4f}, {lon:.4f})")
        print("🤖 AI sedang mencari rekomendasi terbaik...")
        
        # Dapatkan rekomendasi
        recommendations = self.get_recommendations(lat, lon, top_k)
        
        return recommendations

def test_recommender():
    """Test sistem rekomendasi"""
    recommender = MalangFoodRecommender()
    
    # Test beberapa tempat
    test_places = ["Kota Malang", "Batu", "Singosari", "UB Malang"]
    
    for place in test_places:
        print(f"\n🎯 TEST: {place}")
        print("=" * 40)
        
        recommendations = recommender.recommend_by_place_name(place, top_k=3)
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec['name']}")
                print(f"   ⭐ {rec['rating']} | 📍 {rec['distance_km']}km | 🍽️ {rec['cuisine']}")
        else:
            print("❌ Tidak ada rekomendasi")
        
        print()

if __name__ == "__main__":
    test_recommender()