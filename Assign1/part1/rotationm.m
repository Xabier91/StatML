function [ rm ] = rotationm( degree )
%ROTATIONM Summary of this function goes here
%   Detailed explanation goes here

rm = [cosd(degree), -sind(degree) ; sind(degree), cosd(degree)];
end

