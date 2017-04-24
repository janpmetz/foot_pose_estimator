function [ T, oldMax ] = sampleTerrainStages_max(scale)
% sample random terrain and return the height of the highest point
% this is used to learn on normed data and rescale it later to the old
% height


%runs = randint(1, 1, [1,3]);
runs = 1;

% Draw random parents for each new point.

x = 0.25 * randn(3, 1);
y = 0.25 * randn(3, 1);
h = 0.5*randn(3, 1);

% trisurf(delaunay([-1; -1; 1; 1; x], [-1; 1; -1; 1; y]), ...
%        [-1; -1; 1; 1; x], [-1; 1; -1; 1; y], [0; 0; 0; 0; h]);
%     
% axis equal vis3d;
% set(gca, 'Projection', 'perspective');
% 

parents = randi(length(x), 1, 3*length(x)); % Pick parent points.

% Draw new x, y points. Limit to [0, 1].
x_new = max(min(x(parents) + 0.5 * randn(3*length(x), 1), 1), -1);
y_new = max(min(y(parents) + 0.5 * randn(3*length(x), 1), 1), -1);




% Interpolate to find current height. We'll use an anonymous function here
% for brevity and then use it again and again. If this looks unfamiliar,
% search for "anonymous functions" in the documentation.
interpolate = @(x, y, h, x_new, y_new) ...
    feval(@(int) int(x_new, y_new), ...
          TriScatteredInterp([-1; -1; 1; 1; x], ...
                             [-1; 1; -1; 1; y], ...
                             [0; 0; 0; 0; h]));

                         
h_new = interpolate(x, y, h, x_new, y_new);


% 
% pause
% 
% 
% % Show the new points.
% hold on;
% plot3(x_new, y_new, h_new, 'r+');
% hold off;
% 


h_new = h_new + 0.1 * randn(3*length(x), 1);
x = [x; x_new];
y = [y; y_new];
h = [h; h_new];


% We'll use this plot process a lot, so we'll write an anonymouns function
% for this too. Again, see the documentation for "anonymous function" if
% this looks unfamiliar.
plot_it = @(x, y, h) trisurf(delaunay([-1; -1; 1; 1; x], ...
                                      [-1; 1; -1; 1; y]), ...
                             [-1; -1; 1; 1; x], ...
                             [-1; 1; -1; 1; y], ...
                             [0; 0; 0; 0; h]);
                         
                         
% plot_it(x, y, h);
% axis equal vis3d;
% set(gca, 'Projection', 'perspective');
% 
% 
% pause
% 
% % There may be a warning below about duplicate data points. That just means
% % we generated points outside of the [-1, 1] window and are ignoring them.
% % The real algorithm doesn't do this, but it's simpler to see the algorithm
% % without worrying about this detail for now. We'll turn off that
% % particular warning.
warning_state = warning('query', 'MATLAB:delaunay:DupPtsDelaunayWarnId');
warning off MATLAB:delaunay:DupPtsDelaunayWarnId
warning off MATLAB:TriScatteredInterp:DupPtsAvValuesWarnId

% % Draw random parents for each new point.
parents = randi(length(x), 1, 3*length(x)); % Pick parent points.

% Draw new x, y points. Limit to [0, 1].
x_new = max(min(x(parents) + 0.75 * 0.5 * randn(3*length(x), 1), 1), -1);
y_new = max(min(y(parents) + 0.75 * 0.5 * randn(3*length(x), 1), 1), -1);

% Interpolate to find current height.
h_new = interpolate(x, y, h, x_new, y_new);


% % Show the new points.
% hold on;
% plot3(x_new, y_new, h_new, 'r+');
% hold off;
% snapnow();


% Vary the heights.
h_new = h_new + 0.5 * 0.1 * randn(3*length(x), 1);
x = [x; x_new];
y = [y; y_new];
h = [h; h_new];


% pause
% 
% Show the new surface.
% plot_it(x, y, h);
% axis equal vis3d;
% set(gca, 'Projection', 'perspective');

% pause

for k = 1:runs
    
    % Pick parent points.
    parents = randi(length(x), 1, 3*length(x));

    % Draw new x, y points. Limit to [0, 1].
    d = 0.75^k;
    x_new = max(min(x(parents) + d * 0.5 * randn(3*length(x), 1), 1), -1);
    y_new = max(min(y(parents) + d * 0.5 * randn(3*length(x), 1), 1), -1);

    % Interpolate to find current height.
    h_new = interpolate(x, y, h, x_new, y_new);

%     hold on;
%     plot3(x_new, y_new, h_new, 'r+');
%     hold off;
%     snapnow();

    % Vary the heights by half as much as last time.
    h_new = h_new + 0.5^k * 0.1 * randn(3*length(x), 1);
    x = [x; x_new]; %#ok<AGROW>
    y = [y; y_new]; %#ok<AGROW>
    h = [h; h_new]; %#ok<AGROW>

    %size(h)
%     
%     plot_it(x, y, h);
%     axis equal vis3d;
%     set(gca, 'Projection', 'perspective');
%     snapnow();
%     
        
    %pause
end

xidx = round(x * scale);
xidx = xidx+abs(min(xidx))+1;
yidx = round(y * scale);
yidx = yidx+abs(min(yidx))+1;

z = h+abs(min(h));

[X, Y] = meshgrid(1:scale, 1:scale);
Zx = interpolate(xidx, yidx, z, X(:), Y(:));



T = reshape(Zx, [scale,scale]);

oldMax = max(max(T));
% scale to 0-1
T = T ./ oldMax;

T(isnan(T)) = 0 ;

%T = T * 17.5;

%surf(T)

%plot_it(xidx,yidx,z)

% for i = 1:numel(xidx)
%     T(xidx(i), yidx(i)) = z(i);
% end

%d=1
