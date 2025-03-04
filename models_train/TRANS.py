import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, MultiHeadAttention, Dense, LayerNormalization, Flatten
from tensorflow.keras.utils import to_categorical
import tensorflow as tf

iris = load_iris()
X = iris.data
y = iris.target

y = to_categorical(y, num_classes=3)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

inputs = Input(shape=(1, 4))
attention_output = MultiHeadAttention(num_heads=4, key_dim=4)(inputs, inputs) 
attention_output = LayerNormalization()(attention_output)
flatten = Flatten()(attention_output)
dense_1 = Dense(64, activation='relu')(flatten)
outputs = Dense(3, activation='softmax')(dense_1)

model_transformer = Model(inputs=inputs, outputs=outputs)

model_transformer.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model_transformer.fit(X_train, y_train, epochs=50, batch_size=16, validation_split=0.2)

model_transformer.save("trans_model.h5")

loss, accuracy = model_transformer.evaluate(X_test, y_test)
print(f"Précision Transformer : {accuracy:.2f}")