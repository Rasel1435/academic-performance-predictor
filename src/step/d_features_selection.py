import pandas as pd
from error_logs import configure_logger

logger = configure_logger()


def features_selection(df: pd.DataFrame) -> pd.DataFrame:
    """
    Selects features based on their correlation with the target variable.
    Keeps features with absolute correlation greater than 0.05.
    """
    try:
        logger.info("==> Starting Feature Selection...")
        target = 'exam_score'

        # Get absolute correlation values for the target
        correlations = df.corr()[target].abs()

        # Filter features: Keep those with correlation > 0.05
        # We always keep the target itself!
        selected_features = correlations[correlations > 0.05].index.tolist()

        # Create the final dataframe with only selected columns
        df_final = df[selected_features]

        # Identify what was dropped for the log
        dropped_count = df.shape[1] - df_final.shape[1]

        # 4. Structured Summary Report
        summary = (
            f"\n{'='*30}\n"
            f"FEATURE SELECTION REPORT\n"
            f"{'='*30}\n"
            f"Original Features: {df.shape[1]}\n"
            f"Selected Features: {df_final.shape[1]}\n"
            f"Features Dropped:  {dropped_count}\n"
            f"Target Variable:   {target}\n"
            f"Final Columns:     {df_final.columns.tolist()}\n"
            f"{'='*30}"
        )
        logger.info(summary)
        logger.info("==> Feature Selection completed successfully.\n\n")
        return df_final

    except Exception as e:
        logger.error(f"Error during feature selection: {e}")
        return None