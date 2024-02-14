import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Load the trained model
model = joblib.load('D:\\Scifor mini project\\Build For Bharat Hackathon\\price.pkl')  # Replace 'your_model.pkl' with the path to your trained model

# Function to preprocess input data and make predictions
def predict(total_price, freight_price, customers, comp_1, comp_2, comp_3, fp1, fp2, fp3, product_score):
    # Create a DataFrame from the input data
    data = pd.DataFrame({
        'total_price': [total_price],
        'freight_price': [freight_price],
        'customers': [customers],
        'comp_1': [comp_1],
        'comp_2': [comp_2],
        'comp_3': [comp_3],
        'fp1': [fp1],
        'fp2': [fp2],
        'fp3': [fp3],
        'product_score': [product_score]
    })

    # Make predictions using the model
    predicted_price = model.predict(data)[0]

    return predicted_price

# Load your data
df = pd.read_csv('D:\\Scifor mini project\\Build For Bharat Hackathon\\retail_price.csv')

# Streamlit app
st.title("Price Optimization Model")

# Add dropdown navigation
selected_page = st.sidebar.selectbox("Navigation", ["Predict", "Model Info", "About Group", "Charts"])

if selected_page == "Predict":
    st.title("Predict price")
    # Input fields
    total_price = st.number_input("Total Price", value=0.0)
    freight_price = st.number_input("Freight Price", value=0.0)
    customers = st.number_input("Customers", value=0)
    comp_1 = st.number_input("Comp 1", value=0.0)
    comp_2 = st.number_input("Comp 2", value=0.0)
    comp_3 = st.number_input("Comp 3", value=0.0)
    fp1 = st.number_input("FP1", value=0.0)
    fp2 = st.number_input("FP2", value=0.0)
    fp3 = st.number_input("FP3", value=0.0)
    product_score = st.number_input("Product Score", value=0.0)

    # Prediction button
    if st.button("Predict"):
        predicted_price = predict(total_price, freight_price, customers, comp_1, comp_2, comp_3, fp1, fp2, fp3, product_score)
        st.markdown(f"**Predicted Unit Price:** {predicted_price}", unsafe_allow_html=True)

elif selected_page == "Model Info":
    st.title("Model Info")
    st.write("""
             Random Forest is a popular ensemble learning technique used for both classification and regression tasks. In the case of regression, it is called Random Forest Regressor.

Random Forest is a machine learning algorithm that operates by constructing a multitude of decision trees during training time and outputting the mean prediction (regression) or the mode prediction (classification) of the individual trees.

Ensemble Learning: Random Forest Regressor is an ensemble learning method that constructs multiple decision trees during training and outputs the average prediction of individual trees for regression tasks.

Bootstrapping: It uses bootstrapping to create multiple subsets of the original dataset by random sampling with replacement, ensuring diversity among the trees.

Random Feature Selection: At each node of the decision tree, a random subset of features is considered for splitting, reducing the correlation between trees and increasing robustness.

Prediction Aggregation: During prediction, each tree independently predicts the output value, and the final prediction is the average of these individual predictions, reducing overfitting.

Feature Importance: Random Forest provides a measure of feature importance, enabling the identification of influential features in the prediction process.

Robustness: Random Forest is robust to noise and outliers, making it suitable for datasets with complex relationships and noisy data.

Model Performance: It often yields high accuracy and generalization performance, even with large datasets and high-dimensional feature spaces.
             
Random Forest Regressor was chosen by us for its ability to handle a diverse range of features and complex relationships in the data, providing robust and accurate predictions for price optimization. Its ensemble nature and feature importance analysis make it suitable for understanding the drivers of optimal pricing decisions in your model. Additionally, its resistance to overfitting ensures reliable performance even with limited data and noisy inputs.
    """)

elif selected_page == "About Group":
    st.title("ALGOACES")
    st.write("""
    We are a team of data scientists passionate about solving real-world problems using machine learning and data analytics. Our group consists of professionals with expertise in various domains.
    """)
    
    st.markdown(f"Team Leader: Ann Francis Mariya")
    st.markdown(f"Team Member: Mohit Mande")
    st.markdown(f"Team Member: Sesna Tony")

elif selected_page == "Charts":
    st.title("Charts")

    # Dropdown for selecting the chart type
    chart_type = st.selectbox("Select Chart Type", ["Chart 1", "Chart 2", "Chart 3"])

    if chart_type == "Chart 1":
        # Chart 1: Total Price by Product Category
        fig = px.bar(df, x='product_category_name', y='total_price', title='Total Price by Product Category')
        st.plotly_chart(fig)

    elif chart_type == "Chart 2":
        # Chart 2: Unit Price by Product Category
        fig = px.bar(df, x='product_category_name', y='unit_price', title='Unit Price by Product Category')
        st.plotly_chart(fig)

    elif chart_type == "Chart 3":
        # Chart 3: Total Price vs Number of Customers
        monthly_df = df.groupby('month').agg({'customers': 'sum', 'total_price': 'sum'}).reset_index()
        fig = px.scatter(monthly_df, x='customers', y='total_price', trendline='ols',
                         title='Total Price vs Number of Customers')
        st.plotly_chart(fig)
