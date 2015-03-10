load('parkinsonsTestStatML.dt');
load('parkinsonsTrainStatML.dt');

% 2.1

traindata = parkinsonsTrainStatML(:,1:22);
traintarget = parkinsonsTrainStatML(:,23);
testdata = parkinsonsTestStatML(:,1:22);
testtarget = parkinsonsTestStatML(:,23);


normtrain = zeros(size(traindata));
normtest = zeros(size(testdata));

for i=1:size(traindata,2),
    normtrain(:,i) = normcol(traindata(:,i),traindata(:,i));
    normtest(:,i) = normcol(testdata(:,i),traindata(:,i));
end


% 2.2


model = svmtrain(normtrain,traintarget,'kernel_function', @(u,v) kernelfunc(u,v,1));


