rows = 20;
cols = 20;
T = zeros(rows,cols);
n = 500000;
for i=1:n
   terra = sampleTerrain(rows,cols); 
   T = T + terra;
end
T = T/n;
figure()
hold on
axis equal
view(3)
surf(T)

