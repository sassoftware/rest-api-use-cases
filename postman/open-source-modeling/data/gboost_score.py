import pandas as pd
import numpy as np
import pickle

def computeScore(LOAN, MORTDUE, VALUE, YOJ, DEROG, DELINQ, CLAGE, NINQ, CLNO, DEBTINC):
    "Output: P_BAD1, P_BAD0"

    modelFile = ''/tmp/gboost_obj_3_6_5.pkl''
    model = open(modelFile, ''rb'')
    dtree = pickle.load(model)
    model.close()

    input_list=[LOAN, MORTDUE, VALUE, YOJ, DEROG, DELINQ, CLAGE, NINQ, CLNO, DEBTINC]

    # Just to make sure there's no None value in the data
    # convert any of None to 0 if any
    converted = [0 if v is None else v for v in input_list]

    prob = dtree.predict_proba([converted])

    P_BAD0 = prob[0,0]
    P_BAD1 = prob[0,1]
    #print("Probability of bad loan " + str(P_BAD1) + ", and of good loan " + str(P_BAD0))

return P_BAD1, P_BAD0
