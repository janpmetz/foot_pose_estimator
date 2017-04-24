%%%%%%%%%%%%%%%%%%%
%
% This script generates training data pairs and writes them to a hdf5 file
% 
% Using uneven terrain with non-convex foot shapes
% 
% 1. Generate random uneven terrain patch
% 
% 2. Extract points under foot sole
% 
% 3. Calculate roll, pitch and the contact points for this terrain & zmp
% 
% 4. store it in a files


%%%%%%%%%%%%%%%%%%%
% Configuration

n = 50000;      % number of training pairs to generate

showPlots = 1;

fileNameFootShape = 'feet/bigfoot.png';

resultFileString = 'data/DATA_ps_';

% Foot shape size (a rectangle around the foot)
rows = 30;
cols = 30;

%%%%%%%%%%%%%%%%%%%


% result file name
myTimeStamp = datestr(now, 'yymmdd_HHMMSS'); % for easier sorting in file sys
outputFileName = strcat(resultFileString,num2str(n),'_',myTimeStamp,'.h5');

% load foot shape
[ Foot ] = getFoot( fileNameFootShape, rows, cols);

% decide on foot position
% here trivial bc terrain is generated that fits directly under foot
Foot.x = 1;
Foot.y = 1;

% generate a batch of training pairs before writing them to file (faster)
batch = 1000;
numCols = (rows*cols) + 2 + 5 +1; % Z, zmp, roll, pitch, c1s, c2s, c3s, oldMax(to rescale pitch)
ROWS = zeros(batch, numCols);

h5create(outputFileName,'/data',[Inf numCols],'ChunkSize',[5 5]);

batchCount = 1;

disp('Generating training pairs now. Output file:')
disp(outputFileName)
disp('This will take some time...')


for i = 1:n    
    [ Terrain, oldMax ] = sampleTerrainStages_max(rows);

    [zmpX, zmpY] = sampleZMP(Foot, ~showPlots);
    Foot.relativeZmp = [zmpX, zmpY];
   
    Foot.absoluteZmp = [zmpX + Foot.x-1, zmpY + Foot.y-1]; % move zmp together with foot position
    
    [ Foot.xfoot, Foot.yfoot, Foot.zfoot, Foot.X, Foot.Y, Foot.Z ] = pointsUnderSole(Terrain, Foot);

    [ c1, c2, c3, roll, pitch, yaw, solutionFound ] = getFootHold( Terrain, Foot, ~showPlots);
    
    if(isnan(pitch))
       continue 
    end
    
    ZData = Foot.Z;
    
    makeSkalar = @(c)(((c(1)-1)*cols) + c(2));
    c1s = makeSkalar(c1);
    c2s = makeSkalar(c2);
    c3s = makeSkalar(c3);
    
    row = [ZData(:); Foot.absoluteZmp(:); roll; pitch; c1s; c2s; c3s; oldMax];
    ROWS(batchCount,:) = row';
    
    % write to file if batch is full
    if( mod(i,batch) == 0 ) 
       disp(i)
       %dlmwrite( outputFileName , ROWS ,'-append','delimiter', ',', 'newline', 'pc')
       h5write(outputFileName,'/data', ROWS ,[i-batch+1 1], [batch numCols]);
       batchCount = 1;
    else
       batchCount = batchCount +1;
    end
    
end

h5disp(outputFileName);




