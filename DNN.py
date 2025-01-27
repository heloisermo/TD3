#DNN import
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import r2_score

iris = load_iris()
X = iris.data
y = X[:, 0]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

y_mean = y_train.mean()
y_std = y_train.std()
y_train = (y_train - y_mean) / y_std
y_test = (y_test - y_mean) / y_std

model_dnn = Sequential([
    Dense(128, activation='relu', input_shape=(4,)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1)
])

model_dnn.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])

history = model_dnn.fit(X_train, y_train, validation_split=0.2, epochs=100, batch_size=16, verbose=1)

model_dnn.save("dnn_model.h5")

loss, mae = model_dnn.evaluate(X_test, y_test, verbose=0)

y_pred = model_dnn.predict(X_test)

y_test_original = y_test * y_std + y_mean
y_pred_original = y_pred.flatten() * y_std + y_mean

r2 = r2_score(y_test_original, y_pred_original)
print(f"R2 Score : {r2:.2f}")
