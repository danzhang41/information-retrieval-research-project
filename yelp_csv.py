import csv
import re
import os
import argparse
import pandas as pd
import sys
from nltk.tokenize import WordPunctTokenizer
from sklearn.model_selection import train_test_split

def process(data_path):
    newFile = open('Yelp_Processed.csv', 'w', encoding="utf-8")
    with open(data_path, 'r', encoding="utf-8") as csvfile:
        int_count = 0
        for line in csvfile:
            line = line.split("\"")
            #print(line)
            for word in line:
                word = word.strip("\n")
                word = word.replace(',','')
                if(word and word != ','):
                    if(word.isnumeric() and int_count == 3):
                        newFile.write(",")
                    newFile.write(word)
                    #this is a convoluted way of making sure I don't add commas within the review text
                    if(word.isnumeric() or int_count == 1 or int_count == 2):
                        int_count+=1
                    if(int_count == 6): #means end of a review
                        int_count = 0
                        newFile.write("\n")
                    elif(int_count != 3):
                        newFile.write(",")
                    
                        
def process_to_final(data_path):
    finalFile = open('Yelp_Final.csv', 'w', encoding="utf-8")
    with open('stopwords.txt') as f:  # stop words
        stop_words = set(f.read().splitlines())
    with open('punctuations.txt') as f:  # useless punctuations
        punctuations = set(f.read().splitlines())
        
    with open(data_path, 'r', encoding="utf-8") as csvfile:
        df = []
        index = 0
        for line in csvfile:
            line = line.split(",")
            userId = line[1]
            businessId = line[2]
            rating = line[3]
            review = line[5]

            def clean_review(review):  # clean a review using stop words and useless punctuations
                review = review.lower()
                for p in punctuations:
                    review = review.replace(p, ' ')  # replace punctuations by space
                review = WordPunctTokenizer().tokenize(review)  # split words
                review = [word for word in review if word not in stop_words]  # remove stop words
                return ' '.join(review)
            review = clean_review(review)
            df.append([userId, businessId, review, rating])
            index+=1
            #print(df[index])
    return df
def create_for_model(data, train_rate, csv_path):
    df = pd.DataFrame(data, columns=['userID', 'itemID', 'review', 'rating'])
    df['userID'] = df.groupby(df['userID']).ngroup()
    df['itemID'] = df.groupby(df['itemID']).ngroup()
    train, valid = train_test_split(df, test_size=1 - train_rate, random_state=3)
    valid, test = train_test_split(valid, test_size=0.5, random_state=4)
    os.makedirs(csv_path, exist_ok=True)

    train.to_csv(os.path.join(csv_path, 'train.csv'), index=False, header=False)
    valid.to_csv(os.path.join(csv_path, 'valid.csv'), index=False, header=False)
    test.to_csv(os.path.join(csv_path, 'test.csv'), index=False, header=False)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', dest='data_path', default = 'Yelp_dataset/yelp_review_0.csv')
    parser.add_argument('--train_rate', dest='train_rate', default=0.8)
    parser.add_argument('--save_dir', dest='save_dir', default='./csv')

    args = parser.parse_args()
    #process(args.data_path)
    df = process_to_final('Yelp_Processed.csv')
    #print(df)
    create_for_model(df, args.train_rate, args.save_dir)
    print('Finished')

