################################################################
#
# Note: This is not the main model we were working with (see similar_images_model.py). 
#       This file was used for testing efficientNet implementation. It works but does
#       not perform very well.     
#
################################################################

import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB0

# ssl workaround: bad coding practice fix this moving forward
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import pathlib
data_dir = pathlib.Path('similar foods small sample')

image_count = (len(list(data_dir.glob('*/*.png'))) + 
               len(list(data_dir.glob('*/*.jpg'))) + 
               len(list(data_dir.glob('*/*.jpeg'))))
print(image_count)

batch_size = 1
img_height = 224
img_width = 224

ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = ds.class_names
num_classes = len(class_names)
validation_split = .2

# initiallizing val_ds and train_ds as "empty" arrays
val_ds = ds.filter(lambda x, l: tf.math.equal(l[0], num_classes + 1))
train_ds = ds.filter(lambda x, l: tf.math.equal(l[0], num_classes + 1))

# we want validation representation from each class
# however, its very small dataset so we can't rely on random validation sampling
# assign validation images evenly from each class
# gaurantee that there is at least one validation image for each class
for i in range(num_classes):
    filtered_ds = ds.filter(lambda x, l: tf.math.equal(l[0], i))
  
    fds_list = list(filtered_ds)
    val_count = len(fds_list) // (1/validation_split)

    # gaurantee that there is at least one validation image for each class
    if val_count == 0:
      val_count = 1

    if len(fds_list) > 0:
      val_ds = val_ds.concatenate(filtered_ds.take(val_count))
      train_ds = train_ds.concatenate(filtered_ds.skip(val_count))

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]

data_augmentation = keras.Sequential(
  [
    layers.RandomFlip("horizontal",
                      input_shape=(img_height,
                                  img_width,
                                  3)),
    layers.RandomRotation(0.15),
    layers.RandomZoom(0.1),
  ]
)

def build_model(num_classes):
    inputs = layers.Input(shape=(img_height, img_width, 3))
    x = data_augmentation(inputs)
    model = EfficientNetB0(include_top=False, input_tensor=x, weights="imagenet")

    # Freeze the pretrained weights
    model.trainable = False

    # Rebuild top
    x = layers.GlobalAveragePooling2D(name="avg_pool")(model.output)
    x = layers.BatchNormalization()(x)

    top_dropout_rate = 0.1
    x = layers.Dropout(top_dropout_rate, name="top_dropout")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="pred")(x)

    # Compile
    model = tf.keras.Model(inputs, outputs, name="EfficientNet")
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-2)
    model.compile(
        optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    return model

strategy = tf.distribute.MirroredStrategy()

with strategy.scope():
    model = build_model(num_classes=num_classes)

epochs=120
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)
'''
test_img_path = pathlib.Path('test images/shredded wheat.jpeg')

img = tf.keras.utils.load_img(
    test_img_path, target_size=(img_height, img_width)
)

img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)
'''

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
