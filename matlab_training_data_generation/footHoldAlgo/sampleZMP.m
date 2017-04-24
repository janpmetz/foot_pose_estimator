function [ xZmp, yZmp ] = sampleZMP(FootObj, show)
% randomly sample a zmp from within the 2D - convex hull of the foot shape
% bc if the zmp is outside of the convex hull 
% the foot hold is not stable

%imshow(FootObj.Sole);
[X, Y, Z] = getMesh(FootObj.Sole);

x = X(:); y = Y(:); z = Z(:);
xfoot = x(FootObj.ptsInFootIdx);
yfoot = y(FootObj.ptsInFootIdx);
zfoot = z(FootObj.ptsInFootIdx); % only for plotting needed.

K = convhull([xfoot, yfoot], 'simplify', true);

% get a mask of points that are in the convex hull of the 
% 2D foot shape (not to confuse with the convex hull used later)
IN = inpolygon(X, Y, xfoot(K), yfoot(K));

% indices of points in the hull
[rowIdx, colIdx] = find(IN > 0);

pointsWithin = [rowIdx, colIdx];

randIdx = randi([1 size(pointsWithin,1)],1,1);
xZmp = pointsWithin(randIdx, 2);
yZmp = pointsWithin(randIdx, 1);


% just checking if it does the right thing
% figure()
% plot(xfoot(K), yfoot(K), 'r-', xfoot, yfoot, 'b+', xZmp, yZmp, 'or', 'MarkerSize', 10);


% plot all points within hull
if(show)    
    figure()
    plot(xfoot(K), yfoot(K), 'r-', xfoot, yfoot, 'b+', pointsWithin(:,2), pointsWithin(:,1), 'or', 'MarkerSize', 10);
end

end



