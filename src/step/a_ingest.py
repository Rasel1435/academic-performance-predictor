import os
import sys
import pandas as pd
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DATA_SOURCE
from error_logs import configure_logger
logger = configure_logger()


def ingest_data(DATA_SOURCE: str) -> pd.DataFrame:
    """
    Ingests the raw CSV data from the source path defined in config.
    """
    try:
        logger.info("==> Starting data ingestion process...")
        # Convert string path to Path object for robust checking
        data_path = Path(DATA_SOURCE)

        if not data_path.exists():
            logger.error(f"Data file not found at: {data_path}")
            raise FileNotFoundError(f"Missing input data: {data_path}")
        
        # Loading Process
        df = pd.read_csv(data_path)

        # Ingestion Summary
        summary = (
            f"\n{'='*30}\n"
            f"DATA INGESTION REPORT\n"
            f"{'='*30}\n"
            f"Source: {data_path.name}\n"
            f"Rows: {df.shape[0]} | Columns: {df.shape[1]}\n"
            f"File Integrity: {'PASS' if not df.empty else 'FAIL'}\n"
            f"Columns Found: {df.columns.tolist()[:5]}... (Total {len(df.columns)})\n"
            f"{'='*30}"
        )
        logger.info(summary)
        logger.info("==> Data ingestion process completed successfully.\n\n")
        return df

    except Exception as e:
        logger.error(f"==> Unexpected error during ingestion: {e}")
        raise


# ------------------------------------------
# For local testing of the ingestion step
# ------------------------------------------
"""
if __name__ == '__main__':
    df = ingest_data(DATA_SOURCE=DATA_SOURCE)
    print("Ingestion completed.")
    print(df.head())
    print(f"Data shape: {df.shape}" if df is not None else "Ingestion failed.")
"""

# Run: python -m src.step.a_ingest