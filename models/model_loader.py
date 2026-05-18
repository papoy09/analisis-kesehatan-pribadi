import pickle
import streamlit as st


@st.cache_resource
def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)


rf_model = load_model("rf_model.pkl")
xgb_model = load_model("xgb_model.pkl")
