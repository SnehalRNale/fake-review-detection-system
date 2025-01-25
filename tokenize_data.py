from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

def tokenize(data):

    xtrain , xtest , ytrain , ytest = train_test_split(data['text'] , data['label'] , test_size=0.25 , random_state=42)

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(xtrain)
    xtrain_tokenized = tokenizer.texts_to_sequences(xtrain)
    xtest_tokenized = tokenizer.texts_to_sequences(xtest)

    vocab = len(tokenizer.word_index) + 1
    max_length = max([len(i) for i in xtrain_tokenized])
    print(vocab , max_length)

    xtrain_padded = pad_sequences(xtrain_tokenized , maxlen = max_length , padding = "post")
    xtest_padded = pad_sequences(xtest_tokenized , maxlen = max_length , padding = "post")

    pd.DataFrame(xtrain_padded).to_csv("Data//tokenized//xtrain.csv")
    pd.DataFrame(xtest_padded).to_csv("Data//tokenized//xtest.csv")
    ytrain.to_csv("Data//tokenized//ytrain.csv")
    ytest.to_csv("Data//tokenized//ytest.csv")
    pickle.dump(tokenizer , open("Data//tokenized//tokenizer.pkl" , "wb"))

    

if __name__== "__main__":
    print("Hello")