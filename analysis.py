from data_parser import generateTrainingData
from data_parser import generateTestingData
from data_parser import outputParser

import os
import accuracy
import polarityAccuracy

raw_train_data_path='dataset/Restaurants_Train_v2.xml'
raw_test_data_path='dataset/restaurants-trial.xml'
crf_output='generated_files/crf_output.txt'
generateTrainingData.traindatapath(raw_train_data_path)
generateTestingData.traindatapath(raw_test_data_path)
train_data_path='generated_files/train.data'
os.system("crf_learn  crf/template generated_files/train.data crf/model_file")
os.system("crf_test -m crf/model_file generated_files/test.data >generated_files/crf_output.txt ")
outputParser.write_out(crf_output)
print "Aspect Extraction Metrics:"
accuracy.evaluate('dataset/restaurants-trial.xml')
print "\nPolarity Metrics:"
polarityAccuracy.evaluate('dataset/restaurants-trial.xml')



