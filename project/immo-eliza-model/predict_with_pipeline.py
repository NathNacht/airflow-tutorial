import argparse
import pandas as pd
import pickle

import os

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME', '/home/miubuntu/home/BECODE_PROJECTS/8_immo-eliza-airflow/immo-eliza-airflow')
project_directory = os.path.join(AIRFLOW_HOME, 'project')

# Define the file paths using os.path.join to ensure compatibility
huis_pickle_file_path = os.path.join(project_directory, "data", "models", "rfr_house_model_with_pipeline.pkl")
apartement_pickle_file_path = os.path.join(project_directory, "data", "models", "rfr_app_model_with_pipeline.pkl")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", help="Input file path for new data", required=True)
    parser.add_argument("-o", "--output_file", help="Output file path for predictions", required=True)
    parser.add_argument("-p", "--prop", help="Property type (house of app)", choices=['house', 'app'], required=True)
    args = parser.parse_args()


if args.prop =='house':
    with open(huis_pickle_file_path, 'rb') as file:
        model = pickle.load(file)
    X_test = pd.read_csv(args.input_file) 

    predictions = model.predict(X_test)
    
    # Save predictions to a CSV file
    predictions_df = pd.DataFrame(predictions, columns=['predictions'])
    predictions_df.to_csv(args.output_file, index=False)

    print("House Predictions saved to:", args.output_file)

elif args.prop =='app':
    with open(apartement_pickle_file_path, 'rb') as file:
        model = pickle.load(file)
    X_test = pd.read_csv(args.input_file) 

    predictions = model.predict(X_test)
    
    # Save predictions to a CSV file
    predictions_df = pd.DataFrame(predictions, columns=['predictions'])
    predictions_df.to_csv(args.output_file, index=False)

    print("App Predictions saved to:", args.output_file)
