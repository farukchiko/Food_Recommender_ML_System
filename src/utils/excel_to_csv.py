import pandas as pd
import os

def convert_excel_to_csv(excel_file_path: str, output_csv_path: str):
    """
    Convert Excel file to CSV format yang compatible dengan sistem kita
    """
    print(f"📂 Loading Excel file: {excel_file_path}")
    
    try:
        # Read Excel file
        df = pd.read_excel(excel_file_path)
        print(f"✅ Excel loaded: {len(df)} rows, {len(df.columns)} columns")
        print(f"📊 Columns: {list(df.columns)}")
        
        # Standardize column names (case insensitive)
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower()
            if 'nama' in col_lower or 'name' in col_lower:
                column_mapping[col] = 'name'
            elif 'rating' in col_lower:
                column_mapping[col] = 'rating'
            elif 'review' in col_lower or 'ulasan' in col_lower:
                column_mapping[col] = 'review_count'
            elif 'alamat' in col_lower or 'address' in col_lower:
                column_mapping[col] = 'address'
            elif 'latitude' in col_lower or 'lat' in col_lower:
                column_mapping[col] = 'latitude'
            elif 'longitude' in col_lower or 'lon' in col_lower or 'lng' in col_lower:
                column_mapping[col] = 'longitude'
            elif 'kategori' in col_lower or 'category' in col_lower or 'jenis' in col_lower:
                column_mapping[col] = 'categories'
            elif 'area' in col_lower or 'wilayah' in col_lower:
                column_mapping[col] = 'area'
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        print(f"🔧 Columns renamed: {list(df.columns)}")
        
        # Add missing columns if necessary
        if 'categories' not in df.columns:
            df['categories'] = 'Indonesian'
            print("➕ Added default 'categories' column")
        
        if 'area' not in df.columns:
            df['area'] = 'Malang'
            print("➕ Added default 'area' column")
        
        if 'source' not in df.columns:
            df['source'] = 'excel_import'
            print("➕ Added 'source' column")
        
        # Ensure numeric columns
        if 'rating' in df.columns:
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        
        if 'review_count' in df.columns:
            df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')
        
        # Save to CSV
        df.to_csv(output_csv_path, index=False, encoding='utf-8')
        print(f"💾 CSV saved: {output_csv_path}")
        print(f"📊 Final data: {len(df)} restaurants")
        
        # Show sample
        print("\n🍽️  SAMPLE DATA:")
        print(df[['name', 'rating', 'address']].head().to_string())
        
        return df
        
    except Exception as e:
        print(f"❌ Error converting Excel: {e}")
        return None

def main():
    # Ganti dengan path Excel file Anda
    excel_file = "data/raw/restoran_malang.xlsx"  # atau .xls
    output_file = "data/raw/malang_restaurants_real.csv"
    
    # Create directory if not exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    df = convert_excel_to_csv(excel_file, output_file)
    
    if df is not None:
        print("\n🎉 CONVERSION SUCCESSFUL!")
        print("➡️  Now run: python src/training/ml_trainer.py")
    else:
        print("\n❌ CONVERSION FAILED!")

if __name__ == "__main__":
    main()