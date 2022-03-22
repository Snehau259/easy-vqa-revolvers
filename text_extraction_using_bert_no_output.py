# -*- coding: utf-8 -*-
"""Text extraction using bert no output.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Sg8aEuGdUNp0bVanEuoSMi6KyGfxYA5K
"""

!pip install simpletransformers

from simpletransformers.language_representation import RepresentationModel
def text_feature_extraction(sentences):
  

    """**SENTENCE EMBEDDINGS**"""

    model = RepresentationModel(
            model_type="bert",
            model_name="bert-base-uncased",
            use_cuda=False
        )
    sentence_vectors = model.encode_sentences(sentences, combine_strategy="mean")

    print("sentence vector shape",sentence_vectors.shape)

    print("sentence vector",sentence_vectors)
    print("sentence vector[1]",sentence_vectors[1])

#     sentence_vectors[1]