load('IrisTest2014.dt');
load('IrisTrain2014.dt');

[train0,train1,train2] = partitionData(IrisTrain2014);

uk = mean(IrisTrain2014(:,1:2));

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
    
    if IrisTrain2014(i,3) ~= t - 1,
        errorsTest(IrisTest2014(i,3) + 1) = errorsTest(IrisTest2014(i,3) + 1) + 1;
    end
end

TrainN = [bsxfun(@rdivide,IrisTrain2014(:,1:2),sum(IrisTrain2014(:,1:2))) IrisTrain2014(:,3)];
TestN = [bsxfun(@rdivide,IrisTest2014(:,1:2),sum(IrisTest2014(:,1:2))) IrisTest2014(:,3)];



[train0,train1,train2] = partitionData(TrainN);
[test0,test1,test2] = partitionData(TestN);


uk = mean(TrainN(:,1:2));

mean0 = mean(train0(:,1:2));
mean1 = mean(train1(:,1:2));
mean2 = mean(train2(:,1:2));

%Sigma = cov(vertcat(train0(:,1:2),train1(:,1:2),train2(:,1:2)));

p0 = log(length(train0) / length(TrainN));
p1 = log(length(train1) / length(TrainN));
p2 = log(length(train2) / length(TrainN));

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
    
    
    if IrisTest2014(i,3) ~= t - 1,
        errorsTestN(IrisTest2014(i,3) + 1) = errorsTestN(IrisTest2014(i,3) + 1) + 1;
    end
end
