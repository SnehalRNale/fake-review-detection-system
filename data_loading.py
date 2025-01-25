import pandas as pd

def load_data(path):

    dataset = pd.read_csv(path)

    dataset.drop_duplicates(subset=['text' , 'label'] , inplace=True)

    dataset['text'] = dataset['category'] + dataset['text']

    dataset = dataset[['text' , 'label']] 

    dataset = dataset.sample(dataset.shape[0])

    return dataset


if __name__ == "__main__":   
    print(load_data("Data\\external\\fake_reviews_dataset.csv"))
                    

