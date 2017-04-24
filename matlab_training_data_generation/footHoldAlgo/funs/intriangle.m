function [ result ] = intriangle( candVerts, qPtXY )
%INTRIANGLE Summary of this function goes here
%   Detailed explanation goes here

% from math exchange

    % Get my N triangles' vertices into a 3-by-2-by-N shape (easier to work with)
    myVerts = permute(reshape(candVerts',2,3,[]),[2 1 3]);
    % Get unit vectors pointing from each triangle vertex to my query point
    vert2ptVecs = bsxfun(@minus, qPtXY, myVerts);
    vert2ptUVecs = bsxfun(@rdivide, vert2ptVecs, sqrt(sum(vert2ptVecs.^2,2)));
    % Get unit vectors pointing around each triangle (along edge A, edge B, edge C)
    edgeVecs = myVerts([2 3 1],:,:) - myVerts;
    edgeUVecs = bsxfun(@rdivide, edgeVecs, sqrt(sum(edgeVecs.^2,2)));
    % Get the inner product between edgeA.edgeC, edgeB.edgeA, edgeC.edgeB
    edgeEdgeDotPs = sum(edgeUVecs .* -edgeUVecs([3 1 2],:,:),2);
    % Get the inner product between each edge unit vec and the unit vect from qPt to vertex
    edgeQPntDotPs = sum(edgeUVecs .* vert2ptUVecs,2);
    qPntEdgeDotPs = sum(vert2ptUVecs .* -edgeUVecs([3 1 2],:,:),2);
    % If both inner products 2 edges to the query point are greater than the inner product between
    % the two edges themselves, the query point is between the V shape made by the two edges. If
    % this is true for all 3 edge pair, the query point is inside the triangle.
    result = squeeze(all(edgeQPntDotPs>edgeEdgeDotPs & qPntEdgeDotPs>edgeEdgeDotPs,1));
end

