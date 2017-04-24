function [ c1, c2, c3, a, b, c, d, k] = getContactTriangle2( K, zmp, x, y, z )
% find triangle that contains desired zmp in matrix of triangles K
% K contains the triangles that form the convex hull
% return contact points and plane coefficients
% several triangles could match, "bottom triangle" or "top triangle"
% select the one with highest z value at zmp

% maybe no solution is found, then c's will be []

planeCoeffs = [];
p1s = [];
p2s = [];
p3s = [];
ks = [];            % k index of matching triangles

% iterate triangles
for i = 1:size(K,1)
   tri = K(i, :);
   
   xvals = x(tri);
   yvals = y(tri);
   zvals = z(tri);
   
   % zmp in triangle? Use mex function inPolygon to find out
   %[in, on] = inpolygon(zmp(1), zmp(2), xvals, yvals);
   %in = inhull([zmp(1), zmp(2)], [xvals yvals]);
   %in = intriangle([xvals, yvals], [zmp(1), zmp(2)]);
   [in,ON,IN_strict] = InPolygon(zmp(1), zmp(2),  xvals, yvals);
   
   if(in)
       
       % three points of the triangle
       p1 = [x(tri(1)), y(tri(1)), z(tri(1))];
       p2 = [x(tri(2)), y(tri(2)), z(tri(2))];
       p3 = [x(tri(3)), y(tri(3)), z(tri(3))];
       
       normal = cross(p3-p1, p2-p1); % Calculate plane normal
       
       % Find all coefficients of plane equation A*x+B*y+C*z+D=0 
       A = normal(1); B = normal(2); C = normal(3);
       D = -dot(normal,p1);
       
       % save coefficients and triangle if this triangle contains zmp
       planeCoeffs = [planeCoeffs; [A, B, C, D]];
       p1s = [p1s; p1];
       p2s = [p2s; p2];
       p3s = [p3s; p3];
       ks = [ks; tri];
   end
          
end

c1 = [];
c2 = [];
c3 = [];
k = [];
a = 0;
b = 0;
c = 0;
d = 0;

if(size(planeCoeffs,1) ~= 0)
    % select which triangle is the highest at zmp
    zfun = @(x,y,a,b,c,d) (a.*x + b.*y +d)./(-c);
    zmpVals = zfun(zmp(1),zmp(2), planeCoeffs(:,1), planeCoeffs(:,2), planeCoeffs(:,3), planeCoeffs(:,4));
    [m, ix] = max(zmpVals);
    k = ks(ix,:);

    % contact points
    c1 = [p1s(ix, 1), p1s(ix, 2), p1s(ix, 3)];
    c2 = [p2s(ix, 1), p2s(ix, 2), p2s(ix, 3)];
    c3 = [p3s(ix, 1), p3s(ix, 2), p3s(ix, 3)];

    % plane coefficients
    a = planeCoeffs(ix,1);
    b = planeCoeffs(ix,2);
    c = planeCoeffs(ix,3);
    d = planeCoeffs(ix,4);
end



end

