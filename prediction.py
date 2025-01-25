from clean_data import clean
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
from tensorflow.keras.models import load_model


def predict(string , model , tokenizer):
    cleaned_string = clean(string)
    tokenized_string = tokenizer.texts_to_sequences([cleaned_string])
    padded_string = pad_sequences(tokenized_string , maxlen = 323 , padding = "post")
    pred = model.predict([padded_string])
    if pred[0] < 0.6 :
        return "Not Fake"
    else:
        return "Fake"

if __name__ == "__main__":
    model = load_model("LSTM.h5")

    tokenizer = pickle.load(open("Data\\tokenized\\tokenizer.pkl" , "rb"))
    print(predict("""I'm writing the review after 2 months of my regular office usage and it has exceeded my expectations in every aspect. Here's a breakdown of why I believe it's an excellent choice:

1. Efficient Connectivity: The mouse boasts a reliable wireless connection, ensuring seamless performance without any lag. It's a joy to use, especially in fast-paced tasks or gaming scenarios.

2. Affordable Excellence: One of the standout features is its affordability without compromising quality. The Amazon Basics Wireless Optical Mouse offers top-notch performance at a price that doesn't break the bank, making it a budget-friendly yet high-quality option.

3. Compact and Handy: The mouse's compact design makes it incredibly easy to carry around, fitting comfortably in my hand. It's a perfect companion for those on the go, without sacrificing functionality""" , model , tokenizer))


