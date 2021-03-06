from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from tensorflow import keras
import pandas as pd
import json
import numpy as np

def read_dataset(path):
    return json.load(open(path)) 

train = read_dataset('../IME672/train.json')
test = read_dataset('../IME672/test.json')

def generate_text(data):
    text_data = [" ".join(doc['ingredients']).lower() for doc in data]
    return text_data 
    
train_text = generate_text(train)
test_text = generate_text(test)
target = [doc['cuisine'] for doc in train]

tfidf = TfidfVectorizer(binary=True)
def tfidf_features(txt, flag):
    if flag == "train":
        x = tfidf.fit_transform(txt)
    else:
        x = tfidf.transform(txt)
    x = x.astype('float16')
    return x 
X = tfidf_features(train_text, flag="train")
X_test = tfidf_features(test_text, flag="test")

lb = LabelEncoder()
y = lb.fit_transform(target)
print ("Train the model ... ")


model_SVM_L = SVC(kernel = 'linear', random_state = 42, probability=True)
st = time.time()
model_SVM_L.fit(X_train, y_train)
predictions_SVM = model_SVM_L.predict(X_test)
print('Accuracy: %0.4f [SVM Linear] [Time: %ss]' %(accuracy_score(y_test, predictions_SVM), (time.time()-st)))
Accuracy: 0.7923 [SVM Linear] [Time: 600.0440640449524s]
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2 ,random_state = 0)

summary = np.zeros((20, 20), dtype=np.int32)
for y_test_i, y_predict_i in zip(y_test, predictions_SVM):
    summary[y_test_i, y_predict_i] += 1

summary_df = pd.DataFrame(summary,columns=cuisines, 
                          index=cuisines)

summary_norm = ( summary / summary.sum(axis=1) )
sns.heatmap( summary_norm, 
            vmin=0, vmax=1, center=0.5, 
            xticklabels=cuisines,
            yticklabels=cuisines);
            
summary = np.zeros((20, 20), dtype=np.int32)
for y_test_i, y_predict_i in zip(y_test, predictions_SVM):
    summary[y_test_i, y_predict_i] += 1

summary_df = pd.DataFrame(summary,columns=cuisines, 
                          index=cuisines)

summary_norm = ( summary / summary.sum(axis=1) )
sns.heatmap( summary_norm, 
            vmin=0, vmax=1, center=0.5, 
            xticklabels=cuisines,
            yticklabels=cuisines);
            
print(classification_report(y_test,predictions_SVM))
