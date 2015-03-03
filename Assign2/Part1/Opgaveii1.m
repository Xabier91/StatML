load('IrisTest2014.dt');
load('IrisTrain2014.dt');

[train0,train1,train2] = partitionData(IrisTrain2014);
[test0,test1,test2] = partitionData(IrisTest2014);

mean0 = mean(train0(:,1:2));
mean1 = mean(train1(:,1:2));
mean2 = mean(train2(:,1:2));

p0 = log(length(train0) / length(IrisTrain2014));
p1 = log(length(train1) / length(IrisTrain2014));
p2 = log(length(train2) / length(IrisTrain2014));

S = zeros(2,2);

for i = 1:length(train0(1,:)),
    foo = train0(i,:) - mean0;
    S = S + foo' * foo;
   
end

for i = 1:length(train1(1,:)),
    foo = train1(i,:) - mean1;
    S = S + foo' * foo;
   
end

for i = 1:length(train2(1,:)),
    foo = train2(i,:) - mean2;
    S = S + foo' * foo;
   
end

Sigma = S * (1 / 97);

errorsTrain = [0,0,0];
errorsTest = [0,0,0];

for i = 1:length(IrisTrain2014),
    tmp0 = delta(IrisTrain2014(i,1:2),mean0,Sigma,p0);
    tmp1 = delta(IrisTrain2014(i,1:2),mean1,Sigma,p1);
    tmp2 = delta(IrisTrain2014(i,1:2),mean2,Sigma,p2);
    [aadwark, t] = max([tmp0,tmp1,tmp2]);
    
    if IrisTrain2014(i,3) ~= t - 1,
        errorsTrain(IrisTrain2014(i,3) + 1) = errorsTrain(IrisTrain2014(i,3) + 1) + 1;
    end
end
    

for i = 1:length(IrisTest2014),
    tmp0 = delta(IrisTest2014(i,1:2),mean0,Sigma,p0);
    tmp1 = delta(IrisTest2014(i,1:2),mean1,Sigma,p1);
    tmp2 = delta(IrisTest2014(i,1:2),mean2,Sigma,p2);
    [aadwark, t] = max([tmp0,tmp1,tmp2]);
    
    if IrisTest2014(i,3) ~= t - 1,
        errorsTest(IrisTest2014(i,3) + 1) = errorsTest(IrisTest2014(i,3) + 1) + 1;
    end
end


errorTrainPer = sum(errorsTrain) / length(IrisTrain2014);
errorTestPer = sum(errorsTest) / length(IrisTest2014);



figure(1)
hold on
scatter(test0(:,1),test0(:,2),'red');
scatter(test1(:,1),test1(:,2),'green');
scatter(test2(:,1),test2(:,2),'blue');




minTrain = min(IrisTrain2014(:,1:2));
maxTrain = max(IrisTrain2014(:,1:2));

TrainN1 = ((IrisTrain2014(:,1)) - minTrain(1)) /  (maxTrain(1) - minTrain(1));
TrainN2 = ((IrisTrain2014(:,2)) - minTrain(2)) /  (maxTrain(2) - minTrain(2));

TestN1 = ((IrisTest2014(:,1)) - minTrain(1)) /  (maxTrain(1) - minTrain(1));
TestN2 = ((IrisTest2014(:,2)) - minTrain(2)) /  (maxTrain(2) - minTrain(2));

TrainN = [TrainN1 TrainN2 IrisTrain2014(:,3)];
TestN = [TestN1 TestN2 IrisTest2014(:,3)];

[train0,train1,train2] = partitionData(TrainN);
[test0,test1,test2] = partitionData(TestN);




mean0 = mean(train0(:,1:2));
mean1 = mean(train1(:,1:2));
mean2 = mean(train2(:,1:2));

S = zeros(2,2);
foo = 0;


for i = 1:length(train0(1,:)),
    foo = train0(i,:) - mean0;
    S = S + foo' * foo;
   
end

for i = 1:length(train1(1,:)),
    foo = train1(i,:) - mean1;
    S = S + foo' * foo;
   
end

for i = 1:length(train2(1,:)),
    foo = train2(i,:) - mean2;
    S = S + foo' * foo;
   
end

Sigma = S * (1 / 97);

errorsTrainN = [0,0,0];
errorsTestN = [0,0,0];


for i = 1:length(TrainN),
    tmp0 = delta(TrainN(i,1:2),mean0,Sigma,p0);
    tmp1 = delta(TrainN(i,1:2),mean1,Sigma,p1);
    tmp2 = delta(TrainN(i,1:2),mean2,Sigma,p2);
    [aadwark, t] = max([tmp0,tmp1,tmp2]);
    
    if IrisTrain2014(i,3) ~= t - 1,
        errorsTrainN(TrainN(i,3) + 1) = errorsTrainN(TrainN(i,3) + 1) + 1;
    end
end
    

for i = 1:length(TestN),
    tmp0 = delta(TestN(i,1:2),mean0,Sigma,p0);
    tmp1 = delta(TestN(i,1:2),mean1,Sigma,p1);
    tmp2 = delta(TestN(i,1:2),mean2,Sigma,p2);
    [aadwark, t] = max([tmp0,tmp1,tmp2]);
    
    if TestN(i,3) ~= t - 1,
        errorsTestN(TestN(i,3) + 1) = errorsTestN(TestN(i,3) + 1) + 1;
    end
end

errorTrainNPer = sum(errorsTrainN) / length(IrisTrain2014);
errorTestNPer = sum(errorsTestN) / length(IrisTest2014);



figure(2)
hold on
scatter(test0(:,1),test0(:,2),'red');
scatter(test1(:,1),test1(:,2),'green');
scatter(test2(:,1),test2(:,2),'blue');
