# task:
In one single domain, some words have some special meaning, like word "option", does not really mean "choice". That is why we need transfer learning.

# process 
step 1. load pre-trained model based on wv2glove.6B.300d.bin.          
step 2. compute similarity matrix based on common words in source corpus and target corpus.          
step 3. transfer learning based on "A Simple Regularization-based Algorithm for Learning Cross-Domain Word Embeddings".     

# perefence
[1] [a simple regularization-based algorithm for learning cross-domain word embeddings](http://aclweb.org/anthology/D17-1312)







