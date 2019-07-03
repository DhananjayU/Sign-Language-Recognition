# Sign-Language-Recognition
This project is a sign language alphabet recognizer using Python, openCV and tensorflow for training a modified AlexNet model, a convolutional neural network model for classification.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to install Opencv, tensorflow, sklearn, keras, numpy and matplotlib for running the code.

If you are using anaconda package manager

You can install these packages using following commands:
```
conda install -c conda-forge opencv
conda install -c conda-forge keras
conda install -c conda-forge tensorflow
conda install -c conda-forge matplotlib
conda install -c anaconda scikit-learn 

```
### Installing

To run the code to recognize sign language alphabets using webcam run the web.py file using following command

```
python web.py
```
To run the code on a single image of a sign language alphabet run the following command
```
python predict.py -ip [image path]```
```
To train the model on any other or the same dataset

```
python model.py --base_path [path to the dataset directory] 
                --val_split [validation split] 
                --batch_size [Batch size]
                --k_fold [k value for k fold validation] 
                --epochs [number of epochs] 
                --dropout [value for dropout for dense layers] 
                --learning_rate [learning rate]
```

## Built With

* [Jupyter Notebook](https://jupyter.org/install) - IDE used

