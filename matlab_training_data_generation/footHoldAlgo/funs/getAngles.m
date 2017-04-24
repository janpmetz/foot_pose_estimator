function [ roll, pitch ] = getAngles( a, b, c, d, xtri, ytri, ztri, display)
%GETANGLES calcualte roll and pitch angles of a plane

planeFun = @(x,y)( a.*x + b.*y +d)./(-c);
norm = @(v) sqrt(v(1)^2 + v(2)^2 + v(3)^2);

% u and v as "comparison" lines in x and y dir, the axes to compare
u1 = [5,0, planeFun(5,0)];
u2 = [10,0, planeFun(10,0)];
u = u2-u1;

v1 = [0,5, planeFun(0,5)];
v2 = [0,10, planeFun(0,10)];
v = v2-v1;

u = u ./ norm(u);
v = v ./norm(v);

% U AND V NOT ORTHOGONAL!

angle = @(a,b) atan2(norm(cross(a,b)),dot(a,b));
roll = rad2deg(angle([1,0,0], u));
pitch = rad2deg(angle([0,1,0], v));


% TODO put this somewhere else
% display?
if nargin == 8
    if display== 0 
        return;
    end

    p1 = [xtri(1), ytri(1), ztri(1)];
    p2 = [xtri(2), ytri(2), ztri(2)];
    p3 = [xtri(3), ytri(3), ztri(3)];

    axis equal; % otherwise angles and distances look skewed
    
    scale = 5;
    quiver3(p1(1), p1(2), p1(3), u(1), u(2), u(3), scale, 'k', 'linewidth',2)
    quiver3(p1(1), p1(2), p1(3), v(1), v(2), v(3), scale, 'k', 'linewidth',2)

    % plot coordinate system arrows in (0,0,0)
    quiver3(p1(1), p1(2), p1(3), 1, 0, 0, scale, 'r', 'linewidth',2)
    quiver3(p1(1), p1(2), p1(3), 0, 1, 0, scale, 'g', 'linewidth',2)
    quiver3(p1(1), p1(2), p1(3), 0, 0, 1, scale, 'b', 'linewidth',2)
    
    
    
    % make a seperate plot with the coordinate systems
    figure()
    hold on;
    title('3d coordinate systems, orientation of foot');
    axis equal;
    
    scale = 5;
    % plot coordinate system arrows in (0,0,0)
    quiver3(0, 0, 0, 1, 0, 0, scale, 'k', 'linewidth',2)
    quiver3(0, 0, 0, 0, 1, 0, scale, 'k', 'linewidth',2)
    quiver3(0, 0, 0, 0, 0, 1, scale, 'k', 'linewidth',2)

    quiver3(0, 0, 0, u(1), u(2), u(3), scale, 'r', 'linewidth',3)
    quiver3(0, 0, 0, v(1), v(2), v(3), scale, 'g', 'linewidth',3)
    
end

end

