import re, logging, sys, itertools
from optparse import OptionParser

def main():
    usage = "usage: %prog REGEXP_FILE INPUT_FILE"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--debug", action='store_true',
                      help="Turn on debug mode")
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("Incorrect number of arguments")
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    logging.debug("REGEXP_FILE:\t%s" % args[0])
    logging.debug("INPUT_FILE:\t%s" % args[1])
    
    ## get the regexp from the file, ignoring empty lines and "\n"
    regexp_f = open(args[0], 'r')
    regexps = []
    for regexp in regexp_f.readlines():
        regexp = regexp.rstrip()
        ## ignore empty lines and comments
        if regexp == "" or regexp[0] == "#":
            continue
        regexps.append(regexp)
    regexp_f.close()

    ## get the text for the input file
    input_f  = open(args[1], "r")
    text = input_f.readlines()
    input_f.close()

    ## find all matches and print
    for l, i in zip(text, itertools.count(1)):
        ## get rid of the "\n" at the end of the line
        l = l.rstrip()

        ## this is relatively slow, the idea is to let you know what regexp
        ## is matching
        for regexp, j in zip(regexps, itertools.count(1)):
            logging.debug("Checking regexp \"%s\" in sentence \"%s\"" % (regexp, l))
            token_dates = re.findall(regexp, l)
            for token_date in token_dates:
                print ("#%s,%s\t%s" % (i, j, token_date))
            ## skip to the next line after the first match,
            ## so make sure to write more generic regexp at the end of the file
            if token_dates: break

if __name__ == "__main__":
    main()

