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
y_NN = keras.utils.to_categorical(y)

model = keras.Sequential()
model.add(keras.layers.Dense(1000, kernel_initializer=keras.initializers.he_normal(seed=1), activation='relu', input_dim=3010))
model.add(keras.layers.Dropout(0.81))
model.add(keras.layers.Dense(1000, kernel_initializer=keras.initializers.he_normal(seed=2), activation='relu'))
model.add(keras.layers.Dropout(0.81))
model.add(keras.layers.Dense(20, kernel_initializer=keras.initializers.RandomNormal(mean=0.0, stddev=0.05, seed=4), activation='softmax'))
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

from sklearn.model_selection import train_test_split
X_train_NN, X_test_NN, y_train_NN, y_test_NN = train_test_split(X, y_NN , random_state = 0)
history = model.fit(X_train_NN, y_train_NN, epochs=20, batch_size=512, validation_split=0.1)

score=model.evaluate(X_test_NN,y_test_NN)

y_predict_NN=model.predict(X_test_NN)
predictions_encoded = lb.inverse_transform([np.argmax(pred) for pred in y_predict_NN])
y_predict_NN = lb.fit_transform(predictions_encoded)
y_test_NN_encoded=lb.inverse_transform([np.argmax(pred) for pred in y_test_NN])
y_test_NN = lb.fit_transform(y_test_NN_encoded)
summary = np.zeros((20, 20), dtype=np.int32)

for y_test_i, y_predict_i in zip(y_test_NN, y_predict_NN):
    summary[y_test_i, y_predict_i] += 1

summary_df = pd.DataFrame(summary, 
                          columns=cuisines, 
                          index=cuisines)

summary_df

summary_norm = ( summary / summary.sum(axis=1) )
sns.heatmap( summary_norm, 
            vmin=0, vmax=1, center=0.5, 
            xticklabels=cuisines,
            yticklabels=cuisines);

print(classification_report(y_test_NN,y_predict_NN))

print(history.history.keys())
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

y_predict_NN=model.predict(X_test)
print(X_test.shape)
predictions_encoded = lb.inverse_transform([np.argmax(pred) for pred in y_predict_NN])
predictions = lb.inverse_transform([np.argmax(pred) for pred in predictions_encoded])
test_id = [doc['id'] for doc in test]
sub = pd.DataFrame({'id': test_id, 'cuisine': predictions}, columns=['id', 'cuisine'])
sub.to_csv('output_NN.csv', index=False)

