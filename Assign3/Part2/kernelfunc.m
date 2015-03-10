function [ k ] = kernelfunc( x, z, g )
%KERNELFUNC Summary of this function goes here
%   Detailed explanation goes here

% 4 = gamma

    k = exp(sqrt(1 / (2 * g ))*  norm(x-z)^2);



end

