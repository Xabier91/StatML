mu = [1;2];
cov = [0.3, 0.2 ; 0.2, 0.2];

L = chol(cov,'lower');
z = randn(2,100);

y = bsxfun(@plus,mu,L * z)

figure(1)
scatter(z(1,:),z(2,:))
figure(2)
scatter(y(1,:),y(2,:))

figure(3)
hold on

scatter(y(1,:),y(2,:),'cyan')

my1 = mean(y(1,:))
my2 = mean(y(2,:))
scatter(my1,my2,72,'blue','+')
scatter(1,2,72,'red','+')

hold off

mu = [my1 ; my2];

ynew = bsxfun(@minus,y,mu) * bsxfun(@minus,y,mu)';
ycov = ynew / 100;

[v,d] = eig(ycov);

mu + sqrt(d(1,1)) * v(:,1)
mu + sqrt(d(2,2)) * v(:,2)


