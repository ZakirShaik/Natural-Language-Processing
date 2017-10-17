#!/usr/bin/env python

from optparse import OptionParser
import os, logging
import utils, collections
import re

def create_model(sentences):
    model = None
        ## YOUR CODE GOES HERE: create a model
    transition = collections.defaultdict(lambda:collections.defaultdict(float))
    individual_count = collections.defaultdict(int)
    likelihood = collections.defaultdict(lambda:collections.defaultdict(float))
    
    for sentence in sentences:
        previous = "<s>"
        individual_count[previous]+=1
        for token in sentence:

            ## Counting the transition, individual and likelihood items.
            transition[previous][token.tag]+=1
            individual_count[token.tag]+=1
            likelihood[token.tag][token.word]+=1
            previous = token.tag
        transition[previous]["</s>"]+=1
        #Assigning Probabilities for transition.
    for key,value in transition.items():
        for key2,value2 in value.items():
            #Laplace smoothing is done here...
            value[key2]=(value[key2]+1)/float(individual_count[key])
        #Assigning Probabilities for likelihood.
    for key,value in likelihood.items():
        for key2,value2 in value.items():
            value[key2]=value[key2]/float(individual_count[key])

    model=transition,individual_count,likelihood
    return model

def predict_tags(sentences, model):
    ## YOU CODE GOES HERE: use the model to predict tags for sentences
    ## Create the Viterbi matrix, fill the matrix, etc.
    viterbi = collections.defaultdict(lambda:collections.defaultdict(float))
    possible_tags = list()
    transition = model[0]
    likelihood = model[2]
    counting = 0
    for sentence in sentences:
        print("%d"%(counting))
        counting+=1

        for token in sentence: # Splitting line into words
            possible_tags.append(token.tag)

        j = 0 #To check whether first token is executed or not
        for token in sentence:
            
            if j == 0:
                start_tag = '<s>'
                
                for tag in possible_tags:
                    viterbi[tag][token.word] = likelihood[tag][token.word]*transition[start_tag][tag]
                    #viterbi[]
                prev_word = token.word
                j+=1
                prev_tag = token.tag
            if j > 0: 
                ##unknown words
                prob_w_t = 0.0
                if token.word != likelihood[token.tag].keys():
                    if token.word[:1].isupper():
                            token.tag = 'NNP'
                    if token.word.strip()[-2:] == 'ed':
                        token.tag = 'VBD'
                    m = re.match("^\d+$",token.tag)
                    if m:
                       token.tag = 'CD'
                    prob_w_t += 1
                    prob_w_t /= float(model[1][token.tag])
                    model[1][token.tag] += 1
                    likelihood[token.tag][token.word] = (prob_w_t * model[1][token.tag])/float(transition[prev_tag][token.tag]+1.0)


                total_max = 0.0
                for main_tag in possible_tags:
                    max_val = 0.0
                    for tag in possible_tags:
                        viterbi[tag][token.word] = viterbi[tag][prev_word]*likelihood[main_tag][token.word]*transition[tag][main_tag]
                        if viterbi[tag][token.word] > max_val:
                            max_val = viterbi[tag][token.word]
                            token.tag = main_tag
                j+=1
            prev_word = token.word
            prev_tag = token.tag
        possible_tags.clear()
        viterbi.clear()
            ## you can access token.word and self.tag (see utils.py for details)
            #token.tag = "NN"
    return sentences


if __name__ == "__main__":
    usage = "usage: %prog [options] GOLD TEST"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug", action="store_true",
                      help="turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("Please provide required arguments")

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    training_file = args[0]
    training_sents = utils.read_tokens(training_file)
    test_file = args[1]
    test_sents = utils.read_tokens(test_file)

    model = create_model(training_sents)

    ## read sentences again because predict_tags(...) rewrites the tags
    sents = utils.read_tokens(training_file)
    predictions = predict_tags(sents, model)
    accuracy = utils.calc_accuracy(training_sents, predictions)
    print ("Accuracy in training [%s sentences]: %s" % (len(sents), accuracy))

    ## read sentences again because predict_tags(...) rewrites the tags
    sents = utils.read_tokens(test_file)
    predictions = predict_tags(sents, model)
    accuracy = utils.calc_accuracy(test_sents, predictions)
    print ("Accuracy in testing [%s sentences]: %s" % (len(sents), accuracy))

