function [ t1,t2,t3,t4,t5 ] = splitdata( data, target )
%SPLITDATA Summary of this function goes here
%   Detailed explanation goes here

t1 = [data(1:20,:) target(1:20)];
t2 = [data(21:40,:) target(21:40)];
t3 = [data(41:60,:) target(41:60)];
t4 = [data(61:79,:) target(61:79)];
t5 = [data(80:98,:) target(80:98)];


end

