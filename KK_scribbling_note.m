%% readWorld 
f = textread('block1/AprilNew2.txt', '%s');

worldw = str2num(f{1}); 
worldh = str2num(f{2}); 

gridworld = zeros(worldh, worldw);

for i = 3:size(f,1) 

 line = f{i};
 %fprintf('line %d, %s\n', i, line); 
 for j = 1:size(line,2)
    c = str2num(line(j));
   gridworld(i-2,j) = c;
 end
end

%% initialiseWorld
%initialise the visible area
visible = gridworld;
visible(gridworld == 3) = 1;
visible(gridworld < 3 ) = 0;

%the starting cell is alwyas visible
visible(1, 1) = 1;

% let the agent look around
visible = updateVisible(gridworld, visible, 1, 1);

%% updateVisible 
v = visible; 
agent_x = 4; agent_y = 4; 

vis = v; 
vis(agent_y,agent_x)=1;
ww = size(gridworld,2); % x
wh = size(gridworld,1); %

for level = 1:-1:1
    for px = max(agent_x-level, 1):1:min(agent_x+level,ww)

      if agent_y-level > 0
        v1 = addvisible(agent_x, agent_y, px, agent_y-level, level, v, gridworld); 
        vis(v1==1)=1;
      end

      if agent_y+level <= wh
        v2 = addvisible(agent_x, agent_y, px, agent_y+level, level, v, gridworld); 
        vis(v2==1)=1;
      end

    end

    for py = max(agent_y-level,1):1:min(agent_y+level,wh)

      if agent_x+level <=ww
        v3 = addvisible(agent_x, agent_y, agent_x+level, py, level, v, gridworld); 
        vis(v3==1)=1;
      end

      if  agent_x-level > 0
        v4 = addvisible(agent_x, agent_y, agent_x-level, py, level, v, gridworld); 
        vis(v4==1)=1;
      end

    end
    
    if level == 1
          figure; imagesc(vis+gridworld)
    end 
end 
 figure; imagesc(visible+gridworld)