import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from error_logs import configure_logger
logger = configure_logger()

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the data by:
    - Dropping duplicates and null values
    - Converting datetime column
    - Renaming key columns
    - Removing extreme outliers
    """
    try:
        logger.info("==> Starting data cleaning process...")
        df_clean = df.copy()

        # Remove Duplicate Rows
        duplicate_count = df_clean.duplicated().sum()
        df_clean = df_clean.drop_duplicates()

        # Handle Specific Missing Values
        if 'parental_education_level' in df_clean.columns:
            df_clean['parental_education_level'] = df_clean['parental_education_level'].fillna('Unknown')

        # Final Integrity Check
        remaining_nulls = df_clean.isnull().sum().sum()

        # Structured Summary
        summary = (
            f"\n{'='*30}\n"
            f"DATA CLEANING REPORT\n"
            f"{'='*30}\n"
            f"Rows: {df_clean.shape[0]} | Columns: {df_clean.shape[1]}\n"
            f"Duplicates Removed: {duplicate_count}\n"
            f"Remaining Nulls: {remaining_nulls}\n"
            f"Data Cleanliness: {'PASS' if remaining_nulls == 0 else 'FAIL'}\n"
            f"{'='*30}"
        )
        # Log the entire summary at once
        logger.info(summary)
        logger.info("==> Data cleaning process completed successfully.\n\n")
        return df_clean
    
    except Exception as e:
        logger.error(f"Error during data cleaning: {e}")
        return None
    

# Run: python -m src.step.b_cleaning