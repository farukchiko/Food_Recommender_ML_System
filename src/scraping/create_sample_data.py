import pandas as pd
import numpy as np
import random

def create_sample_malang_restaurants():
    """Buat sample dataset restoran Malang untuk testing ML"""
    
    print("🚀 Creating sample Malang restaurant data for testing...")
    
    # Restoran populer di Malang (data real berdasarkan knowledge)
    real_restaurants = [
        # Kota Malang
        {"name": "Bakso President", "rating": 4.5, "review_count": 1280, "categories": "Bakso, Indonesian", "address": "Jl. Pandanaran 12, Kota Malang", "latitude": -7.9666, "longitude": 112.6326, "area": "Kota Malang"},
        {"name": "Warung Soto Pak Sadi", "rating": 4.3, "review_count": 890, "categories": "Soto, Indonesian", "address": "Jl. Basuki Rahmat 45, Kota Malang", "latitude": -7.9680, "longitude": 112.6300, "area": "Kota Malang"},
        {"name": "Cafe Toko Oen", "rating": 4.4, "review_count": 1100, "categories": "Dutch, Cafe", "address": "Jl. Basuki Rahmat 5, Kota Malang", "latitude": -7.9670, "longitude": 112.6310, "area": "Kota Malang"},
        {"name": "Rumah Makan Lemburu", "rating": 4.2, "review_count": 760, "categories": "Sunda, Indonesian", "address": "Jl. Letjen S. Parman 23, Kota Malang", "latitude": -7.9650, "longitude": 112.6280, "area": "Kota Malang"},
        
        # Batu
        {"name": "Restoran Apung Selecta", "rating": 4.7, "review_count": 2100, "categories": "Indonesian, International", "address": "Jl. Raya Selecta, Batu", "latitude": -7.8612, "longitude": 112.5243, "area": "Batu"},
        {"name": "Bakso President Batu", "rating": 4.4, "review_count": 870, "categories": "Bakso, Indonesian", "address": "Jl. Panglima Sudirman, Batu", "latitude": -7.8671, "longitude": 112.5251, "area": "Batu"},
        
        # Singosari
        {"name": "Sate Ayam Pak Dullah", "rating": 4.6, "review_count": 980, "categories": "Sate, Indonesian", "address": "Jl. Raya Singosari, Malang", "latitude": -7.8924, "longitude": 112.6655, "area": "Singosari"},
        
        # Area Kampus
        {"name": "Warung Steak dan Shake UB", "rating": 4.2, "review_count": 540, "categories": "Western, Steak", "address": "Jl. Veteran, Ketawanggede", "latitude": -7.9519, "longitude": 112.6154, "area": "Lowokwaru"},
        {"name": "Mie Ayam Pak Man", "rating": 4.3, "review_count": 670, "categories": "Mie Ayam, Indonesian", "address": "Jl. Sawojajar, Malang", "latitude": -7.9800, "longitude": 112.6500, "area": "Blimbing"},
    ]
    
    # Tambahkan lebih banyak variasi restoran
    restaurant_types = [
        "Bakso", "Soto", "Sate", "Pecel Lele", "Mie Ayam", "Nasi Goreng", 
        "Seafood", "Sunda", "Jawa", "Chinese", "Western", "Cafe", "Fast Food"
    ]
    
    areas_malang = {
        "Kota Malang": {"center": (-7.9666, 112.6326), "radius": 0.02},
        "Batu": {"center": (-7.8671, 112.5251), "radius": 0.03},
        "Singosari": {"center": (-7.8924, 112.6655), "radius": 0.02},
        "Kepanjen": {"center": (-8.1305, 112.5722), "radius": 0.02},
        "Blimbing": {"center": (-7.9478, 112.6380), "radius": 0.015},
        "Lowokwaru": {"center": (-7.9477, 112.6150), "radius": 0.015},
    }
    
    np.random.seed(42)  # Untuk hasil konsisten
    
    additional_restaurants = []
    for i in range(50):  # Tambahkan 50 restoran random
        area_name = np.random.choice(list(areas_malang.keys()))
        area = areas_malang[area_name]
        
        # Generate random coordinates around area center
        lat = area["center"][0] + np.random.uniform(-area["radius"], area["radius"])
        lon = area["center"][1] + np.random.uniform(-area["radius"], area["radius"])
        
        restaurant_type = np.random.choice(restaurant_types)
        owner_name = np.random.choice(['Cak', 'Pak', 'Bu', 'Warung'])
        
        additional_restaurants.append({
            "name": f"{restaurant_type} {owner_name} {np.random.choice(['Malang', 'Batu', 'Jaya', 'Enak'])}",
            "rating": round(np.random.uniform(3.5, 4.9), 1),
            "review_count": np.random.randint(50, 1500),
            "categories": f"{restaurant_type}, Indonesian",
            "address": f"Jl. {np.random.choice(['Veteran', 'Basuki Rahmat', 'Pandanaran', 'Sawojajar'])}, {area_name}",
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "area": area_name
        })
    
    # Gabungkan semua data
    all_restaurants = real_restaurants + additional_restaurants
    
    # Convert to DataFrame
    df = pd.DataFrame(all_restaurants)
    
    # Simpan ke CSV
    df.to_csv('data/raw/malang_restaurants_real.csv', index=False)
    
    print(f"✅ Created sample dataset with {len(df)} restaurants")
    print("📊 Dataset Overview:")
    print(f"   - Average rating: {df['rating'].mean():.2f}")
    print(f"   - Total reviews: {df['review_count'].sum()}")
    print(f"   - Areas covered: {df['area'].nunique()}")
    
    # Show sample
    print("\n🍽️  SAMPLE RESTAURANTS:")
    for i, (_, row) in enumerate(df.head(8).iterrows(), 1):
        print(f"{i}. {row['name']} | ⭐{row['rating']} | 📍{row['area']}")
    
    return df

if __name__ == "__main__":
    create_sample_malang_restaurants()