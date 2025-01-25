from clean_data import clean
from tokenize_data import tokenize
from data_loading import load_data
import pandas as pd


if __name__ == "__main__":
    dataset = load_data("Data\\external\\fake_reviews_dataset.csv")

    dataset['text'] = dataset['text'].apply(clean)

    dataset.to_csv("Data\\cleaned\\cleaned.csv")

    cleaned_data = pd.read_csv("Data//cleaned//cleaned.csv")

    tokenize(cleaned_data)
