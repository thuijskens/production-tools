"""
Train module nodes
==================

This module contains nodes that train a random forest model
on the MNIST data set.
"""
import datetime as dt

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.preprocessing import LabelBinarizer


# NOTE: Normally you would put this in a config file
MODEL_OUTPUT_PATH = "models/example.joblib"


def get_mnist_data():
    """Loads the MNIST data set into memory.

    Returns
    -------
    X : array-like, shape=[n_samples, n_features]
        Training data for the MNIST data set.
        
    y : array-like, shape=[n_samples,]
        Labels for the MNIST data set.
    """
    digits = load_digits()
    X, y = digits.data, digits.target
    y = LabelBinarizer().fit_transform(y)

    return X, y


def fit_estimator(model_path, **kwargs):
    """Estimates a random forest on the MNIST data set.

    Parameters
    ----------
    model_path : str
        Path the pickled model is written to.

    kwargs : dict
        Keyword arguments for Airflow compatibility.
    """
    X, y = get_mnist_data()

    model = RandomForestClassifier(n_estimators=50)
    model.fit(X, y)

    joblib.dump(model, model_path)


def predict_samples(model_path, **kwargs):
    """Computes in-sample predictions on the MNIST data
    set, using the model built by ``fit_estimator``.

    Parameters
    ----------
    model_path : str
        Path the pickled model is loaded from.

    kwargs : dict
        Keyword arguments for Airflow compatibility.
    """
    model = joblib.load(model_path)
    X, y = get_mnist_data()

    # XX: Normally you would save the predictions to somewhere here.
    model.predict(X)


model_output_path = MODEL_OUTPUT_PATH
default_args = {
    "owner": "me",
    "start_date": dt.datetime(2017, 6, 1),
    "retries": 1,
    "retry_delay": dt.timedelta(minutes=5),
}

with DAG(
    "dummy_ml_pipeline", default_args=default_args, schedule_interval="0 * * * *"
) as dag:

    train_model = PythonOperator(
        task_id="train_model",
        provide_context=True,
        op_kwargs={"model_path": model_output_path},
        python_callable=fit_estimator,
    )

    predict_data = PythonOperator(
        task_id="predict_data",
        provide_context=True,
        op_kwargs={"model_path": model_output_path},
        python_callable=predict_samples,
    )

train_model.set_downstream(predict_data)
