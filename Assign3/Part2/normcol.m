function [ ncol ] = normcol( X,Y )

X=X-mean(Y(:));
ncol=X/std(Y(:));


end

