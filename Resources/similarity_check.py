import nltk
import os
from email.parser import Parser
import math
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import gensim
from gensim.models.doc2vec import TaggedDocument

# rootdir = "C:\\Users\\rohit\\Downloads\\enron_mail_20150507.tar\\enron_mail_20150507\\maildir\\lay-k\\"

class Similarity:

    stopwords_en = stopwords.words("english")
    def __init__(self,rec_mail,email_dir):
        
        self.recived_mail = rec_mail
        self.similirity_list = list()
        self.rootdir = email_dir
        self.top5 = list()

    def preprocessing(self,raw):
        wordlist = nltk.word_tokenize(raw)
        text = [w.lower() for w in wordlist if w not in self.stopwords_en]
        return text

    def email_analyse(self,inputfile):

        with open(inputfile,"r") as f:
            data2=f.read()
    
        email2 = Parser().parsestr(data2)


        text1 = self.preprocessing(self.rec_mail.replace("\n",""))
        text2 = self.preprocessing(email2.get_payload().replace("\n",""))

        word_set = set(text1).union(set(text2))

        freqd_text1 = FreqDist(text1)
        text1_count_dict = dict.fromkeys(word_set,0)
        for word in text1:
            text1_count_dict[word] = freqd_text1[word]

        freqd_text2 = FreqDist(text2)
        text2_count_dict = dict.fromkeys(word_set,0)
        for word in text2:
            text2_count_dict[word] = freqd_text2[word]
        
        freqd_text1 = FreqDist(text1)
        text1_length = len(text1)
        text1_tf_dict = dict.fromkeys(word_set,0)
        for word in text1:
            text1_tf_dict[word] = freqd_text1[word]/text1_length

        freqd_text2 = FreqDist(text2)
        text2_length = len(text2)
        text2_tf_dict = dict.fromkeys(word_set,0)
        for word in text2:
            text2_tf_dict[word] = freqd_text2[word]/text2_length
        
        text12_idf_dict = dict.fromkeys(word_set,0)
        text12_length = 2

        for word in text12_idf_dict.keys():
            if word in text1:
                text12_idf_dict[word] += 1
            if word in text2:
                text12_idf_dict[word] += 1
        
        for word, val in text12_idf_dict.items():
            text12_idf_dict[word] = 1 + math.log(text12_length/(float(val)))
        
        text1_tfidf_dict = dict.fromkeys(word_set,0)
        for word in text1:
            text1_tfidf_dict[word] = (text1_tf_dict[word]) * (text12_idf_dict[word])

        text2_tfidf_dict = dict.fromkeys(word_set,0)
        for word in text2:
            text2_tfidf_dict[word] = (text2_tf_dict[word]) * (text12_idf_dict[word])
        
        taggeddocs = list()
        doc1 = TaggedDocument(words=text1,tags= ["Mail_1"])
        taggeddocs.append(doc1)
        doc2 = TaggedDocument(words=text2,tags= ["Mail_2"])
        taggeddocs.append(doc2)

        model = gensim.models.Doc2Vec(taggeddocs,dm=0,alpha=0.025,vector_size=20,min_alpha=0.025,min_count=0)
        token_count = sum([len(sentence) for sentence in taggeddocs])
        for epoch in range(80):
            if epoch % 20 ==0:
                print("Now training epoch %s" %epoch)
            model.train(taggeddocs,total_examples = token_count, epochs = 80)
            model.alpha -= 0.002
            model.min_alpha = model.alpha
        
        v1 = list(text1_tfidf_dict.values())
        v2 = list(text2_tfidf_dict.values())

        similarity = 1 - nltk.cluster.cosine_distance(v1,v2)
        self.similirity_list.append(similarity)
        print("Similarity Index: {:4.2f} %".format(similarity*100))



    def check_similarity(self):
        for directory, subdirectory,filenames in os.walk(self.rootdir):
            for filename in  filenames:
                try:
                    self.email_analyse(os.path.join(directory,filename))
                except:
                    print(os.path.join(directory,filename))
        
    def display_similarities(self):
        for i in range (5):
            self.top5.append(max(self.similirity_list))
            self.similirity_list.remove(max(self.similirity_list))
        print(self.top5)