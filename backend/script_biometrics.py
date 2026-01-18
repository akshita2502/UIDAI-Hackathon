import pandas as pd
import os
from datetime import datetime
from typing import cast
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, BiometricData

def populate_biometric_data(csv_file_path: str, append_mode: bool = True):
    """
    Reads a CSV file and populates the BiometricData table.
    
    Args:
        csv_file_path: Path to the CSV file
        append_mode: If True, appends new records. If False, replaces all data.
    
    CSV Columns Expected:
        - date (YYYY-MM-DD format)
        - state
        - district
        - pincode
        - bio_age_5_17
        - bio_age_17_
    """
    
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file not found at {csv_file_path}")
        return False
    
    try:
        # Read CSV file
        print(f"Reading CSV file: {csv_file_path}")
        df = pd.read_csv(csv_file_path)
        
        # Validate required columns
        required_columns = ['date', 'state', 'district', 'pincode', 'bio_age_5_17', 'bio_age_17_']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Error: Missing columns in CSV: {missing_columns}")
            return False
        
        # Convert date column to datetime (handle DD-MM-YYYY format)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', dayfirst=True).dt.date
        
        # Create session
        db: Session = SessionLocal()
        
        try:
            # If not in append mode, clear existing data
            if not append_mode:
                print("Clearing existing BiometricData records...")
                db.query(BiometricData).delete()
                db.commit()
            
            # Track statistics
            inserted = 0
            skipped = 0
            
            # Iterate through dataframe rows
            for index, row in df.iterrows():
                try:
                    # Check if record with same date, state, district, pincode exists
                    existing_record = db.query(BiometricData).filter(
                        BiometricData.date == row['date'],
                        BiometricData.state == row['state'],
                        BiometricData.district == row['district'],
                        BiometricData.pincode == int(row['pincode'])
                    ).first()
                    
                    if existing_record and append_mode:
                        # Update existing record
                        val_5_17 = int(row['bio_age_5_17']) if pd.notna(row['bio_age_5_17']) else 0
                        val_17_plus = int(row['bio_age_17_']) if pd.notna(row['bio_age_17_']) else 0
                        existing_record.bio_age_5_17 = val_5_17  # type: ignore
                        existing_record.bio_age_17_ = val_17_plus  # type: ignore
                        inserted += 1
                    elif not existing_record:
                        # Create new record
                        new_record = BiometricData(
                            date=row['date'],
                            state=str(row['state']).strip(),
                            district=str(row['district']).strip(),
                            pincode=int(row['pincode']),
                            bio_age_5_17=int(row['bio_age_5_17']) if pd.notna(row['bio_age_5_17']) else 0,
                            bio_age_17_=int(row['bio_age_17_']) if pd.notna(row['bio_age_17_']) else 0
                        )
                        db.add(new_record)
                        inserted += 1
                    else:
                        skipped += 1
                
                except Exception as e:
                    print(f"Error processing row {index}: {str(e)}")
                    skipped += 1
                    continue
            
            # Commit all changes
            db.commit()
            
            print(f"\n✓ Data population completed successfully!")
            print(f"  - Records inserted/updated: {inserted}")
            print(f"  - Records skipped: {skipped}")
            print(f"  - Total rows in CSV: {len(df)}")
            
            return True
        
        except Exception as e:
            db.rollback()
            print(f"Error during commit: {str(e)}")
            return False
        
        finally:
            db.close()
    
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return False

def main():
    """
    Main function to run the population script.
    Place your CSV file in the backend directory and update the path below.
    """
    
    # Default CSV file path (place your CSV in the backend folder)
    csv_path = os.path.join(os.path.dirname(__file__), "api_data_aadhar_biometric_0_500000.csv")
    
    # Alternative: You can specify the path directly
    # csv_path = "c:/path/to/your/file.csv"
    
    print("=" * 60)
    print("BiometricData Table Population Script")
    print("=" * 60)
    
    # Check if CSV exists at default location
    if not os.path.exists(csv_path):
        print(f"\nCSV file not found at: {csv_path}")
        print("\nUsage:")
        print("  1. Place your CSV file in the backend directory as 'biometric_data.csv'")
        print("  2. Ensure CSV has columns: date, state, district, pincode, bio_age_5_17, bio_age_17_")
        print("  3. Run: python script.py")
        print("\nOr pass a custom path:")
        print("  python script.py <path_to_csv>")
        return
    
    # Run population in append mode (default)
    success = populate_biometric_data(csv_path, append_mode=True)
    
    if success:
        print("\n✓ Script completed successfully!")
    else:
        print("\n✗ Script encountered errors. Please check the output above.")

if __name__ == "__main__":
    import sys
    
    # Allow custom CSV path via command line argument
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        print("=" * 60)
        print("BiometricData Table Population Script")
        print("=" * 60)
        success = populate_biometric_data(csv_file, append_mode=True)
        if success:
            print("\n✓ Script completed successfully!")
        else:
            print("\n✗ Script encountered errors. Please check the output above.")
    else:
        main()
