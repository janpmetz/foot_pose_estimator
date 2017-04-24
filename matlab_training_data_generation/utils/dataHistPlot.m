m = mean(y);
s = std(y);

st = strcat('mean: ', num2str(m), ' std: ', num2str(s));

% also median and mode


hist(y,100);
hold on;
title(st, 'FontSize', 12);