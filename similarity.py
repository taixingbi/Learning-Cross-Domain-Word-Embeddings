# rank2frequency
class zipf(object):
    def __init__(self, ranks):
        self.ranks= ranks
        
    def frequency(self):
        #print (self.rank)        
        f= {}
        N= 0
        
        for word, rank in self.ranks:
            freq= 1.0/rank
            f[word]= freq
            #N += freq
        print f['the']
        #for word in f: f[word] /= N
        #print(f)
        return f

#target
import gensim
import operator

class CorpusRank(object): # normalized 
    def __init__(self, filename):
        self.filename = filename
        self.MAX_SENTENSE_SIZE= 1000 # in general 15-20 words
        
    def iter(self):
        print("reading target domain and tokenization", self.filename)
        i = 0
        for line in open(self.filename):
            i += 1
            if i % 1000000 == 0:
                print "processed %s lines" % str(i)
            #print(sentense)
            #if len(sentense) > self.MAX_SENTENSE_SIZE:    continue
            #for token in gensim.utils.tokenize(sentense, encoding='utf8',to_lower=True):    yield token 
            yield line.strip().split('\t')
                
    def rank(self):
        dic= {}
        
        print("computing target domain rank...")
        for line in self.iter():
            #print(word)
            for word in line:
                if word not in dic:    
                    dic[word]= 0
                dic[word] += 1
        
        # sort by dictionary value 
        sorted_tuple = sorted(dic.items(), key=operator.itemgetter(1),reverse=True)
        
        l_rank= []
        rank= 1
        for key, val in sorted_tuple:
            l_rank.append( (key, rank) )
            rank+= 1

            
        print("numeber of tokens:",rank)
        return l_rank

#source
from gensim.models import word2vec
from gensim.models import KeyedVectors

class WvRank(object): # normalized 
    def __init__(self, filename):
        self.filename = filename
        
    def read_file(self):
        print("loading source model...")
        model= KeyedVectors.load_word2vec_format(self.filename, binary=True)
        print( self.filename + " model dimentional is", model.vector_size)
        return model
    
    def rank(self):
        dic= {}
        rank= []       
        print("computing source domain frequnecy...")
        i = 0
        for word, vocab_obj in self.read_file().vocab.items():   
            i += 1
            if i % 100000 == 0:
                print "processed %s words" % str(i)
            dic[word]= vocab_obj.count
        
        N= len(dic)
        print("number of dictionary:", N)
        for word in dic: rank.append( (word, N+1-dic[word]) )
        
        return rank
   

class SimilarityScore(object): 
    def __init__(self, f1, f2, freq1, file_name):
        self.f1 = f1
        self.f2 = f2
        self.freq1 = freq1
        self.file_name = file_name
    
    def save(self):
        outF = open(self.file_name, "w")
        score= {}
        for w in [_[0] for _ in freq1]:
            if w in f1 and w in f2:
                score[w]= 2*f1[w]*f2[w]/(f1[w] + f2[w])
                outF.write('$'+ w +'$' + ' ' + '$'+ str(score[w])+'$')
                outF.write("\n")
        outF.close()
        print(self.file_name, "has been saved")

        
target= '/home/kungangli/alternativeData/earningsCall/word2vec_selfTrained/word2vecTrainCorpus.txt'
#target= 'corpus.txt'
#target= '1000000_lines.txt'

#source= 'GoogleNews-vectors-negative300.bin'        
#source= '10000_lines.bin'
source= 'wv2glove.6B.300d.bin' 

freq1= CorpusRank(target).rank()     
freq2= WvRank(source).rank() 
print 'the freq: ', freq1[0:10], freq2[0:10]
f1, f2= zipf(freq1).frequency(), zipf(freq2).frequency()
SimilarityScore(f1, f2, freq1, '_similarity_score.txt').save()
