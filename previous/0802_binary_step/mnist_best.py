import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np
from tensorflow import keras

data = np.load('mnist.npz')

print(data)
for k in data.files:
    print(k)
print(data.keys())

data = np.load('mnist.npz')
lst = data.files
for item in lst:
    print(item)
    print(data[item])

X_train, y_train, X_test, y_test = data['x_train'], data['y_train'], data['x_test'], data['y_test']

(train_images, train_labels), (test_images, test_labels) = (X_train, y_train), (X_test, y_test)

train_labels = train_labels[:1000]
test_labels = test_labels[:1000]

train_images = train_images[:1000].reshape(-1, 28 * 28) / 255.0
test_images = test_images[:1000].reshape(-1, 28 * 28) / 255.0




X_train = X_train / 255
X_test = X_test / 255

X_train_flattened = X_train.reshape(len(X_train), 28 * 28)
X_test_flattened = X_test.reshape(len(X_test), 28 * 28)




model = keras.Sequential([
    keras.layers.Dense(200, input_shape=(784,), activation='relu'),
    keras.layers.Dense(100, input_shape=(200,), activation='relu'),
    keras.layers.Dense(50, input_shape=(100,), activation='tanh'),
    keras.layers.Dense(10, input_shape=(50,), activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

epochs_num = 1

acc_list = []

for i in range(epochs_num):
    model.fit(X_train_flattened, y_train, epochs=1)
    y_predicted = model.predict(X_test_flattened)
    print('y_predicted',y_predicted)
    loss, acc = model.evaluate(test_images, test_labels, verbose=2)
    print('Restored model, accuracy: {:5.2f}%'.format(100 * acc))
    acc_list.append('Restored model, accuracy: {:5.2f}%'.format(100 * acc))

    from keras.callbacks import History

    history = History()
    print(history.model)

model.save('./ws_model.h5')

for i in acc_list:
    print(i)


#
# y_predicted_labels = [np.argmax(i) for i in y_predicted]
#
# y_predicted_labels[:5]
#
# print(y_predicted_labels[:5])
