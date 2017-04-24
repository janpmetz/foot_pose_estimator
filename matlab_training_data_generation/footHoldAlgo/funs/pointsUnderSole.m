function [ xfoot, yfoot, zfoot, X, Y, Z ] = pointsUnderSole(Terrain, Foot)
%TERRAINUNDERFOOT returns the terrain points directly under the foot sole
% additionally X, Y, Z a matrix of the rectangular area AROUND the sole

[XTerra, YTerra, ZTerra] = getMesh(Terrain);

rows = size(Foot.Sole,1)-1;
cols = size(Foot.Sole,2)-1;

xpos = Foot.x;
ypos = Foot.y;

% Foot.Sole are 0's and 1's
Z = ZTerra(xpos:xpos+rows, ypos:ypos+cols) .* Foot.Sole;
X = XTerra(xpos:xpos+rows, ypos:ypos+cols);
Y = YTerra(xpos:xpos+rows, ypos:ypos+cols);

% only consider points within the foot shape for convex hull
x = X(:); y = Y(:); z = Z(:);

xfoot = x(Foot.ptsInFootIdx);
yfoot = y(Foot.ptsInFootIdx);
zfoot = z(Foot.ptsInFootIdx);

end

