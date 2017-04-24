function [ pointMap ] = hullClsMaps_contact_area_triangle(K, Foot, x, y, z, terrainSize)

px = 1:terrainSize(1);
py = 1:terrainSize(2);

[X, Y] = meshgrid(px,py);
pxpy = [X(:) Y(:)];

[ c1, c2, c3, a, b, c, d, tri] = getContactTriangle2( K, Foot.absoluteZmp, x, y, z );

cps_x = [c1(1), c2(1), c3(1)];
cps_y = [c1(2), c2(2), c3(2)];

[in,on,inStrict] = InPolygon(pxpy(:,1), pxpy(:,2), cps_x, cps_y);

ins = reshape(in, terrainSize(1),terrainSize(2));
ins = ins+0.0000001;

pointMap = ins;

end

