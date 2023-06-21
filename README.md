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
- F stands for Player First Spawn locations
The second char of each tile represents the height level. Holes can only be on height level 0

All tiles shall be connected, and tiles are connected if they follow the rules of being just pathable from
one another, based on height. Ramps are only pathable from their two endpoints, where the facing endpoint is one up

This works by first creating a minimum spanning tree for the lower triangle part of the map with the kruskal algorithm on the grid graph,
then traversing this graph with a depth first search and adding ramps and ground tiles along the way. Afterwards the holes, obstacles and powerups are filled in.

Current Limitation for height: 9 (as its handled by single character currently!)

An Example map could look like this:
```
G2 G2 G2 G2 G2 W1 G1 W0 E0 G1 G2 O2 O2 G0 G5 G4 G4 W3 G3 G3 G3 G3 W2 E2 G3 E3 G4 G4 G5 G5 
G2 G2 S2 G2 G2 G1 G1 O1 G2 G2 G2 G2 P0 G0 G5 W4 G4 G3 G3 G3 G3 G3 G1 G4 G3 G3 G4 E4 G5 N4 
G2 E2 G3 G2 G2 G2 G1 G1 G2 G2 N1 G1 S0 G5 G5 G5 G5 G3 G3 G3 G3 G3 N0 G4 W3 G3 G4 G4 G5 O4 
G2 G2 G2 G2 G2 G1 G1 G1 G1 G1 G1 G1 G1 G4 G4 G5 G3 G3 G3 W2 G2 G2 S0 G4 G2 G2 G4 W3 G3 G3 
G2 G2 G2 G2 G1 G1 G1 G1 G1 G1 G1 G1 G0 G4 G4 W3 O3 G3 G3 G2 G2 W1 G1 G1 G1 O2 G2 G4 W3 G3 
N1 G1 G2 G1 G1 G1 G1 G1 G1 G1 G1 G0 G0 G0 G4 G2 W1 G1 G1 G2 G2 G2 G2 S1 G1 S2 G4 G4 G4 G4 
G1 G1 G1 G1 G1 G1 O1 G1 G1 N0 G1 G1 S0 G1 G2 G2 G1 G1 G1 N1 G2 G2 G2 F2 G2 G3 E3 G4 G4 G4 
N0 O1 G1 G1 G1 G1 G1 G1 G1 G0 E0 G1 G1 G1 G1 G2 G1 G1 G1 G1 E1 G2 G2 N1 S2 G3 E3 G4 S4 G5 
S0 G2 G2 G1 G1 G1 G1 G1 G1 G0 G0 N0 G1 G1 G1 G1 G1 H0 G1 G1 G1 G1 G2 N0 G3 G3 G3 G3 G5 G5 
G1 G2 G2 G1 G1 G1 W0 G0 G0 G0 G0 S0 G1 G1 G1 O1 G1 G1 G1 G1 S1 G3 G3 G0 G4 G3 G3 G3 G5 S5 
G2 G2 W1 G1 G1 G1 G1 S0 G0 G0 G1 G1 G1 G1 G1 G1 G1 G1 G1 E1 G2 G3 G3 G3 N3 G3 G3 G4 G4 G6 
O2 G2 G1 G1 G1 G0 G1 G1 W0 E0 G1 G1 G1 P1 G1 G2 G1 G1 G1 E1 G2 G3 G3 G3 G3 G3 E3 G4 G4 O4 
O2 P0 E0 G1 G0 G0 E0 G1 G1 G1 G1 G1 G1 S1 G2 G2 G1 G1 G1 G1 G2 G3 G3 G3 G3 G3 G3 G4 G4 G4 
G0 G0 G5 G4 G4 G0 G1 G1 G1 G1 G1 P1 E1 G2 G2 G1 G1 G1 G1 G2 E2 E3 G4 G3 G3 G3 G3 G3 N3 G4 
G5 G5 G5 G4 G4 G4 G2 G1 G1 G1 G1 G1 G2 G2 G2 G2 S1 G1 E1 G2 W1 G1 H0 G3 G3 G3 N2 G3 G3 G3 
G4 N4 G5 G5 N3 G2 G2 G2 G1 O1 G1 G2 G2 G1 G2 G2 G2 G2 G2 G2 G1 G1 G3 G3 W2 G2 G2 G3 G3 G3 
G4 G4 G5 G3 O3 N1 G1 G1 G1 G1 G1 G1 G1 G1 E1 G2 G2 G2 G2 G2 G2 G2 G2 G2 G2 G2 G2 G3 G3 G3 
N3 G3 G3 G3 G3 G1 G1 G1 H0 G1 G1 G1 G1 G1 G1 G2 G2 G2 G2 G2 G2 G2 G2 G2 G2 G1 G1 G3 G3 G3 
G3 G3 G3 G3 G3 G1 G1 G1 G1 G1 G1 G1 G1 G1 S1 G2 G2 G2 G2 E2 G3 W2 G2 G2 G2 G1 G1 G1 G3 G3 
G3 G3 G3 N2 G2 G2 W1 G1 G1 G1 S1 S1 G1 G2 G2 G2 G2 G2 S2 G3 G3 G3 G2 G2 G2 G2 S1 G2 E2 G3 
G3 G3 G3 G2 G2 G2 G2 S1 G1 E1 G2 G2 G2 S2 N1 G1 G2 G2 G3 G3 G3 G2 G2 G2 G2 G2 G2 G2 G2 N2 
G3 G3 G3 G2 N1 G2 G2 G2 G1 G3 G3 G3 G3 S3 G1 G1 G2 G2 N2 G3 G2 G2 G2 G2 G2 W1 E1 G2 G2 G2 
N2 G1 W0 E0 G1 G2 G2 G2 G2 G3 G3 G3 G3 G4 H0 G3 G2 G2 G2 G2 G2 G2 G2 G2 N1 G1 G2 G2 G2 S2 
S2 G4 G4 G4 G1 E1 F2 W1 W0 G0 G3 G3 G3 G3 G3 G3 G2 G2 G2 G2 G2 G2 G2 G1 G1 G1 G1 G1 H0 G3 
G3 G3 N3 G2 G1 G1 G2 E2 G3 G4 W3 G3 G3 G3 G3 N2 G2 G2 G2 G2 G2 G2 W1 G1 G1 O1 G1 G1 G3 G3 
S3 G3 G3 G2 O2 E2 G3 G3 G3 G3 G3 G3 G3 G3 G3 G2 G2 G1 G1 G2 G2 N1 G1 G1 O1 G1 G1 G1 G1 G0 
G4 G4 G4 G4 G2 G4 S3 S3 G3 G3 G3 S3 G3 G3 W2 G2 G2 G1 G1 E1 G2 S1 G2 G1 G1 G1 G1 G1 G0 G0 
G4 S4 G4 N3 G4 G4 G4 G4 G3 G3 G4 G4 G4 G3 G3 G3 G3 G3 G1 G2 G2 G2 G2 G1 G1 G1 G1 G1 W0 G0 
G5 G5 G5 G3 N3 G4 G4 E4 G5 G5 G4 G4 G4 W3 G3 G3 G3 G3 G3 S2 G2 G2 G2 H0 G3 G1 G0 N0 O0 G0 
G5 W4 O4 G3 G3 G4 G4 G5 G5 E5 G6 O4 G4 G4 G3 G3 G3 G3 G3 G3 W2 G2 E2 G3 G3 G0 G0 G0 G0 G0 
```
