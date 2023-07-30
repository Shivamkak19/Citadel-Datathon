import streamlit as st
import pandas as pd
import xgboost as xgb
from scipy import stats
import numpy as np
import json

# Load the trained XGBoost model
model = xgb.Booster(model_file="main.model")

# Load the actual dataset from the CSV file
traffic_processed = pd.read_csv("processed_traffic.csv")

# Client side function for calling the predictive model
def predict_avg_delay(avgFare, distance, airline_id):
    # Find the airline_id_hotkey for the given airline_id
    matching_rows = traffic_processed.loc[traffic_processed['airline_id'] == airline_id, 'airline_id_hotkey']
    if matching_rows.any():
        airline_id_hotkey = matching_rows.values[0]
    else:
        raise ValueError(f"No matching airline_id found for: {airline_id}")

    # Prepare the input for prediction
    input_data = pd.DataFrame({'avgFare': [avgFare], 'distance': [distance], 'airline_id_hotkey': [airline_id_hotkey]})

    # Use the trained model to predict the average delay
    predicted_delay = model.predict(xgb.DMatrix(input_data))[0]

    # Check if the data is approximately normally distributed
    # Using Shapiro-Wilk test (null hypothesis: data is normally distributed)
    _, p_value = stats.shapiro(predicted_delay)
    is_normal = p_value > 0.05

    if not is_normal:
        # If data is not normally distributed, use the best-fitting distribution for probability calculation
        probability = np.mean(prob_distribution >= predicted_delay)
    else:
        # If data is normally distributed, use None as probability (not applicable)
        probability = None

    return predicted_delay, probability

# Main API handler
def api_handler(request):
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps('Method Not Allowed')
        }

    try:
        # Parse JSON request body
        data = json.loads(request.body)

        # Get inputs from the JSON request body
        avgFare = data.get('avgFare')
        distance = data.get('distance')
        airline_id = data.get('airline_id')

        # Perform prediction
        predicted_delay, probability = predict_avg_delay(avgFare, distance, airline_id)

        # Prepare the response
        response_data = {
            'predicted_delay': predicted_delay,
            'probability': probability
        }

        return {
            'statusCode': 200,
            'body': json.dumps(response_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

# Streamlit app
def main():
    st.title("Average Delay Prediction")
    st.write("Enter the following information to predict the average delay:")

    # Input fields
    airline_id = st.text_input("Airline ID (e.g., AA)", "")
    distance = st.number_input("Distance", value=0.0)
    avgFare = st.number_input("Average Fare", value=0.0)

    # Predict button
    if st.button("Predict Average Delay"):
        if airline_id.strip() == "":
            st.error("Please enter a valid Airline ID.")
        else:
            predicted_delay, probability = predict_avg_delay(avgFare, distance, airline_id)
            st.write(f"Predicted Average Delay: {predicted_delay}")

            if probability is not None:
                st.write(f"Probability of Delay >= Predicted Delay: {probability}")
            else:
                st.write("Probability calculation is not available for the normal distribution case.")

if __name__ == "__main__":
    main()