TrainN1 = ((IrisTrain2014(:,1)) - minTrain(1)) /  (maxTrain(1) - minTrain(1));
TrainN2 = ((IrisTrain2014(:,2)) - minTrain(2)) /  (maxTrain(2) - minTrain(2));

TestN1 = ((IrisTest2014(:,1)) - minTrain(1)) /  (maxTrain(1) - minTrain(1));
TestN2 = ((IrisTest2014(:,2)) - minTrain(2)) /  (maxTrain(2) - minTrain(2));
