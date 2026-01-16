import pandas as pd
from error_logs import configure_logger

logger = configure_logger()




def features_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs Ordinal, One-Hot, and Binary encoding on the dataset.
    Removes non-predictive ID columns.
    """
    try:
        logger.info("==> Starting Feature Engineering...")
        df_feat = df.copy()

        # Safety: Remove ID if it exists (IDs are not features!)
        if 'student_id' in df_feat.columns:
            df_feat = df_feat.drop(columns=['student_id'])
            logger.info("==> Feature Engineering: Removed 'student_id'.")

        # Ordinal Encoding (Mapped by Rank/Logic)
        ordinal_mappings = {
            'parental_education_level': {'Unknown': 0, 'High School': 1, 'Bachelor': 2, 'Master': 3},
            'internet_quality': {'Poor': 1, 'Average': 2, 'Good': 3},
            'diet_quality': {'Poor': 1, 'Fair': 2, 'Good': 3}
        }
        for col, mapping in ordinal_mappings.items():
            if col in df_feat.columns:
                df_feat[col] = df_feat[col].map(mapping)
        logger.info("==> Ordinal Encoding complete for Education, Internet, and Diet.")

        # 4. One-Hot Encoding (No natural order)
        if 'gender' in df_feat.columns:
            df_feat = pd.get_dummies(df_feat, columns=['gender'], drop_first=True, dtype=int)
            logger.info("==> One-Hot Encoding complete for Gender.")

        # Binary Encoding (Yes/No to 0/1)
        binary_encoding = {
            'part_time_job': {'No': 0, 'Yes': 1},
            'extracurricular_participation': {'No': 0, 'Yes': 1}
        }
        for col, mapping in binary_encoding.items():
            if col in df_feat.columns:
                df_feat[col] = df_feat[col].map(mapping)
        logger.info("==> Binary Encoding complete for Job and Participation.")

        # Final check: Ensure all okay
        summary = (
            f"\n{'='*30}\n"
            f"FEATURE ENGINEERING REPORT\n"
            f"{'='*30}\n"
            f"Rows: {df_feat.shape[0]} | Columns: {df_feat.shape[1]}\n"
            f"Dtypes: {df_feat.dtypes.value_counts().to_dict()}\n"
            f"Columns: {df_feat.columns.tolist()}\n"
            f"{'='*30}"
        )
        logger.info(summary)
        logger.info("==> Feature Engineering completed successfully.\n\n")
        return df_feat

    except Exception as e:
        logger.error(f"Error in Feature Engineering: {e}")
        return None
    
# Run: python -m src.step.c_feature_engineering