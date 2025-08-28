import numpy as np


X = np.array ([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y = np.array ([0, 1, 1, 1])

weights = np.random.rand(2)
bias = np.random.rand(1)
learning_rate = 0.1

for epoch in range (20):
    for i in range(len(X)):
        linear_output = np.dot(X[i], weights) + bias

        y_pred = 1 if linear_output >= 0.5 else 0
        error = y[i] - y_pred
        weights += learning_rate *error * X[i]
        bias += learning_rate * error

print("Trénované váhy:", weights)
print("Bias:", bias)

for i in range(len(X)):
    linear_output = np.dot(X[i]), weights + bias
    y_pred = 1 if linear_output >= 0.5 else 0
    print(f"Vstup: {X[i]} >= Predikcia: {y_pred}")