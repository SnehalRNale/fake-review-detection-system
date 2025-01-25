from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, GlobalAveragePooling1D, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils.class_weight import compute_class_weight

def check_class_imbalance(ytrain):
    # Check class distribution
    class_distribution = pd.Series(ytrain).value_counts()
    print("Class Distribution in Training Data:")
    print(class_distribution)
    
    # Visualize the class distribution
    plt.figure(figsize=(8, 6))
    plt.bar(class_distribution.index, class_distribution.values)
    plt.xlabel('Class Labels')
    plt.ylabel('Frequency')
    plt.title('Class Distribution')
    plt.show()
    
    # Calculate imbalance ratio
    class_ratio = class_distribution.max() / class_distribution.min()
    print(f"Class Imbalance Ratio: {class_ratio}")
    
    # If highly imbalanced, compute class weights
    if class_ratio > 2:  # You can adjust the threshold based on your case
        print("Class imbalance detected. Adjusting class weights.")
        class_weights = compute_class_weight('balanced', classes=np.unique(ytrain), y=ytrain)
        class_weight_dict = dict(zip(np.unique(ytrain), class_weights))
        return class_weight_dict
    else:
        return None

def model():
    model = Sequential()
    # Embedding layer: converts integer sequences to dense vectors
    model.add(Embedding(output_dim=128, input_dim=50000))

    # LSTM layer: for sequence processing
    model.add(LSTM(64, return_sequences=True))

    # Dropout layer: to prevent overfitting by randomly setting a fraction of inputs to zero
    model.add(Dropout(0.5))  # 50% dropout rate

    # Global Average Pooling: reduces dimensions by averaging over the sequence
    model.add(GlobalAveragePooling1D())

    # Dense layer with ReLU activation
    model.add(Dense(128, activation='relu'))

    # Output layer: sigmoid for binary classification
    model.add(Dense(1, activation='sigmoid'))

    # Compile model with binary crossentropy loss and Adam optimizer
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Load data
    xtrain = pd.read_csv("Data//tokenized//xtrain.csv")
    xtest = pd.read_csv("Data//tokenized//xtest.csv")
    ytrain = pd.read_csv("Data//tokenized//ytrain.csv")
    ytest = pd.read_csv("Data//tokenized//ytest.csv")

    # Flatten ytest
    ytest = ytest['label'].values  # or ytest.squeeze()

    # EarlyStopping callback: stop training if validation loss doesn't improve for 3 epochs
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    # Check for class imbalance and calculate class weights if needed
    class_weight_dict = check_class_imbalance(ytrain['label'])

    if class_weight_dict:
        print("Training with class weights.")
        model.fit(np.array(xtrain), np.array(ytrain['label']), epochs=10, validation_data=(np.array(xtest), np.array(ytest)), class_weight=class_weight_dict, callbacks=[early_stopping])
    else:
        print("Training without class weights.")
        model.fit(np.array(xtrain), np.array(ytrain['label']), epochs=10, validation_data=(np.array(xtest), np.array(ytest)), callbacks=[early_stopping])

    # Evaluate the model
    evaluation = model.evaluate(np.array(xtest), np.array(ytest))
    print(f"Test Loss: {evaluation[0]}")
    print(f"Test Accuracy: {evaluation[1]}")

    # Save the model
    model.save("LSTM.h5")

    return "Your Task is completed."

if __name__ == "__main__":
    print(model())
