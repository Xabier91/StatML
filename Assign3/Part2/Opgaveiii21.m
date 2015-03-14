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

C = [0.01, 0.1, 1, 10, 100, 1000, 10000];
Gamma = [0.0000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1];

errors = zeros(7,7,5);


[t1,t2,t3,t4,t5] = splitdata(traindata,traintarget);

sel1 = [t2 ; t3 ; t4 ; t5];
sel2 = [t1 ; t3 ; t4 ; t5];
sel3 = [t1 ; t2 ; t4 ; t5];
sel4 = [t1 ; t2 ; t3 ; t5];
sel5 = [t1 ; t2 ; t3 ; t4];


for k=1:5
    switch k
        case 1
            test = t1;
            train = sel1;
        case 2
            test = t2;
            train = sel2;
        case 3
            test = t3;
            train = sel3;
        case 4
            test = t4;
            train = sel4;
        case 5
            test = t5;
            train = sel5;
    end
    
    for i=1:7
        for j=1:7

            model = svmtrain(train(:,1:22),train(:,23),'boxconstraint',C(i),'autoscale',false,'kernel_function', @(u,v) exp(-Gamma(j) .* pdist2(u,v,'euclidean').^2));
            tresult = svmclassify(model,test(:,1:22));
            errors(k,i,j) = sum(tresult + test(:,23) == 1);

        end
    end
end

errsum = squeeze(sum(errors));

[bC, bGamma] = find(errsum==min(min(errsum)),1);

Gamma(bGamma)
C(bC)

model = svmtrain(traindata,traintarget,'boxconstraint',C(bC),'autoscale',false,'kernel_function', @(u,v) exp(-Gamma(bGamma) .* pdist2(u,v,'euclidean').^2));
tresult = svmclassify(model,traindata);
traincrossvalerror = sum(tresult + traintarget == 1);

tresult = svmclassify(model,testdata);
testcrossvalerror = sum(tresult + testtarget == 1);

trainerror = traincrossvalerror / length(traindata)
testerror = testcrossvalerror / length(testdata)

%Normalized

errors = zeros(7,7,5);


[t1,t2,t3,t4,t5] = splitdata(normtrain,traintarget);

sel1 = [t2 ; t3 ; t4 ; t5];
sel2 = [t1 ; t3 ; t4 ; t5];
sel3 = [t1 ; t2 ; t4 ; t5];
sel4 = [t1 ; t2 ; t3 ; t5];
sel5 = [t1 ; t2 ; t3 ; t4];


for k=1:5
    switch k
        case 1
            test = t1;
            train = sel1;
        case 2
            test = t2;
            train = sel2;
        case 3
            test = t3;
            train = sel3;
        case 4
            test = t4;
            train = sel4;
        case 5
            test = t5;
            train = sel5;
    end
    
    for i=1:7
        for j=1:7

            model = svmtrain(train(:,1:22),train(:,23),'boxconstraint',C(i),'autoscale',false,'kernel_function', @(u,v) exp(-Gamma(j) .* pdist2(u,v,'euclidean').^2));
            tresult = svmclassify(model,test(:,1:22));
            errors(k,i,j) = sum(tresult + test(:,23) == 1);

        end
    end
end

errsum = squeeze(sum(errors));

[bC, bGamma] = find(errsum==min(min(errsum)),1);

Gamma(bGamma)
C(bC)

model = svmtrain(normtrain,traintarget,'boxconstraint',C(bC),'autoscale',false,'kernel_function', @(u,v) exp(-Gamma(bGamma) .* pdist2(u,v,'euclidean').^2));
tresult = svmclassify(model,normtrain);
ntraincrossvalerror = sum(tresult + traintarget == 1);

tresult = svmclassify(model,normtest);
ntestcrossvalerror = sum(tresult + testtarget == 1);

ntrainerror = ntraincrossvalerror / length(traindata)
ntesterror = ntestcrossvalerror / length(testdata)


