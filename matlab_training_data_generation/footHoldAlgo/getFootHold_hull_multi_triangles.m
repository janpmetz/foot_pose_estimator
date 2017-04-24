function [ hullClsMap ] = getFootHold_hull_multi_triangles(Terrain, Foot, show)
%GETFOOTHOLDANGLES calculates the hold of the foot on that terrain
%   returns a map of the convex hull, where each facet has a different class value
    
    xfoot = Foot.xfoot;
    yfoot = Foot.yfoot;
    zfoot = Foot.zfoot;
    X = Foot.X;
    Y = Foot.Y;
    Z = Foot.Z;
    
    K = convhull([xfoot, yfoot, zfoot], 'simplify', true);
    
    hullClsMap = hullClsMaps(K, xfoot, yfoot, zfoot, size(Terrain));
    
end

