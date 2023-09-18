from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
import numpy as np

# prepare input data
def prepare_inputs(X_train, X_test):
    oe = OrdinalEncoder()
    oe.fit(X_train)
    X_train_enc = oe.transform(X_train)
    X_test_enc = oe.transform(X_test)
    return X_train_enc, X_test_enc


# prepare target
def prepare_targets(y_train, y_test):
    le = LabelEncoder()
    le.fit(y_train)
    y_train_enc = le.transform(y_train)
    y_test_enc = le.transform(y_test)
    return y_train_enc, y_test_enc

dataset = []

for i in range(100000):
    if i % 7 == 0:
        dataset.append(('丽丽', '美女'))
    else:
        dataset.append(('东东', '丑男'))

images = [x[0] for x in dataset]
labels = [x[1] for x in dataset]

# print(images)
# print(labels)

train_images = [[x] for x in images[:90000]]
test_images = [[x] for x in images[90000:]]
train_labels = [[x] for x in labels[:90000]]
test_labels = [[x] for x in labels[90000:]]

print(train_images[:10])
print(test_images[:10])
print(train_labels[:10])
print(test_labels[:10])

# train_images = np.array(train_images)
# test_images = np.array(test_images)
# train_labels = np.array(train_labels)
# test_labels = np.array(test_labels)

train_images, test_images = prepare_targets(train_images, test_images)
train_labels, test_labels = prepare_targets(train_labels, test_labels)

print(train_images.shape)

print(train_images[:10])
print(test_images[:10])
print(train_labels[:10])
print(test_labels[:10])

import keras

# define the model
# model = keras.Sequential()
# model.add(Dense(9, input_dim=train_images.shape[1], activation='relu', kernel_initializer='he_normal'))
# model.add(Dense(9, input_dim=train_images.shape[1], activation='relu', kernel_initializer='he_normal'))
# model.add(Dense(9, input_dim=train_images.shape[1], activation='relu', kernel_initializer='he_normal'))
# model.add(Dense(9, input_dim=train_images.shape[1], activation='relu', kernel_initializer='he_normal'))
# model.add(Dense(1, activation='sigmoid'))

model = keras.Sequential([
    # keras.layers.Dense(1, input_shape=(1,), activation='relu'),
    keras.layers.Dense(1, input_shape=(1,), activation='relu'),
    # keras.layers.Dense(1, input_shape=(1,), activation='tanh'),
    # keras.layers.Dense(1, input_shape=(1,), activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

epochs_num = 1

acc_list = []

for i in range(epochs_num):
    model.fit(train_images, train_labels, epochs=1)
    test_labels = model.predict(test_images)
    # print('y_predicted',y_predicted)
    loss, acc = model.evaluate(test_images, test_labels, verbose=1)
    print('Restored model, accuracy: {:5.2f}%'.format(100 * acc))
    acc_list.append('Restored model, accuracy: {:5.2f}%'.format(100 * acc))



    model.evaluate(test_images, test_labels)

    model.save('./ws_model1.h5')

    model.summary()

    weights = model.get_weights()  # Getting params
    print(weights)

    a_weights = [np.array([[0.0155494]], dtype='float32'),np.array([0.5], dtype='float32')]
    print(a_weights)
    model.set_weights(a_weights)


    y_predicted = model.predict(test_images)
    print(test_images[:20])
    print(y_predicted[:20])