#!/usr/bin/env python

from optparse import OptionParser
import nltk
from nltk.corpus import treebank
from nltk.tree import ParentedTree


BIG_BAR = "################################################################################"
SMALL_BAR = "--------------------------------------------------------------------------------"

# The API for the nltk Tree module is available here: http://www.nltk.org/api/nltk.html#module-nltk.tree

# DO NOT MODIFY ANY CODE EXCEPT THE LINES INDICATED WITH "YOUR CODE GOES HERE":
################################################################################
"""
# YOUR CODE GOES HERE: return the siblings, move to the parent, collect the siblings, etc.
# ... more comments

potential_arguments = [node] <--- dummy code to get the code to run, CHANGE ONLY THESE LINES
################################################################################
"""


def get_potential_args(node):

    ################################################################################
    # YOUR CODE GOES HERE: return the siblings, move to the parent, collect the siblings, etc.
    # Useful methods you may want to use: tree.left_sibling(), tree.right_sibling(), tree.parent()

    # sily implementation, the only potential argument is the verb itself
    potential_arguments = [node]
    ################################################################################

    return potential_arguments


def main():
    ## Read a fixed file, it could really be any file
    for tree in treebank.parsed_sents('wsj_0010.mrg'):
        print BIG_BAR
        print "%s\n" % tree
        print BIG_BAR
        # Convert to ParentedTree, so we have access to the parent of any node
        tree = ParentedTree.convert(tree)
        # Step 1 is implemented for you: loop through all the leaves in the tree, ...
        for leaf in tree.subtrees(lambda st: st.height() == 2):
            # ... and skip them unless they are a verb
            if leaf.label()[0] != 'V':                
                continue
            verb = leaf

            print BIG_BAR
            print "Potential arguments of %s" % leaf
            for pot_arg in get_potential_args(verb):
                print SMALL_BAR
                print pot_arg
                print "Selected features:",

                ################################################################################
                # YOUR CODE GOES HERE: calculate the value for the features
                # Useful methods you may want to use: pot_arg.pos(), pot_arg.leaves(), pot_arg.treeposition()
                verb_word = 'UNK'
                verb_pos = 'UNK'
                arg_num_leaves = 'UNK'
                direction = 'UNK'
                ################################################################################

                print "Verb_word:", verb_word,
                print "Verb_pos:", verb_pos,
                print "arg_num_leaves:", arg_num_leaves,
                print "direction:", direction
            print


if __name__ == '__main__':
    usage = "usage: %prog"
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.error("No arguments accepted")
        
    main()
