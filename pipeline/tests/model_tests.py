"""
Unit tests for the MNIST model
==============================
"""
import os
import shutil

from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from pipeline.dags.train_model import get_mnist_data, fit_estimator


def test_accuracy():
    # XX: This is not the cleanest test ever, but shows the concept
    os.mkdir('./tmp')
    fit_estimator(model_path='./tmp/model.joblib')

    X, y = get_mnist_data()
    model = joblib.load('./tmp/model.joblib')
    y_pred = model.predict(X)

    shutil.rmtree('./tmp')

    assert(accuracy_score(y, y_pred) >= 0.9)
