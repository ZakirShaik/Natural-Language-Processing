#!/usr/bin/env python

from optparse import OptionParser
import os, logging, collections
import utils
from _ast import stmt

def create_model(sentences):
    model = None
    ## YOUR CODE GOES HERE: create a model
    individual_count = collections.defaultdict(lambda:collections.defaultdict(int))
    for sentence in sentences:
        for token in sentence:
            token.word = token.word.lower()
            individual_count[token.word][token.tag]+=1

    return individual_count

def predict_tags(sentences, model):
    individual_count = model
    possible_tags = list()
    
    for sentence in sentences:
        for token in sentence: # Splitting line into words
            possible_tags.append(token.tag)
        for token in sentence:
            maximum = 0
            # if word-tag count is maximum we will assign the tag to word
            for tag in possible_tags:
                if individual_count[token.word][tag] > maximum:
                    maximum = individual_count[token.word][tag]
                    token.tag = tag
            # if unknown tag is found then we will assign noun.
            if token.tag == 'UNK':
                print(token.word," ",token.tag)
                token.tag = "NN"
        possible_tags.clear()
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
    print ("Accuracy in training [%s sentences]: %s" % (len(sents), accuracy))

