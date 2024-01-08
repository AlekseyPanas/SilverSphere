# SilverBall

### About
A Pygame clone of a somewhat popular flash game on Miniclip called SilverSphere. Made as a birthday gift to my mom who really enjoyed playing that flash game. Contains additional features

### Software Contents
The project consists of 1 part:
- **Pygame Client:** The singleplayer game client for SilverBall

### Development Progress
The project is complete!:
> Client 100%

### Dependencies:
- Python 3.10+
- Pygame

### Planned Features
Additional features in mind by planned version

#### v3.1
- Extensive refactoring of sprite game logic, including a fix for cross-sprite mutation
#### v3.2
- Database for user-made levels
#### v3.3
- Database for best times on custom and main levels
- Level select menu displays user's best time and score on each level
- Total score a sum of main level scores
- Scores update when you beat a level with a better time / score
#### v3.4
- Add white flash for ball spawning and ball vortex exiting

### Changelog

#### v3.0
This version is still in development; changelog is subject to change.

Changes
- Visuals
  - Shadows:
    - Added separate shadows for water and land
    - Added box, metal box, ball, X, and Vortex water and land shadows
    - Added land shadow clipping
    - Shadows scale and move based on z-coordinate
    - Added ambient tree shadows like in original game
  - Drowned spheres get smaller with an animation
  - Added splash effect for objects dropped in water
  - Designed new original metal box asset
- Game
  - [ ] Added custom level editor
  - Drowned enemy spheres now act as platforms
- Bug Fixes
  - Fixed X tiles drawn above metal boxes
  - Fixed ball clipping slightly into pushed boxes
  - Fixed relative paths breaking when executing script from another directory
  - Fixed broken collision radius under resolution changes
  - Fixed jittery open vortex animation
  - Fixed libpng warning
- Other
  - Extensive refactoring of entire codebase
  - Added signal catching to prevent losing data when terminating game

Bugs
- If a level is beaten with a better time, no additional score is given
- Enemy sprite animation is not using intermediates
- Objects in editor can be moved into an enemy path, such as Vortex or Metal block

Issues
- Direct cross-sprite mutation causes unpredictable behavior. 
Add methods for so that sprite modifications are queued into the sprite and performed by that sprite
in a second post-update loop
- Intermediate animation frame generation is not very good at the moment.
Furthermore, Animation in general should be somehow better organized rather than
controlled by each sprite individually
- Player and enemy have similar visuals in terms of animation, drowning, etc.
Code should be extracted into a shared class rather than repeated

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
