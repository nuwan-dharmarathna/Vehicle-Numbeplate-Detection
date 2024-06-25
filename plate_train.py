import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

import random


#Load the model

model_path = './models/number_plate_model.joblib'

model = joblib.load(model_path)

# Load the label encoders
encoders_filename = './models/label_encoders.joblib'
label_encoders = joblib.load(encoders_filename)

#  Remake the array size to 85
def remake_array(arr):
    # Step 1: Remove the first 10 items
    arr = arr[10:]
    
    # Step 2: Check the array length
    if len(arr) > 85:
        # If len(arr) > 85, remove elements till the length becomes 85
        arr = arr[:85]
    elif len(arr) < 85:
        # If len(arr) < 85, fill with random values till the length becomes 85
        while len(arr) < 85:
            arr.append(random.choice(arr)) # Choose a random element from the current array to fill
    
    return arr

test_data = [
    "NC;0", "HG0532", "HG0532", "HG0532", "HG0532", "HG9532", "HG9532", "HG9532",
    "NKHG9532", "NKHG9532", "NHHG9532", "NHHG9532", "NHHG9532", "NKHG9532", "NXHG9532",
    "NKHG-9532", "NXHG9532", "NKHG9532", "NHHG9532", "NKHG9532", "NHHG9532", "NHG9532",
    "NHHG0532", "NHG9532", "NHHG9532", "NKHG9532", "NXHG9532", "NXHG9532", "NXHG9532",
    "NKHG9532", "NXHG9532", "NHHG9532", "NHHG9532", "NHHG9532", "NXHG9532", "NKHG9532",
    "NKHG9532", "NKHG9532", "NHHG9532", "NHHG9532", "NHHG9532", "NKHG9532", "NKHG9532",
    "NHHG9532", "NKHG9532", "NKHG9532", "NKHG9532", "NXHG9532", "NHHG9532", "NHHG9532",
    "NHHG9532", "NHHG9532"
]

# Convert the test data into a DataFrame
test_df = pd.DataFrame([test_data], columns=label_encoders.keys())

# Fill missing values in the test data (if any)
test_df.fillna('missing', inplace=True)

# Encode the test data using the same label encoders used for training data
for col in test_df.columns:
    test_df[col] = label_encoders[col].transform(test_df[col])

# Make predictions using the loaded model
prediction = model.predict(test_df)
predicted_target = label_encoders['Target'].inverse_transform(prediction)

print(f'Predicted Target: {predicted_target[0]}')