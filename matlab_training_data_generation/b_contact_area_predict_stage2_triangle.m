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
% 3. Calculate the contact area triangle that contains the zmp
% 
% 4. store it in a file


%%%%%%%%%%%%%%%%%%%
% Configuration

n = 10000;          % number of training pairs to generate

showPlots = 1;

fileNameFootShape = 'feet/bigfoot.png';

resultFileString = 'data/DATA_hull_multi_triangles_';

% Foot shape size (a rectangle around the foot)
rows = 20;
cols = 20;

%%%%%%%%%%%%%%%%%%%


% result file name
myTimeStamp = datestr(now, 'yymmdd_HHMMSS'); % for easier sorting in file sys
outputFileName = strcat(resultFileString,num2str(n),'_',myTimeStamp,'.csv');

% load foot shape
[ Foot ] = getFoot( fileNameFootShape, rows, cols);

% decide on foot position, here trivial because
% generated terrain is as big as the foot shape size
Foot.x = 1;
Foot.y = 1;

% generate a batch of training pairs before writing them to file (faster)
batch = 1000;
numCols = (rows * cols * 2) + 2;
ROWS = zeros(batch, numCols);

%addHeadersToCSV(numCols, outputFileName)

batchCount = 1;

disp('Generating training pairs now. Output file:')
disp(outputFileName)
disp('This will take some time...')


for i = 1:n    
    [ Terrain ] = sampleTerrainStages(rows);

    [zmpX, zmpY] = sampleZMP(Foot, ~showPlots);
    Foot.relativeZmp = [zmpX, zmpY];
   
    Foot.absoluteZmp = [zmpX + Foot.x-1, zmpY + Foot.y-1]; % move zmp together with foot position
    
    [ Foot.xfoot, Foot.yfoot, Foot.zfoot, Foot.X, Foot.Y, Foot.Z ] = pointsUnderSole(Terrain, Foot);

    [hullClsMap] = getFootHold_contact_area_triangle(Terrain, Foot);   
    
    ZData = Foot.Z;
    
    row = [ZData(:); hullClsMap(:); Foot.absoluteZmp(:)];
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

