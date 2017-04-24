function [] = showPlots( X, Y, Z, xfoot, yfoot, zfoot, Foot, K, zmp, tri, c1, c2, c3, Terrain )


% figure()
% hold on;
% title('Convex hull of terrain under foot')
% xlabel('X-Axis');
% ylabel('Y-Axis');
% zlabel('Z-Axis');
% view(3);
% surf(X, Y, Z, 'facealpha', 0.2);
% % plot triangles of convex hull
% trisurf(K, xfoot, yfoot, zfoot, 'Facecolor', 'b', 'facealpha', 0.5);
% % edge points of triangles
% scatter3(xfoot(K(:,1)), yfoot(K(:,1)), zfoot(K(:,1)), 'filled', 'MarkerFaceColor','red');
 
figure()
subplot(1,2,1)
hold on;
title('Terrain and foot points projected on ground')
xlabel('X-Axis');
ylabel('Y-Axis');
zlabel('Z-Axis');
view(3);
%figure(); 
surf(Terrain,  'facealpha', 0.5);
hold on;
plot3(xfoot, yfoot, zfoot, 'o', 'MarkerSize', 10, 'MarkerFaceColor', 'red')
hold on; 
scatter3(Foot.absoluteZmp(1), Foot.absoluteZmp(2), 5, 300, 'filled', 'MarkerFaceColor','green');

subplot(1,2,2)
%figure()
hold on;
title('Contact points, plane through points, ZMP')
xlabel('X-Axis');
ylabel('Y-Axis');
zlabel('Z-Axis');
view(3);
surf(X, Y, Z, 'facealpha', 0.2);
% plot big red ball for zmp
scatter3(zmp(1), zmp(2), 5, 300, 'filled', 'MarkerFaceColor','red');
trisurf(tri, xfoot, yfoot, zfoot, 'Facecolor', 'b', 'facealpha', 0.5);
markerSize = 200;
scatter3(c1(1), c1(2), c1(3), markerSize, 'filled', 'MarkerFaceColor','green');
scatter3(c2(1), c2(2), c2(3), markerSize, 'filled', 'MarkerFaceColor','green');
scatter3(c3(1), c3(2), c3(3), markerSize, 'filled', 'MarkerFaceColor','green');


end

