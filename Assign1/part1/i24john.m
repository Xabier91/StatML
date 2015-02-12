mu = [my1 ; my2];

ynew = bsxfun(@minus,y,mu) * bsxfun(@minus,y,mu)';
ycov = ynew / 100;

[v,d] = eig(ycov);

mu + sqrt(d(1,1)) * v(:,1)
mu + sqrt(d(2,2)) * v(:,2)
