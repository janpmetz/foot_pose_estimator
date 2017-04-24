
% first import the csv target column y manually
y = VarName36;

cols = 36;

[B,IX] = sort(y);

% round to next 10
B = round( B / 10 ) * 10;

minBinSize = numel(y);
for i = 5:-1:0
    c = i+1;
    idxs{c} = IX(B == i*10);
    binSize = numel(idxs{c});
    if(binSize < minBinSize)
            minBinSize = binSize;
    end
end

% all indexes
allIdxs = [];
for i = 1:numel(idxs)
    xs = idxs{i};
    allIdxs = [allIdxs; xs(1:minBinSize)];
end
allIdxs = sort(allIdxs);
allIdxs = allIdxs-1;


% now you have the indices, read those rows from the big file now
% Using sscanf, once per line
ROWS = [];
lineCount = 0; %start at 0 bc of the header
idxCount = 1;
tic;
fid = fopen('data/DATA_Zsole_500000_160417_013835.csv');
tline = fgetl(fid);
while ischar(tline) && idxCount <= numel(allIdxs)
    if(lineCount == allIdxs(idxCount))
            row = str2num(tline);
            ROWS = [ROWS; row];
            idxCount = idxCount+1;
    end
    lineCount = lineCount+1;
    tline = fgetl(fid);
end
fclose(fid);
t = toc;

hist(ROWS(:,36))

dlmwrite( 'data/equalDataDistr500k.csv' , ROWS ,'-append','delimiter', ',', 'newline', 'pc')

debug=1;



