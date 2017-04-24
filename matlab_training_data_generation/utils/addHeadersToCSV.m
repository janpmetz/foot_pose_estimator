function [] = addHeadersToCSV( numAttributes, outputFileName )
%ADDHEADERSTOCSV add headers for csv file
% atr000001 ....

    % 
    %nAttribs = size(Foot.Z(:),1) + 1;
    
    attr = [];
    for i = 1:numAttributes-1
        attr = [attr, strcat('atr',sprintf('%06d' ,i),',')];
    end
    attr = [attr, strcat('atr',sprintf('%06d' ,numAttributes),'\r\n')];
    
    fid = fopen(outputFileName, 'w');
    fprintf(fid, attr);
    fclose(fid);

end

