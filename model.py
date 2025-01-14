from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPooling2D, Flatten, Multiply
from tensorflow.keras.optimizers import Adam
import numpy as np 
import matplotlib.pyplot as plt
import glob
import cv2
import tensorflow as tf
from keras.models import Model, Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
import os
import seaborn as sns
from keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.resnet50 import ResNet50
from keras import models
from keras import layers

def build_model(im_shape, vocab_size, num_answers, big_model):
  # The CNN
  im_input = Input(shape=im_shape)
  x1 = VGG16(weights='imagenet', include_top=False, input_shape=(250, 250, 3))(im_input)
  x1 = tf.keras.layers.GlobalMaxPooling2D()(x1)
  x1 = tf.keras.layers.Dense(512, activation='relu')(x1)
  print("shape of x1",x1.shape)
  # The question network
  q_input = Input(shape=(768,))
  x2 = Dense(512, activation='tanh')(q_input)
  x2 = Dense(512, activation='tanh')(x2)
  print("shape of x2",x2.shape)
  print("type of x1 and x2", type(x1), type(x2))

  def attention(x1, x2, dropout=True):
    
    IQ = tf.nn.tanh(x1 + x2)

    print("IQ shpe: ", IQ.shape)
     
    if dropout:
        IQ = tf.nn.dropout(IQ , rate=1 - (0.5))
    
    temp = Dense(1)(IQ)
    
    temp = tf.reshape(temp , [-1,temp.shape[1]])
    print("temp shpe: ", temp.shape)
    
    p = tf.nn.softmax(temp)
    print("p shpe: ", p.shape)
    
    p_exp = tf.expand_dims(p , axis = -1)
    
    att_layer = tf.reduce_sum(input_tensor=p_exp * x1 , axis = 1)
    print("attlay shpe: ", att_layer.shape)
    
    final_out = att_layer + x2
        
    return p , final_out

  att_l1 , att = attention(x1, x2)
    
  att_l2 , att = attention(x1, att)
    
  att = tf.nn.dropout(att , rate=1 - (0.4)
  print("att shpe: ", att.shape)
    
  print(att.shape)
    
  attention_layers = [att_l1 , att_l2]

  out = Dense(512, activation='tanh')(att)
  out = Dense(num_answers, activation='softmax')(out)
  print("out shape: ", out.shape)
  print("im_input shpe: ", im_input.shape)

  model = Model(inputs=[im_input, q_input], outputs=out)
  model.compile(Adam(lr=5e-4), loss='categorical_crossentropy', metrics=['accuracy'])

  return model
