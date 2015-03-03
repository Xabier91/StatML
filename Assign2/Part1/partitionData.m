function [ set0,set1,set2 ] = partitionData( data )


set0 = zeros(100,2);
set1 = zeros(100,2);
set2 = zeros(100,2);

counter0 = 1;
counter1 = 1;
counter2 = 1;

for i = 1:length(data(:,3)),
    if data(i,3) == 0
        set0(counter0,:) = data(i,1:2);
        counter0 = counter0 + 1;
    elseif data(i,3) == 1
         set1(counter1,:) = data(i,1:2);
         counter1 = counter1 + 1;
    elseif data(i,3) == 2
         set2(counter2,:) = data(i,1:2);
         counter2 = counter2 + 1;
    end
end
    

set0 = set0(1:counter0 -1,:);
set1 = set1(1:counter1 -1,:);
set2 = set2(1:counter2 -1,:);

end
