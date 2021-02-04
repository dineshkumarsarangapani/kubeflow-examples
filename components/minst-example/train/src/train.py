#!/usr/bin/env python3
import json
import pickle
import argparse

from tensorflow.python import keras


def train(data_path, model_file):
    # func_to_container_op requires packages to be imported inside of the function.

    # Download the dataset and split into training and test data.
    fashion_mnist = keras.datasets.fashion_mnist

    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    # Normalize the data so that the values all fall between 0 and 1.
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    # Define the model using Keras.
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10)
    ])

    model.compile(optimizer='adam',
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    # Run a training job with specified number of epochs
    model.fit(train_images, train_labels, epochs=10)

    # Evaluate the model and print the results
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    print('Test accuracy:', test_acc)
    metrics = {
        'metrics': [
            {
                'name': 'accuracy-score',  # The name of the metric. Visualized as the column name in the runs table.
                'numberValue': test_acc,  # The value of the metric. Must be a numeric value.
                'format': "RAW",
                # The optional format of the metric. Supported values are "RAW" (displayed in raw format) and "PERCENTAGE" (displayed in percentage format).
            },
            {
                'name': 'test-loss',  # The name of the metric. Visualized as the column name in the runs table.
                'numberValue': test_loss,  # The value of the metric. Must be a numeric value.
                'format': "RAW",
                # The optional format of the metric. Supported values are "RAW" (displayed in raw format) and "PERCENTAGE" (displayed in percentage format).
            }
        ]
    }
    with open('/mlpipeline-metrics.json', 'w') as f:
        json.dump(metrics, f)

    # Save the model to the designated
    model.save(f'{data_path}/{model_file}')

    # Save the test_data as a pickle file to be used by the predict component.
    with open(f'{data_path}/test_data', 'wb') as f:
        pickle.dump((test_images, test_labels), f)


# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='Training for Minst')
parser.add_argument('--data-path', type=str,
                    help='Path of the local file.')  # Paths should be passed in, not hardcoded
parser.add_argument('--model-file', type=str, help='Model file name')
args = parser.parse_args()

train(args.data_path, args.model_file)
