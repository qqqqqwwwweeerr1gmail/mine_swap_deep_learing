
dataset = []

for i in range(100000):
    if i % 7 == 0:
        dataset.append(('丽丽', '美女'))
    else:
        dataset.append(('东东', '丑男'))


images = [x[0] for x in dataset]
labels = [x[1] for x in dataset]

print(images)
print(labels)


train_images = images[:90000]
test_images = images[90000:]
train_labels = labels[:90000]
test_labels = labels[90000:]


print(train_images[:10])
print(test_images[:10])
print(train_labels[:10])
print(test_labels[:10])

train_images = images[:90000]
test_images = images[90000:]
train_labels = labels[:90000]
test_labels = labels[90000:]

import numpy as np

outfile = './create_dataset.npz'

np.savez(outfile, xtr=train_images, ytr=train_labels, xte=test_images, yte=test_labels)

data = np.load(outfile)

train_images = data['xtr']
test_images = data['ytr']
train_labels = data['xte']
test_labels = data['yte']

print(train_images[:10])
print(test_images[:10])
print(train_labels[:10])
print(test_labels[:10])
print(type(train_images))

















