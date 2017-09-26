#!/usr/bin/env python

from optparse import OptionParser
import os, logging, re
import collections
import math 
import codecs


def preprocess(line):
    ## get rid of the staff at the end of the line
    line = line.rstrip()
    ## lower case
    line = line.lower()
    ## remove everything except characters and white space
    line = re.sub("[^a-z ]", '', line)

    tokens = line.split()

    tokens = ['$$'+token+'$$' for token in tokens]
    
    return tokens



def create_model(path):
    bigrams = collections.defaultdict(lambda: collections.defaultdict(int))
    ##Created nested defaultdicts for trigrams
    trigrams = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
    trigram_prob = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(float)))

    #used codecs and utf8 encoding to open files other than english.
    f = codecs.open(path, 'r', encoding = "utf-8")
    ## Shouldn't visit a token more than once
    for l in f.readlines():
        tokens = preprocess(l)
        if len(tokens) == 0:
            continue
        for token in tokens:
            for i in range(0, len(token)):
                ## Counting bigrams and trigrams.
                if i > 0:
                    bigrams[token[i-1]][token[i]] += 1
                if i > 1:
                    trigrams[token[i-2]][token[i-1]] [token[i]] += 1       
            pass
        
        # Calculating trigram probabilities using trigrams and bigrams.
    for k,v in trigrams.items():
        for k2,v2 in v.items():
            for k3,v3 in v2.items():
                trigram_prob [k] [k2] [k3] = abs(math.log((1.0+trigrams[k][k2][k3])/(bigrams[k][k2]+26.0)))



    ## return the actual model    
    return trigram_prob,bigrams

def predict(file, model_en, model_es):
    prediction = None
    prob_eng = 0.00
    prob_esp = 0.00
    f = codecs.open(file, encoding = "utf-8")
    for l in f.readlines():
        tokens = preprocess(l)
        if len(tokens) == 0:
            continue
        ## Calculating probabilities to predict the language.
        prob_eng += calc_prob(tokens, model_en)
        prob_esp += calc_prob(tokens, model_es)
    ##print("english probabilities: %.2f"%(prob_eng))
    ##print("spanish probabilities: %.2f"%(prob_esp))
    if prob_eng > prob_esp:
        prediction = "English"
    elif prob_esp > prob_eng :
        prediction = "Espanol"
    elif prob_esp == prob_eng:
        prediction = "Cannot decide."

    return prediction

def calc_prob(tokens, model):
    prob = 0.00
    tri_prob = model[0]
    bigrams = model[1]
    for token in tokens:
        for i in range(0,len(token)-2):
            ## Assigning the probability values. 
           if tri_prob[token[i]][token[i+1]][token[i+2]] in tri_prob.values():
              prob += tri_prob[token[i]][token[i+1]][token[i+2]]
           else:
              prob += abs(math.log10(1/(bigrams[token[i]][token[i+1]] + 26)))

    return prob
        

def main(en_tr, es_tr, folder_te):
    ## DO NOT CHANGE THIS METHOD

    ## STEP 1: create a model for English with en_tr
    model_en = create_model(en_tr)
##    bigram_prob = model_en[0];
##    uni = model_en[1];
##    print("Bigram Probability values of model for english: ")
##    for k,v in bigram_prob.items():
##        print("\n%s : "%(k),end="")
##        for k2,v2 in v.items():
##            print (" %s - %.2f,"%(k2,v2),end="")
##    print("\nUnigram values of model for english: ")
##    for k,v in uni.items():
##        print("%s - %d"%(k,v))
        
##    print("\n")
    ## STEP 2: create a model for Spanish with es_tr
    model_es = create_model(es_tr)
##    bigram_prob = model_es[0];
##    uni = model_es[1];
##    print("Bigram Probability values of model for espanol: ")
##    for k,v in bigram_prob.items():
##        print("\n%s : "%(k),end="")
##        for k2,v2 in v.items():
##            print (" %s - %.2f,"%(k2,v2),end="")
##    print("\nUnigram values of model for espanol: ")
##    for k,v in uni.items():
##        print("%s - %d"%(k,v))
        
##    print("\n")

    ## STEP 3: loop through all the files in folder_te and print prediction
    folder = os.path.join(folder_te, "en")
    print ("Prediction for English documents in test:")
    for f in os.listdir(folder):
        f_path =  os.path.join(folder, f)
        print ("%s\t%s" % (f, predict(f_path, model_en, model_es)))
    
    folder = os.path.join(folder_te, "es")
    print ("\nPrediction for Spanish documents in test:")
    for f in os.listdir(folder):
        f_path =  os.path.join(folder, f)
        print ("%s\t%s" % (f, predict(f_path, model_en, model_es)))

if __name__ == "__main__":
    ## DO NOT CHANGE THIS CODE

    usage = "usage: %prog [options] EN_TR ES_TR FOLDER_TE"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug", action="store_true",
                      help="turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 3:
        parser.error("Please provide required arguments")

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    main(args[0], args[1], args[2])


