from src.recommendation.recommender import MalangFoodRecommender
from src.utils.gps_helper import MALANG_PLACES

def main():
    print("🍽️" * 20)
    print("🤖 AI FOOD RECOMMENDATION SYSTEM - MALANG")
    print("🍽️" * 20)
    print("\nSelamat datang! Sistem AI ini akan merekomendasikan")
    print("restoran terbaik di Malang berdasarkan lokasi Anda.")
    
    # Initialize AI system
    recommender = MalangFoodRecommender()
    
    if recommender.df is None:
        print("\n❌ Sistem belum siap. Silakan run setup terlebih dahulu:")
        print("   1. python src/scraping/openstreetmap_malang.py")
        print("   2. python src/training/ml_trainer.py")
        return
    
    while True:
        print("\n" + "="*50)
        print("📍 PILIHAN INPUT LOKASI:")
        print("="*50)
        print("1. 🏠 Masukkan nama tempat di Malang")
        print("2. 📋 Lihat daftar tempat yang tersedia") 
        print("3. 🚪 Keluar")
        
        choice = input("\nPilih opsi (1-3): ").strip()
        
        if choice == '1':
            # Input nama tempat
            place_name = input("\nMasukkan nama tempat di Malang: ").strip()
            
            if not place_name:
                print("❌ Nama tempat tidak boleh kosong!")
                continue
            
            try:
                top_k = int(input("Jumlah rekomendasi (default 5): ") or "5")
            except:
                top_k = 5
            
            # Dapatkan rekomendasi dari AI
            recommendations = recommender.recommend_by_place_name(place_name, top_k)
            
            if recommendations:
                print(f"\n🎯 REKOMENDASI AI UNTUK {place_name.upper()}:")
                print("=" * 60)
                
                for i, rec in enumerate(recommendations, 1):
                    print(f"\n{i}. 🏷️  {rec['name']}")
                    print(f"   ⭐ Rating: {rec['rating']}/5")
                    print(f"   📍 Jarak: {rec['distance_km']} km dari lokasi Anda")
                    print(f"   👥 Review: {rec['review_count']} reviews")
                    print(f"   🍽️  Tipe: {rec['cuisine']}")
                    print(f"   🗺️  Area: {rec['area']}")
                    print(f"   📍 Alamat: {rec['address']}")
                    print(f"   💯 AI Score: {rec['weighted_score']:.3f}")
                    print("-" * 50)
            else:
                print(f"❌ Tidak ada rekomendasi untuk {place_name}")
                print("💡 Coba tempat lain seperti: 'Kota Malang', 'Batu', 'Singosari'")
        
        elif choice == '2':
            # Tampilkan daftar tempat yang tersedia
            print("\n📋 DAFTAR TEMPAT DI MALANG:")
            print("=" * 30)
            for i, (key, desc) in enumerate(MALANG_PLACES.items(), 1):
                print(f"{i}. {key} - {desc}")
        
        elif choice == '3':
            print("\n👋 Terima kasih telah menggunakan AI Food Recommendation!")
            print("Selamat menikmati kuliner Malang! 🍽️")
            break
        
        else:
            print("❌ Pilihan tidak valid! Silakan pilih 1, 2, atau 3.")

if __name__ == "__main__":
    main()