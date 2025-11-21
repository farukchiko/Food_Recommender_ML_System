from geopy.geocoders import Nominatim
import requests
import time

class GPSHelper:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="malang_food_recommender")
    
    def get_coordinates_from_place(self, place_name: str):
        """
        Convert nama tempat ke koordinat (latitude, longitude)
        Contoh: 'Malang Kota' -> (-7.9666, 112.6326)
        """
        try:
            print(f"📍 Mencari koordinat untuk: {place_name}...")
            
            # Tambahkan 'Malang' jika belum ada untuk spesifik
            if 'malang' not in place_name.lower():
                place_name = f"{place_name}, Malang"
            
            location = self.geolocator.geocode(place_name)
            
            if location:
                print(f"✅ Ditemukan: {location.address}")
                print(f"   Koordinat: ({location.latitude:.4f}, {location.longitude:.4f})")
                return location.latitude, location.longitude
            else:
                print(f"❌ Tidak ditemukan: {place_name}")
                return None, None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None, None
    
    def get_current_location(self):
        """
        Coba dapatkan lokasi saat ini menggunakan IP (fallback)
        """
        try:
            response = requests.get('http://ipinfo.io/json', timeout=5)
            data = response.json()
            
            loc = data['loc'].split(',')
            city = data.get('city', 'Unknown')
            region = data.get('region', '')
            
            print(f"📍 Lokasi terdeteksi: {city}, {region}")
            return float(loc[0]), float(loc[1])
            
        except:
            print("❌ Tidak bisa detect lokasi otomatis")
            return None, None

# Contoh tempat-tempat di Malang yang bisa diinput
MALANG_PLACES = {
    "Kota Malang": "Pusat Kota Malang",
    "Batu": "Kota Batu, Malang", 
    "Singosari": "Singosari, Malang",
    "Kepanjen": "Kepanjen, Malang",
    "Tumpang": "Tumpang, Malang",
    "Pujon": "Pujon, Malang",
    "Dau": "Dau, Malang",
    "Wagir": "Wagir, Malang",
    "Blimbing": "Blimbing, Malang",
    "Klojen": "Klojen, Malang",
    "Lowokwaru": "Lowokwaru, Malang",
    "Sukun": "Sukun, Malang",
    "Kedungkandang": "Kedungkandang, Malang",
    "UB Malang": "Universitas Brawijaya, Malang",
    "UM Malang": "Universitas Negeri Malang",
    "ITN Malang": "ITN Malang",
    "Alun-alun Malang": "Alun-alun Malang",
    "Malang Town Square": "Matos, Malang",
}

def test_gps_helper():
    """Test fungsi GPS helper"""
    helper = GPSHelper()
    
    # Test beberapa tempat
    test_places = ["Kota Malang", "Batu", "Singosari", "UB Malang"]
    
    for place in test_places:
        lat, lon = helper.get_coordinates_from_place(place)
        if lat and lon:
            print(f"✅ {place}: ({lat:.4f}, {lon:.4f})")
        else:
            print(f"❌ Gagal: {place}")
        time.sleep(1)  # Delay untuk menghormati rate limit

if __name__ == "__main__":
    test_gps_helper()