mu = [1;2];
cov = [0.3, 0.2 ; 0.2, 0.2];

L = chol(cov,'lower');
z = randn(2,100);

y = bsxfun(@plus,mu,L * z)

figure(1)
scatter(z(1,:),z(2,:))
figure(2)
scatter(y(1,:),y(2,:))
