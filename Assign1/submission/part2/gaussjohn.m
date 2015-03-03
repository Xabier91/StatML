function [ f ] = gaussjohn( mu, sigma )
%GAUSSJOHN Summary of this function goes here
%   Detailed explanation goes here
    a = 1 / (sigma * sqrt(2 * pi));
    f = @(x) a * exp(-((x - mu)^2) / (2 * sigma^2));

end

