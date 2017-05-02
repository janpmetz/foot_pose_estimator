%%%%%%%%%%%%%%%%%%%
%
% This script generates training data pairs and writes them to a csv file
% 
% Using uneven terrain with non-convex foot shapes
% 
% 1. Generate random uneven terrain patch
% 
% 2. Extract points under foot sole
% 
% 3. Calculate how the foot stands on the ground using a convex hull algorithm
% 
% 4. store it in a file


%%%%%%%%%%%%%%%%%%%
% Configuration

n = 50000;                          % number of training pairs to generate

showPlots = 1;                      % show plots for testing and debugging

fileNameFootShape = 'feet/bigfoot.png';

resultFileString = 'data/DATA_CNN_10_10_nozmp_Stages_';

% Foot shape size (a rectangle around the foot)
rows = 10;
cols = 10;

%%%%%%%%%%%%%%%%%%%

% result file name
myTimeStamp = datestr(now, 'yymmdd_HHMMSS');    % for easier file sorting
outputFileName = strcat(resultFileString,num2str(n),'_',myTimeStamp,'.csv');

% load foot shape
[ Foot ] = getFoot(fileNameFootShape, rows, cols);

% decide on foot position, here trivial because
% generated terrain is as big as the foot shape size
Foot.x = 1;
Foot.y = 1;

% generate a batch of training pairs before writing them to file (faster)
batch = 1000;
numCols = rows*cols * 3; 
ROWS = zeros(batch, numCols);

%addHeadersToCSV(numCols, outputFileName)

batchCount = 1;

disp('Generating training pairs now. Output file:')
disp(outputFileName)

for i = 1:n    
    
    [ Terrain ] = sampleTerrainNORM(rows, cols);

    % Just put the ZMP in the middle of the foot shape
    zmpX = floor(rows/2);
    zmpY = floor(cols/2);
    %[zmpX, zmpY] = sampleZMP(Foot, showPlots);
    
    Foot.relativeZmp = [zmpX, zmpY];
    Foot.absoluteZmp = [zmpX + Foot.x-1, zmpY + Foot.y-1];
    
    % get points under the sole and store them in the Foot obj
    % zfoot are indices of the ponits
    % Foot.Z is a matrix of points
    [ Foot.xfoot, Foot.yfoot, Foot.zfoot, Foot.X, Foot.Y, Foot.Z ] = pointsUnderSole(Terrain, Foot);

    % c1 - c3 contact points
    [c1, c2, c3, roll, pitch, yaw, cvxHullEdgePts, solutionFound] = getFootHold_edgePoints(Terrain, Foot, showPlots);   
    
    if(isnan(pitch)) % || pitch>10 optionally filter out of range pitches
     	continue 
    end
        
    % Matrix that includes the contact points (like a heat map)
    Y = zeros(rows, cols);
    Y(c1(2), c1(1)) = c1(3); % rows and cols are now x and y, therefore switch 2 and 1
    Y(c2(2), c2(1)) = c2(3);
    Y(c3(2), c3(1)) = c3(3);
    
    % assemble the training pair row
    row = [Foot.Z(:); cvxHullEdgePts(:); Y(:)];
    
    ROWS(batchCount,:) = row';
    
    % write to file if batch is full
    if( mod(i,batch) == 0 ) 
       disp(i)
       dlmwrite( outputFileName , ROWS ,'-append','delimiter', ',', 'newline', 'pc')
       batchCount = 1;
    else
       batchCount = batchCount +1;
    end
    
end
