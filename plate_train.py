import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load the CSV file
file_path = './frames_data.csv'
data = pd.read_csv(file_path)

# Fill missing values with a placeholder
data.fillna('missing', inplace=True)

# Initialize label encoders for each column
label_encoders = {col: LabelEncoder() for col in data.columns}

# Encode categorical variables
for col in data.columns:
    data[col] = label_encoders[col].fit_transform(data[col])

# Separate features and target
X = data.drop(columns=['Target'])
y = data['Target']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a RandomForestClassifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save the trained model to a file
model_filename = './models/number_plate_model.joblib'
joblib.dump(model, model_filename)

# Load the model from the file
loaded_model = joblib.load(model_filename)

# Make predictions on the test set
y_pred = loaded_model.predict(X_test)

# Evaluate the model
report = classification_report(y_test, y_pred)
print("Classification Report:\n", report)

# Test data provided
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
test_df = pd.DataFrame([test_data], columns=data.columns[:-1])

# Fill missing values in the test data (if any)
test_df.fillna('missing', inplace=True)

# Encode the test data using the same label encoders used for training data
for col in test_df.columns:
    test_df[col] = label_encoders[col].transform(test_df[col])

# Make predictions using the loaded model
prediction = loaded_model.predict(test_df)
predicted_target = label_encoders['Target'].inverse_transform(prediction)

print(f'Predicted Target: {predicted_target[0]}')
