function [ pointMap ] = hullClsMaps(K, x, y, z, terrainSize, Z)

pointMap = zeros(terrainSize);

n = numel(pointMap);
pointIndices = 1:n;
classCount = 1;

px = 1:terrainSize(1);
py = 1:terrainSize(2);
[X, Y] = meshgrid(px,py);
pxpy = [X(:) Y(:)];


for i = 1:size(pxpy,1)
    planeCoeffs = [];
    p1s = [];
    p2s = [];
    p3s = [];
    ks = [];
    kj = [];
    
    for j = 1:size(K,1)
        tri = K(j, :);
        xvals = x(tri);
        yvals = y(tri);
        zvals = z(tri);
        
        [in,on,inStrict] = InPolygon(pxpy(i,1), pxpy(i,2), xvals, yvals);
        %ptsIn = find(in > 0);
        %ptsOn = find(on > 0);
        %ptsinStrict = find(inStrict > 0);

        if(in)
            % three points of the triangle
            p1 = [x(tri(1)), y(tri(1)), z(tri(1))];
            p2 = [x(tri(2)), y(tri(2)), z(tri(2))];
            p3 = [x(tri(3)), y(tri(3)), z(tri(3))];

            normal = cross(p3-p1, p2-p1); % Calculate plane normal

            % Find all coefficients of plane equation A*x+B*y+C*z+D=0 
            A = normal(1); B = normal(2); C = normal(3);
            D = -dot(normal,p1);

            planeCoeffs = [planeCoeffs; [A, B, C, D]];
            p1s = [p1s; p1];
            p2s = [p2s; p2];
            p3s = [p3s; p3];
            ks = [ks; tri];
            kj = [kj;j];
        end
       
    end
    
    if(size(planeCoeffs,1)>0)
        zfun = @(x,y,a,b,c,d) (a.*x + b.*y +d)./(-c);
        pVals = zfun(pxpy(i,1),pxpy(i,2), planeCoeffs(:,1), planeCoeffs(:,2), planeCoeffs(:,3), planeCoeffs(:,4));
        [m, ix] = max(pVals);
        k = ks(ix,:);
        pointMap(pxpy(i,1), pxpy(i,2)) = kj(ix);
    end
end

pointMap = pointMap';

end

