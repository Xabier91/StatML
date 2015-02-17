%I.2.2
mu = [1;2];
cov = [0.3, 0.2 ; 0.2, 0.2];

L = chol(cov,'lower');
z = randn(2,100);
y = bsxfun(@plus,mu,L * z);

figure(1)
p1 = scatter(z(1,:),z(2,:));
figure(2)
p2 = scatter(y(1,:),y(2,:));

saveas(p1, 'I221.png','png');
saveas(p2, 'I222.png','png');


%I.2.3
figure(3)
clf;
hold on
axis equal;

p3 = scatter(y(1,:),y(2,:),'cyan');

my1 = mean(y(1,:));
my2 = mean(y(2,:));
scatter(my1,my2,72,'blue','+');
scatter(1,2,72,'red','+');

mu = [my1 ; my2]

% I.2.4

ynew = bsxfun(@minus,y,mu) * bsxfun(@minus,y,mu)';
ycov = ynew / 100;

[v,d] = eig(ycov);

v1 = sqrt(d(1,1)) * v(:,1);
v2 = sqrt(d(2,2)) * v(:,2);

quiver(my1,my2,v1(1,1),v1(2,1));
quiver(my1,my2,v2(1,1),v2(2,1));

saveas(p3, 'I231.png','png');
hold off


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

p4 = scatter(y30(1,:),y30(2,:),'yellow');
scatter(y60(1,:),y60(2,:),'blue')
scatter(y90(1,:),y90(2,:),'red')

figure(5)
clf;
hold on

rm = rotationm(40);

rcovnew = rm^-1 * ycov * rm;
ynew = bsxfun(@plus,mu,rcovnew * z);
p5 = scatter(ynew(1,:),ynew(2,:),'green');
axis equal

saveas(p4, 'I241.png','png');
saveas(p5, 'I242.png','png');

hold off