show = 1;

% Foot
fileName = 'feet\bigfoot.png';
rows = 10;
cols = 10;
[ Foot ] = getFoot( fileName, rows, cols);
Foot.x = 1;
Foot.y = 1;

n = 10000;

ROLL = [];
PITCH = [];


for i = 1:n
    [ Terrain ] = sampleTerrain(rows, cols);

    [zmpX, zmpY] = sampleZMP(Foot, ~show);
    Foot.relativeZmp = [zmpX, zmpY];
    Foot.absoluteZmp = [zmpX + Foot.x-1, zmpY + Foot.y-1];
    
    [ Foot.xfoot, Foot.yfoot, Foot.zfoot, Foot.X, Foot.Y, Foot.Z ] = pointsUnderSole(Terrain, Foot);

    [roll, pitch, yaw, solutionFound] = getFootHoldAngles(Terrain, Foot, ~show);
    
    ROLL = [ROLL; roll];
    PITCH = [PITCH; pitch];

end


debug =1;

figure()
hold on
subplot(1,2,1)
hold on
title('distribution of roll in dataset')
hist(ROLL);
subplot(1,2,2)
hold on
title('distribution of pitch in dataset')
hist(PITCH);




