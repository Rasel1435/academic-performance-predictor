from config import DATA_SOURCE
from src.step.a_ingest import ingest_data
from src.step.b_cleaning import clean_data
from src.step.c_feature_engineering import features_engineering
from src.step.d_features_selection import features_selection
from src.step.e_model_training import model_training
from error_logs import configure_logger

logger = configure_logger() 

# ------------------------------------------
# ETL Feature Pipeline
# ------------------------------------------
def run_pipeline():
    """
    Pipeline that runs all ETL / feature steps.
    """
    try:
        logger.info("==> Starting ETL Feature Pipeline...\n")

        # Step 1: Ingest Data
        data = ingest_data(DATA_SOURCE=DATA_SOURCE)
        if data is None:
            logger.error("==> ETL Pipeline aborted: Ingestion failed.")
            return None
        
        # Step 2: Clean Data
        df_clean = clean_data(data)

        # Step 3: Feature Engineering
        df_encoded = features_engineering(df_clean)

        # Step 4: Feature Selection
        df_selection = features_selection(df_encoded)

        # Step 5: Model Training
        model, scaler, metrics = model_training(df_selection)

        logger.info("\n==> ETL Feature Pipeline completed successfully.")
        return model, scaler, metrics

    except Exception as e:
        logger.error(f"Error in ETL Feature Pipeline: {e}")
        return None
    

# ------------------------------------------
# Run ETL Feature Pipeline
# ------------------------------------------
if __name__ == "__main__":
    run_pipeline()




# Run: python -m src.pipeline.ETLFeaturePipeline