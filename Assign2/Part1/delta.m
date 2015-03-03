function [ y ] = delta( x, uk, cov, p )
%DELTA Summary of this function goes here
%   Detailed explanation goes hereUntitled

foo = x * inv(cov) * uk';
bar = 0.5 * uk * inv(cov) * uk';
y =  foo - bar + p;




end

