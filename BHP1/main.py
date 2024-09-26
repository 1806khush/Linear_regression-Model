from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

# Load the dataset and the trained model
data = pd.read_csv(r'C:\BHP1\Cleaned_data.csv')
with open('RidgeModel.pkl', 'rb') as f:
    pipe = pickle.load(f)

@app.route('/')
def index():
    # Fetching unique locations for the dropdown
    locations = sorted(data['location'].unique())
    return render_template('index.html', locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    location = request.form.get('location')
    bhk = float(request.form.get('bhk'))
    bath = float(request.form.get('bath'))
    sqft = float(request.form.get('total_sqft'))

    # Prepare the input DataFrame
    input_df = pd.DataFrame([{
        'location': location,
        'total_sqft': sqft,
        'bath': bath,
        'bhk': bhk
    }])

    try:
        # Make the prediction
        prediction = pipe.predict(input_df)[0] * 1e5  # Adjust price scale
        return str(np.round(prediction, 2))
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
