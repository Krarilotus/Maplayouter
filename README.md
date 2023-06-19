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

An Example map could look like this:
G5 G5 O5 G5 G5 E5 E6 G7 G7 G7 G7 G7 G7 E7 G8 E8 W8 E8 G9 G5 G5 P5 G4 G3 G2 G2 G2 G1 E1 G2 
G5 G5 G5 G5 G5 G5 G5 G7 G7 G7 G7 G7 G7 G8 G8 G8 G5 G5 G5 G5 G5 G5 N3 G3 G3 G2 G2 G2 G2 G2 
O5 G5 G5 G5 O5 G5 G5 G7 G7 G7 G7 G7 G8 G8 G8 G8 G8 G5 G5 G5 G5 G3 G3 G3 G3 G2 G2 G2 N1 G2 
G5 G5 G5 G5 G5 G5 G5 G5 G8 G8 G7 G7 G8 G8 G8 G8 G5 G5 G5 G5 G5 G3 G3 G3 G3 W2 G2 G2 G1 G1 
G5 G5 O5 G5 G5 G5 G5 G5 G8 G8 W7 G7 N7 S8 G4 E4 G5 G5 G5 G1 E1 E2 G3 G3 G3 G4 G2 G2 G1 G1 
S5 G5 G5 G5 G5 G5 G5 G5 G8 G8 G7 G7 N6 G9 G6 W5 O5 G5 H0 G4 G4 G3 G3 G3 E3 G4 G4 G1 G1 G1 
S6 G5 G5 G5 G5 G5 G5 G5 G6 G5 G5 G5 G6 G6 G6 G6 W5 G5 G4 G4 N3 H0 G3 G3 G3 G4 G4 O1 G1 G1 
G7 G7 G7 G5 G5 G5 G5 G6 G6 G5 G5 G5 G6 G6 G6 G6 G6 G4 G4 G4 G3 G3 G3 G3 G4 G4 G4 W3 G3 G3 
G7 G7 G7 G8 G8 G8 G6 G6 O6 W5 G5 G5 E5 G6 G6 G6 P4 G4 G4 G4 W3 O3 G3 G3 G3 G3 G4 G4 G3 S3 
G7 G7 G7 G8 G8 G8 G5 G5 N5 G5 G5 E5 G6 N5 G6 G6 G6 G4 G4 G3 G3 G3 G3 G3 O3 G3 G4 W3 G3 G4 
G7 G7 G7 G7 N7 G7 G5 G5 G5 G5 G5 G5 G6 G5 G5 G5 G5 G5 G4 G3 G3 N2 G2 G3 G3 G3 G4 E4 G5 G5 
G7 G7 G7 G7 G7 G7 G5 G5 G5 S5 G5 G5 G5 G5 G5 G5 G5 W4 W3 W2 G2 G2 G2 W1 G1 G1 G6 G6 G5 G5 
G7 G7 G8 G8 W7 W6 G6 G6 S5 G6 G6 G5 G5 G5 G5 G5 G5 G5 G5 G3 G2 G2 G2 G0 N0 S1 N5 N5 G6 G6 
S7 G8 G8 G8 E8 G9 G6 G6 G6 W5 G5 G5 G5 G5 G6 S5 G5 G5 H0 G3 W2 G2 G2 G0 G0 G2 G5 G5 E5 G6 
G8 G8 G8 G8 G4 G6 G6 G6 G6 G6 G5 G5 G5 G6 G6 G6 W5 G5 G5 G2 G2 G2 G2 G5 G5 G5 G6 G5 G5 G5 
S8 G8 G8 G8 S4 N5 G6 G6 G6 G6 G5 G5 G5 E5 G6 O6 G6 G5 G5 G2 G2 G2 G4 G5 G5 G5 N5 G5 G5 G5 
N8 G5 G8 G5 G5 O5 N5 G6 P4 G6 G5 G5 G5 G5 N5 G6 G6 G5 G5 G5 G5 G4 G4 O4 G5 G5 G5 G5 G5 N4 
S8 G5 G5 G5 G5 G5 G5 G4 G4 G4 G5 N4 G5 G5 G5 G5 G5 G4 E4 G5 G5 S4 G4 E4 G5 G5 G5 G5 G5 S4 
G9 G5 G5 G5 G5 H0 G4 G4 G4 G4 G4 N3 G5 H0 G5 G5 G5 S4 G5 G5 G5 G5 G5 G5 G5 G5 G5 S5 G5 G5 
G5 G5 G5 G5 G1 G4 G4 G4 G4 G3 G3 N2 G3 G3 G2 G2 G5 G5 G5 G5 G5 G6 G5 G5 G5 G7 W6 G6 G6 G6 
G5 G5 G5 G5 S1 G4 W3 G3 N3 G3 G3 G2 G2 N2 G2 G2 G5 G5 G5 G5 G5 N5 G5 G5 G5 G7 G7 G6 G6 G6 
P5 G5 G3 G3 S2 G3 H0 G3 O3 G3 W2 G2 G2 G2 G2 G2 G4 E4 G5 G6 W5 G5 G5 G5 G6 G6 G7 W6 G6 G6 
G4 W3 G3 G3 G3 G3 G3 G3 G3 G3 G2 G2 G2 G2 G2 G4 G4 G4 G5 G5 G5 G5 G5 S5 O6 G6 G7 G7 N5 N5 
G3 G3 G3 G3 G3 G3 G3 G3 G3 G3 G3 N1 G0 G0 G5 G5 O4 S4 G5 G5 G5 G5 E5 G6 G6 G7 G7 G5 O5 S5 
G2 G3 G3 G3 G3 S3 G3 G4 G3 O3 G3 G1 W0 G0 G5 G5 G5 G5 G5 G5 G5 G6 O6 G6 G6 G6 G6 W5 G5 G6 
G2 G2 G2 N2 G4 G4 G4 G4 G3 G3 G3 G1 E1 G2 G5 G5 G5 G5 G5 G7 G7 G6 G6 G7 G6 G6 G6 G5 G5 G5 
G2 G2 G2 G2 G2 G4 G4 G4 G4 G4 G4 G6 W5 G5 G6 W5 G5 G5 G5 N6 G7 G7 G7 G7 G6 G6 G5 G5 G5 G5 
G1 G2 G2 G2 G2 G1 O1 N3 G4 N3 S4 G6 W5 G5 G5 G5 G5 G5 E5 G6 G6 N6 G7 G5 N5 G5 G5 G5 W4 G4 
S1 G2 W1 G1 G1 G1 G1 G3 G3 G3 G5 G5 G6 S5 G5 G5 G5 G5 G5 G6 G6 G6 W5 O5 G5 G5 G5 N4 G4 G4 
G2 G2 G2 G1 G1 G1 G1 G3 E3 G4 G5 G5 G6 G6 G5 G5 W4 E4 G5 G6 G6 G6 W5 E5 G6 G5 G5 G4 G4 G4 
