function [ FootObj ] = getFoot( fileName, rows, cols, display)
% load foot from black/white image as 0-1 matrix
% rows and cols size of output matrix (foot size)
% k are indices of points under the foot sole

A = imread(fileName);
A = imresize(A, [rows cols]); % if cols automatic then use NaN as cols
A = A(:,:,1);
Flogical = A <= 0;
Sole = 0+Flogical; % cast logical to double

%[row,col,v] = find(A <= 0);

k = find(A <= 0);

FootObj.Sole = Sole;
FootObj.ptsInFootIdx = k;

if nargin == 4
    if display== 0 
        return;
    end
    figure()
    hold on;
    title('Foot shape');
    imshow(Sole);
end

end

