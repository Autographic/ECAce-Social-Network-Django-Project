from socialnetwork.constants import *

##########
# 2-level Item Weighting
#
# Item weights from 0 through 10
#MIN_WEIGHT = 0
#DEFAULT_WEIGHT = 5
#MAX_WEIGHT = 10

WEIGHTS_COARSE = WEIGHTS_FINE = [ [i,i] for i in range ( MIN_WEIGHT, MAX_WEIGHT + 1 ) ]
# customize some labels...
WEIGHTS_COARSE[MIN_WEIGHT][1] = "Lightest [%d]" % MIN_WEIGHT
WEIGHTS_COARSE[DEFAULT_WEIGHT][1] = "Default [%d]" % DEFAULT_WEIGHT
WEIGHTS_COARSE[MAX_WEIGHT][1] = "Heaviest [%d]" % MAX_WEIGHT

WEIGHTS_FINE[MIN_WEIGHT][1] = "Lighter [%d]" % MIN_WEIGHT
WEIGHTS_FINE[DEFAULT_WEIGHT][1] = "Default [%d]" % DEFAULT_WEIGHT
WEIGHTS_FINE[MAX_WEIGHT][1] = "Heavier [%d]" % MAX_WEIGHT

# Recursively tuple-ize the list of lists for performance
WEIGHTS_COARSE = tuple([ tuple(i) for i in WEIGHTS_COARSE ])
WEIGHTS_FINE = tuple([ tuple(i) for i in WEIGHTS_FINE ])


