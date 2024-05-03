import argparse
import pandas as pd
import pickle

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", help="Input file path for new data", required=True)
    parser.add_argument("-o", "--output_file", help="Output file path for predictions", required=True)
    parser.add_argument("-p", "--prop", help="Property type (house of app)", choices=['house', 'app'], required=True)
    args = parser.parse_args()


if args.prop =='house':
    with open('./data/models/rfr_house_model_with_pipeline.pkl', 'rb') as file:
        model = pickle.load(file)
    X_test = pd.read_csv(args.input_file) 

    predictions = model.predict(X_test)
    
    # Save predictions to a CSV file
    predictions_df = pd.DataFrame(predictions, columns=['predictions'])
    predictions_df.to_csv(args.output_file, index=False)

    print("House Predictions saved to:", args.output_file)

elif args.prop =='app':
    with open('./data/models/rfr_app_model_with_pipeline.pkl', 'rb') as file:
        model = pickle.load(file)
    X_test = pd.read_csv(args.input_file) 

    predictions = model.predict(X_test)
    
    # Save predictions to a CSV file
    predictions_df = pd.DataFrame(predictions, columns=['predictions'])
    predictions_df.to_csv(args.output_file, index=False)

    print("App Predictions saved to:", args.output_file)
