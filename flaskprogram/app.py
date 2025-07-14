from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd
from model import TreeNode, DecisionTree, RandomForest

app = Flask(__name__)

# Load your saved model AND feature names
with open("loan_model.pkl", "rb") as f:
    model = pickle.load(f)

# CRITICAL: Load the feature names to ensure correct order
with open("features.pkl", "rb") as f:
    feature_names = pickle.load(f)

print("Expected feature order:", feature_names)
print("Number of features expected:", len(feature_names))

# Encoding maps - make sure these match your training data
gender_map = {"Male": 1, "Female": 0}
married_map = {"Yes": 1, "No": 0}
dependents_map = {"0": 0, "1": 1, "2": 2, "3+": 3}
education_map = {"Graduate": 1, "Not Graduate": 0}
self_employed_map = {"Yes": 1, "No": 0}
property_area_map = {"Urban": 2, "Semiurban": 1, "Rural": 0}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            # Get form data
            gender = request.form.get("Gender")
            married = request.form.get("Married")
            dependents = request.form.get("Dependents")
            education = request.form.get("Education")
            self_employed = request.form.get("Self_Employed")
            applicant_income = float(request.form.get("ApplicantIncome"))
            coapplicant_income = float(request.form.get("CoapplicantIncome"))
            loan_amount = float(request.form.get("LoanAmount"))
            loan_amount_term = float(request.form.get("Loan_Amount_Term"))
            credit_history = float(request.form.get("Credit_History"))
            property_area = request.form.get("Property_Area")

            # Encode categorical features
            gender_enc = gender_map.get(gender, 0)
            married_enc = married_map.get(married, 0)
            dependents_enc = dependents_map.get(dependents, 0)
            education_enc = education_map.get(education, 0)
            self_employed_enc = self_employed_map.get(self_employed, 0)
            property_area_enc = property_area_map.get(property_area, 0)

            # Create a dictionary with all features
            input_dict = {
                'Gender': gender_enc,
                'Married': married_enc,
                'Dependents': dependents_enc,
                'Education': education_enc,
                'Self_Employed': self_employed_enc,
                'ApplicantIncome': applicant_income,
                'CoapplicantIncome': coapplicant_income,
                'LoanAmount': loan_amount,
                'Loan_Amount_Term': loan_amount_term,
                'Credit_History': credit_history,
                'Property_Area': property_area_enc
            }

            # CRITICAL: Build input array in the EXACT order from training
            input_data = np.array([[input_dict[feature] for feature in feature_names]])
            
            print("Input data shape:", input_data.shape)
            print("Input data:", input_data)

            # Predict
            prediction = model.predict(input_data)[0]
            print("Raw prediction:", prediction)
            
            # Convert prediction to label
            # Check what your actual labels were during training
            pred_label = "Y" if prediction == 1 else "N"

            return render_template("form.html", prediction=pred_label, 
                                 input_data=input_data.tolist(), 
                                 raw_prediction=prediction)

        except Exception as e:
            print("Error:", str(e))
            return render_template("form.html", error=str(e))

    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)