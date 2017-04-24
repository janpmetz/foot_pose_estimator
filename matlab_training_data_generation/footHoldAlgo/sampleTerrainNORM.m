function [ T ] = sampleTerrainNORM( rows, cols )
%SAMPLETERRAIN samples terrain from under the foot sole
% returns a matrix of points
    
    randSpikes = randn(rows,cols);
    
    smoothingFilter = ones(9,9)/81;
    %smoothingFilter = ones(3,3)/9;
    %smoothingFilter = ones(4,4)/16;
    %smoothingFilter = ones(5,5)/25;

    sum1 = cumsum(randSpikes,1);
    edgyTerrain = cumsum(sum1,2);

    for i=1:10
        edgyTerrain = funnyFlip(edgyTerrain);
    end
    
    smoothTerrain = conv2(edgyTerrain, smoothingFilter, 'same');

    % shift to positive
    smoothTerrain = smoothTerrain - min(min(smoothTerrain));
    
    % scale
    smoothTerrain = smoothTerrain ./ max(max(smoothTerrain));
    %smoothTerrain = smoothTerrain .* 2;
    %smoothTerrain = smoothTerrain .* 7;
    
    
%     figure()
%     hold on
%     axis equal
%     view(3)
%     surf(smoothTerrain);

    assert( max(max(smoothTerrain))==1, 'wrong normalization, max not 1')
    assert( min(min(smoothTerrain))==0, 'wrong normalization, min not 0')
    T = smoothTerrain;

end



