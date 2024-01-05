# SilverBall

### About
A Pygame clone of a somewhat popular flash game on Miniclip called SilverSphere. Made as a birthday gift to my mom who really enjoyed playing that flash game. Contains additional features

### Software Contents
The project consists of 1 part:
- **Pygame Client:** The singleplayer game client for SilverBall

### Development Progress
The project is complete!:
> Client 100%

### Planned Features
Additional features in mind by planned version

#### v3.1
- Database for user-made levels
#### v3.2
- Database for best times on custom and main levels
- Level select menu displays user's best time and score on each level
- Total score a sum of main level scores
- Scores update when you beat a level with a better time / score
#### v3.3
- (Consider if this is even necessary) Add separate shadow layer for X 
tiles so shadows are slightly above when cast onto them

### Dependencies:
- Python 3.10+
- Pygame

### Changelog

#### v3.0
This version is still in development; changelog is subject to change.

Changes
- Extensive refactoring of entire codebase
- Shadows:
  - Added separate shadows for water and land
  - Added box, metal box, and ball water and land shadows
  - Added land shadow clipping
  - Shadows scale and move based on z-coordinate
- Added white flash animation for ball spawning at level start
- Drowned spheres get smaller with an animation
- Added splash effect for objects dropped in water
- Added custom level editor
- Drowned enemy spheres now act as platforms
- Fixed X tiles drawn above metal boxes
- Fixed ball clipping slightly into pushed boxes

Bugs
- If a level is beaten with a better time, no additional score is given

#### v.2.0:
Changes
- Added enemies
- Added original Silversphere levels
- Changed water texture
- Changed background texture
- Changed shadow texture
- Added 2 additional levels
- Added BIRTHDAY effect after beating all levels

Bugs:
- Border causes immense lag
- When ball pushes box into yellow ball, silver ball remains alive contrary to original game
- X tiles are drawn above metal box tiles 
- Ball shadow extends past game window
- A drowned box on the same tile as a drowned yellow ball doesn't have proper draw order
- A drowned yellow ball should probably act as a platform
- If a level is beaten with a better time, no additional score is given

#### v1.0
Changes
- Port game from codeskulptor

Bugs:
- Border causes immense lag
