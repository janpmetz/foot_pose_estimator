function [ pointMap ] = hullEdges(K, x, y, z, terrainSize)
%return a map of all edge points of the convex hull

pointMap = zeros(terrainSize);


% iterate triangles
for i = 1:size(K,1)
   tri = K(i, :);
   
   xvals = x(tri);
   yvals = y(tri);
   zvals = z(tri);
  
   for j = 1:size(xvals,1)
          pointMap(xvals(j), yvals(j)) = zvals(j);
   end
   
end

pointMap = pointMap';

end

