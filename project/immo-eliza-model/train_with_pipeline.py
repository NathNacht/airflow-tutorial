import pandas as pd
import numpy as np
import os
# import cPickle as pickle
import pickle
import math
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error as MSE
# from preprocessing_with_pipeline import preprocessing


AIRFLOW_HOME = os.getenv('AIRFLOW_HOME', '/home/miubuntu/home/BECODE_PROJECTS/8_immo-eliza-airflow/immo-eliza-airflow')
project_directory = os.path.join(AIRFLOW_HOME, 'project')

# Define the file paths using os.path.join to ensure compatibility
clean_huis_te_koop_path = os.path.join(project_directory, "data", "cleaned", "clean_house.csv")
clean_apartement_te_koop_path = os.path.join(project_directory, "data", "cleaned", "clean_app.csv")
huis_pickle_file_path = os.path.join(project_directory, "data", "models", "rfr_house_model_with_pipeline.pkl")
apartement_pickle_file_path = os.path.join(project_directory, "data", "models", "rfr_app_model_with_pipeline.pkl")



def preprocessing(df, prop):
    """ Preprocesses features for house and app
        Imputes missing values for swimmingpool -> they get filled up with 0
        Label encoding for a few categorical features
        Removing columns that are not needed
    """
    # Define features
    target_column_to_drop = ['price']
    X = df.drop(columns=target_column_to_drop, axis=1)

    if prop =='house':
        # Define columns to drop    
        columns_to_drop = ['property_id', 'latitude', 'longitude', 'property_type', 'type_of_sale', 'fully_equipped_kitchen', 'locality_name', 'main_city']
    elif prop =='app':
        columns_to_drop = ['property_id', 'latitude', 'longitude', 'property_type', 'type_of_sale', 'fully_equipped_kitchen', 'locality_name', 'main_city', 'surface_of_good']

    X = X.drop(columns=columns_to_drop, axis=1)

    return X

def train_model(X, y):
    """
    Trains a Random Forest Regressor on the given features and target
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #______Define categorical and numerical features____
    
    #______identify numerical columns____
    numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.values
    
    #______identify categorical columns____
    categorical_features = X.select_dtypes(include=['object']).columns.values
    
    #______Define the pipeline for imputing the 'swimming_pool' column_____
    swimming_pool_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=0))
    ])

    #_____Manual Fit and transform the 'swimming_pool' column using the pipeline_____
    # X_train['swimming_pool'] = swimming_pool_pipeline.fit_transform(X_train[['swimming_pool']])
    # X_test['swimming_pool'] = swimming_pool_pipeline.fit_transform(X_test[['swimming_pool']])

    #_____Define the pipeline for encoding the categorical features_____
    categorical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(missing_values=np.nan, strategy='constant', fill_value='missing')),
        ('encoder', OrdinalEncoder())
    ])

    #_____Manual Fit and transform the categorical features using the pipeline_____
    # X_train[categorical_features] = categorical_pipeline.fit_transform(X_train[categorical_features])
    # X_test[categorical_features] = categorical_pipeline.fit_transform(X_test[categorical_features])

    #_____Define the pipeline for encoding the categorical features_____
    numerical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(missing_values=np.nan, strategy='constant', fill_value=-1))
    ])

    #_____ManualFit and transform the categorical features using the pipeline_____
    # X_train[numerical_features] = numerical_pipeline.fit_transform(X_train[numerical_features])
    # X_test[numerical_features] = numerical_pipeline.fit_transform(X_test[numerical_features])

    preprocessing_pipeline = ColumnTransformer(transformers=[
        ('swimmingpool_imputer', swimming_pool_pipeline, ['swimming_pool']),
        ('categorical_imputer_encoder', categorical_pipeline, categorical_features),
        ('numerical_imputer_encoder', numerical_pipeline, numerical_features)
    ])

    grid_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessing_pipeline),
        ('regressor', RandomForestRegressor())
    ])

    #____Define parameter grid for grid search____
    param_grid = {
        'regressor__max_depth': [10, 15, 20, 25, 30, 40],
        'regressor__n_estimators': [100, 200]
    }

    #____Perform grid search____
    grid = GridSearchCV(grid_pipeline, param_grid=param_grid, cv=3, verbose=4, error_score='raise')  
    grid.fit(X_train, y_train)

    best_max_depth = grid.best_params_['regressor__max_depth']
    best_n_estimators = grid.best_params_['regressor__n_estimators']

    #____show the choosen max_depth____
    print("randomforest choosen max_depth: ", best_max_depth)

    #____show the choosen n_estimators____
    print("randomforest choosen n_estimators: ", best_n_estimators)

    final_model = Pipeline(steps=[
        ('preprocess', preprocessing_pipeline),
        ('regressor', RandomForestRegressor(n_estimators=best_n_estimators, max_depth=best_max_depth))])
    final_model.fit(X_train, y_train)
    
        
    #____Show training score____
    print("Random Forest training score:", final_model.score(X_train, y_train))

    #____Test the model____
    y_prediction = final_model.predict(X_test)

    #____Show test score____
    print("Random Forest test score:", final_model.score(X_test, y_test))

    mse = MSE(y_test, y_prediction)
    rmse = math.sqrt(mse)
    print("RMSE:", rmse)

    print("Cross-validation score:", cross_val_score(final_model, X_train, y_train).mean())

    return final_model


# HOUSES

df_house = pd.read_csv(clean_huis_te_koop_path, sep=",")

# _____Define X and y_____
y_house = df_house['price']
X_house = preprocessing(df_house, prop='house')

# _____Train the model____
model_house = train_model(X_house, y_house)

# _____Create pickle file____
with open(huis_pickle_file_path, 'wb') as file:
    pickle.dump(model_house, file=file)
print("For HOUSE rfr_house_model_with_pipeline.pkl has been created in the models folder")

# _____APARTMENTS_____
df_app = pd.read_csv(clean_apartement_te_koop_path, sep=",")

# _____Define X and y_____
y_app = df_app['price']
X_app = preprocessing(df_app, prop='app')

# _____Train the model____
model_app = train_model(X_app, y_app)

# _____Create pickle file____
with open(apartement_pickle_file_path, 'wb') as file:
    pickle.dump(model_app, file=file)
print("For APARTMENTS rfr_app_model_with_pipeline.pkl has been created in the models folder")