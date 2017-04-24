function [ X, Y, Z ] = getTerrain(display)
% get a matrix with a rough terrain

[X,Y] = meshgrid(-50:50, -50:50);
Z = zeros(101,101);

scale = 0.5;
Z(1:50, 1:50) = peaks(50) .* scale;
Z(51:100, 1:50) = peaks(50) .* scale;
Z(1:50, 51:100) = peaks(50) .* scale;
Z(51:100, 51:100) = peaks(50) .* scale;
Z(26:75, 26:75) = Z(26:75, 26:75)+peaks(50);

%Z = abs(Z) .*10;
Z = abs(Z) .* 5;

if nargin == 1
    if display== 0 
        return;
    end
    figure()
    hold on;
    title('Uneven terrain');
    view(3);
    surf(X, Y, Z)
end


end

