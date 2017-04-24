function [ c1, c2, c3, roll, pitch, yaw, hullEdgeMap, solutionFound ] = getFootHold_edgePoints(Terrain, Foot, show)
%GETFOOTHOLDANGLES calculates the hold of the foot on that terrain
%   returns roll pitch yaw
    
    %[ xfoot, yfoot, zfoot, X, Y, Z ] = pointsUnderSole(Terrain, Foot);
    xfoot = Foot.xfoot;
    yfoot = Foot.yfoot;
    zfoot = Foot.zfoot;
    X = Foot.X;
    Y = Foot.Y;
    Z = Foot.Z;
    
    K = convhull([xfoot, yfoot, zfoot], 'simplify', true);
    
    hullEdgeMap = hullEdges(K, xfoot, yfoot, zfoot, size(Terrain));

    % the contact triangle (returns contact points and coefficients of plane through them)
    [ c1, c2, c3, a, b, c, d, tri] = getContactTriangle2( K, Foot.absoluteZmp, xfoot, yfoot, zfoot );

    roll = 0;
    pitch = 0;
    yaw = 0;
    solutionFound = 0;
    
    if(size(c1,1) ~= 0) % solution found

        if(show)
            showPlots( X, Y, Z, xfoot, yfoot, zfoot, Foot, K, Foot.absoluteZmp, tri, c1, c2, c3, Terrain)
        end
        
        % the angles
        [ roll, pitch ] = getAngles( a, b, c, d, xfoot(tri), yfoot(tri), zfoot(tri), 0);

        solutionFound = 1;
        % old version for some plots:
        %getAngles_old( a, b, c, d, xfoot(tri), yfoot(tri), zfoot(tri), display);
    end
    
end

