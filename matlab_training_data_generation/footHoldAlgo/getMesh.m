function [ X, Y, Z ] = getMesh( Z )
% generates a meshgrid from the matrix Z

% grid vectors
ygv = 1 : size(Z,1);    % the rows are y
xgv = 1 : size(Z,2);

[X,Y] = meshgrid(xgv, ygv);

end

