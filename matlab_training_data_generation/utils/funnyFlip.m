function [ flipped ] = funnyFlip( A )

    A = rot90(A, randi([1 8],1,1));
    if rand() <= 0.5
        A = flipud(A); 
    else
        A = fliplr(A);
    end

    flipped = A;
end

