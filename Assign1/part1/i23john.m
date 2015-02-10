figure(3)
hold on

scatter(y(1,:),y(2,:),'cyan')

my1 = mean(y(1,:))
my2 = mean(y(2,:))
scatter(my1,my2,72,'blue','+')
scatter(1,2,72,'red','+')

hold off
