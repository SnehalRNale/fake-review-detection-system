from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, accuracy_score
import numpy as np
import pandas as pd
import tensorflow as tf

# Load the test data
xtest = pd.read_csv("Data//tokenized//xtest.csv")
ytest = pd.read_csv("Data//tokenized//ytest.csv")

# Load the trained model
model = tf.keras.models.load_model("LSTM.h5")

# Make predictions
predictions = model.predict(np.array(xtest))
# Binarize predictions: assuming a binary classification task with threshold 0.5
y_pred = (predictions > 0.5).astype(int).flatten()

# Calculate metrics
accuracy = accuracy_score(ytest['label'], y_pred)
precision = precision_score(ytest['label'], y_pred)
recall = recall_score(ytest['label'], y_pred)
f1 = f1_score(ytest['label'], y_pred)
conf_matrix = confusion_matrix(ytest['label'], y_pred)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:\n", conf_matrix)
