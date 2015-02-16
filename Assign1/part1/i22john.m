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
axis equal;

scatter(y(1,:),y(2,:),'cyan')

my1 = mean(y(1,:));
my2 = mean(y(2,:));
scatter(my1,my2,72,'blue','+')
scatter(1,2,72,'red','+')

mu = [my1 ; my2];

ynew = bsxfun(@minus,y,mu) * bsxfun(@minus,y,mu)';
ycov = ynew / 100;

[v,d] = eig(ycov);



%sv1 = mu + sqrt(d(1,1)) * v(:,1);
%sv2 = mu + sqrt(d(2,2)) * v(:,2);

v1 = sqrt(d(1,1)) * v(:,1);
v2 = sqrt(d(2,2)) * v(:,2);




quiver(1,2,v1(1,1),v1(2,1));
quiver(1,2,v2(1,1),v2(2,1));

%quiver(mu(1,1),mu(2,1),sv1(1,1),sv1(2,1));
%quiver(mu(1,1),mu(2,1),sv2(1,1),sv2(2,1));

%plot(sv1)
%plot(sv2)

hold off

% I.2.4
rm = rotationm(30);
rcov30 = rm^-1 * ycov * rm;

rm = rotationm(60);
rcov60 = rm^-1 * ycov * rm;

rm = rotationm(90);
rcov90 = rm^-1 * ycov * rm;

y30 = bsxfun(@plus,mu,rcov30 * z);
y60 = bsxfun(@plus,mu,rcov60 * z);
y90 = bsxfun(@plus,mu,rcov90 * z);


figure(4)
clf;
hold on

rm = rotationm(40)
rcovnew = rm^-1 * ycov * rm;
ynew = bsxfun(@plus,mu,rcovnew * z);

scatter(y30(1,:),y30(2,:),'yellow')
scatter(y60(1,:),y60(2,:),'blue')
scatter(y90(1,:),y90(2,:),'red')
scatter(ynew(1,:),ynew(2,:),'green')

figure(5)
clf;
rm = rotationm(40)
rcovnew = rm^-1 * ycov * rm;
ynew = bsxfun(@plus,mu,rcovnew * z);


scatter(ynew(1,:),ynew(2,:),'blue')
rm = rotationm(45)
rcovnew = rm^-1 * ycov * rm;
ynew = bsxfun(@plus,mu,rcovnew * z);


scatter(ynew(1,:),ynew(2,:),'green')
axis equal
