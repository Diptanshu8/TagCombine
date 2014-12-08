import operator
import json
import numpy as np
from sklearn.naive_bayes import MultinomialNB as mnb
import loadData
import wordvectors

def recallTest(numQuestions, clf, k):
  recallSum = 0
  for i in range(0, numQuestions):
    tagProb = clf.predict_proba(X[i])   

def multinomialNaiveBayesTrain(numQuestions, tag, X, y):
  clf = mnb()
  i = 0
  for qid in loadData.questions:
    if tag in loadData.questions[qid].tags:
      y[i] = 1
    else:
      y[i] = 0
    i += 1

  clf.fit(X,y)
  print "Fit Complete"
  i = 0
  tagProb = clf.predict_proba(X)
  for qid in loadData.questions:
    probList = recallProbs[qid]    
    probList.append((tag, tagProb[i][1]))
    sortedProbs = sorted(probList, key=operator.itemgetter(1), reverse=True)
    sortedProbs.pop()
    recallProbs[qid] = sortedProbs
    i += 1

y = np.zeros(loadData.NUM_QUESTIONS)
X = np.zeros((loadData.NUM_QUESTIONS,len(wordToIndex)))
i = 0
for qid in loadData.questions:
  X[i] = np.array(wordVecs[qid])
  i += 1

recallProbs = {}
for qid in loadData.questions:
  recallProbs[qid] = [(-1,-1), (-1,-1), (-1,-1), (-1,-1), (-1,-1), (-1,-1), (-1,-1), (-1,-1), (-1,-1), (-1,-1)]

tcount = open('tcount-50000.txt')
tagsf = json.load(tcount)

i = 0
for tag in tagsf:
  print loadData.tags[int(tag)].tag
  multinomialNaiveBayesTrain(loadData.NUM_QUESTIONS, int(tag), X, y)

recallSum = 0
for qid in loadData.questions:
  recallValue = 0
  questionTags = loadData.questions[qid].tags
  for recallTag in recallProbs[qid]:
    if recallTag[0] in questionTags:
      recallValue += 1
  recallSum += (recallValue*1.0)/len(questionTags)
print (recallSum*1.0)/loadData.NUM_QUESTIONS


