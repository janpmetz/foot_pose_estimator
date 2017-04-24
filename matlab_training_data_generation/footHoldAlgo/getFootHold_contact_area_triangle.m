function [ hullClsMap ] = getFootHold_contact_area_triangle(Terrain, Foot)
%GETFOOTHOLDANGLES calculates the hold of the foot on that terrain
%   returns a map of the contact area in form of a triangle
    
    %[ xfoot, yfoot, zfoot, X, Y, Z ] = pointsUnderSole(Terrain, Foot);
    xfoot = Foot.xfoot;
    yfoot = Foot.yfoot;
    zfoot = Foot.zfoot;
    X = Foot.X;
    Y = Foot.Y;
    Z = Foot.Z;
    
    K = convhull([xfoot, yfoot, zfoot], 'simplify', true);  
       
    %only one triangle
    hullClsMap = hullClsMaps_contact_area_triangle(K, Foot, xfoot, yfoot, zfoot, size(Terrain));
    
end

