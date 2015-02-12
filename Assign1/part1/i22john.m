mu = [1;2];
cov = [0.3, 0.2 ; 0.2, 0.2];

L = chol(cov,'lower');
z = randn(2,100);

y = bsxfun(@plus,mu,L * z);

figure(1)
scatter(z(1,:),z(2,:))
figure(2)
scatter(y(1,:),y(2,:))

figure(3)
clf;
hold on

scatter(y(1,:),y(2,:),'cyan')

my1 = mean(y(1,:));
my2 = mean(y(2,:));
scatter(my1,my2,72,'blue','+')
scatter(1,2,72,'red','+')

mu = [my1 ; my2];

ynew = bsxfun(@minus,y,mu) * bsxfun(@minus,y,mu)';
ycov = ynew / 100;

[v,d] = eig(ycov);

sv1 = mu + sqrt(d(1,1)) * v(:,1);
sv2 = mu + sqrt(d(2,2)) * v(:,2);



quiver(mu(1,1),mu(2,1),sv1(1,1),sv1(2,1));
quiver(mu(1,1),mu(2,1),sv2(1,1),sv2(2,1));

%plot(sv1)
%plot(sv2)

hold off
