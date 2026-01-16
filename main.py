import sys
from src.pipeline.ETLFeaturePipeline import run_pipeline
from src.step.f_predict import make_prediction

def main():
    while True:
        print("\n" + "="*30)
        print(" ACADEMIC PERFORMANCE SYSTEM ")
        print("="*30)
        print("1. Train Model (Run ETL Pipeline)")
        print("2. Make a Prediction")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ")

        if choice == '1':
            # ONLY runs the pipeline if the user selects 1
            result = run_pipeline()
            if result:
                # Unpack the three values returned by your pipeline
                model, scaler, metrics = result
                print(f"\nTraining Complete!")
                # Note: Ensure your metrics dict has 'model_name' or use best_model_name
                print(f"Best Model Performance: {metrics['r2']:.4f} R2")
                
        elif choice == '2':
            # Executes your prediction script using the saved .pkl files
            make_prediction()
            
        elif choice == '3':
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please run again.")

if __name__ == "__main__":
    main()



# Run: python main.py