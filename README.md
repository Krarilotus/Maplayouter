# Maplayouter
Creating generic map layouts for grid based maps to train AI FPS agents

We want to create a dungeon floor plan
N, S, W, E stand for directions, left top is lowest index being north west
while bottom right is east south with the highest index
First index stands for north to south
Second stands for West to East

We have 5 tile types:
- N, S, W, E are all Ramp tiles, where the ramp connects to one height higher than
  their own ground from their opposite direction to their facing direction
- G stands for ground
- H - stands for Hole
- O stands for Obstacle
- P stands for Powerup
The second char of each tile represents the height level. Holes can only be on height level 0

All tiles shall be connected, and tiles are connected if they follow the rules of being just pathable from
one another, based on height. Ramps are only pathable from their two endpoints, where the facing endpoint is one up

This works by first creating a minimum spanning tree for the lower triangle part of the map with the kruskal algorithm on the grid graph,
then traversing this graph with a depth first search and adding ramps and ground tiles along the way. Afterwards the holes, obstacles and powerups are filled in.

Current Limitation for height: 9 (as its handled by single character currently!)
