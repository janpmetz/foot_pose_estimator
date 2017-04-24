
% run prototype script

s=dbstatus;
save('myBreakpoints.mat', 's');
clear all
load('myBreakpoints.mat');
dbstop(s);

display = 1;    % show plots

%fileName = 'feet\foot1.png';
%fileName = 'feet\foot2.png';
fileName = 'feet\bigfoot.png';

[ XTerra, YTerra, ZTerra ] = getTerrain(display);

%also cool:
%surf(conv2(ones(9,9)/81,cumsum(cumsum(randn(100,100)),2)))

rows = 40; cols = 40;   % foot size
[ Foot, ptsInFootIdx ] = getFoot( fileName, rows, cols, display);

% position of foot on terrain and desired zmp
xpos = 0; ypos = 0;
zmp = [15, 20];
[ xfoot, yfoot, zfoot, X, Y, Z ] = terrainUnderFoot(XTerra, YTerra, ZTerra, Foot, ptsInFootIdx, xpos, ypos);


K = convhull([xfoot, yfoot, zfoot], 'simplify', true);

% the contact triangle (returns contact points and coefficients of plane through them)
[ c1, c2, c3, a, b, c, d, tri] = getContactTriangle( K, zmp, xfoot, yfoot, zfoot );

showPlots( X, Y, Z, xfoot, yfoot, zfoot, K, zmp, tri, c1, c2, c3, display )

% the angles
[ roll, pitch ] = getAngles( a, b, c, d, xfoot(tri), yfoot(tri), zfoot(tri), display);
% old version for some plots:
getAngles_old( a, b, c, d, xfoot(tri), yfoot(tri), zfoot(tri), display);

%disp(roll);
%disp(pitch);

