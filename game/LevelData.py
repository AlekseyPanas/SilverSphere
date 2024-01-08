from __future__ import annotations
from dataclasses import dataclass
import Constants


@dataclass
class BoxData:
    coord_xy: tuple[int, int]
    is_ice: bool


@dataclass
class EnemyData:
    """
    path formed by moving in the specified direction for the specified length as indicated by index correspondence
    """
    start_coord_xy: tuple[int, int]
    path_directions: list[str]
    path_lengths: list[int]


@dataclass
class LevelData:
    name: str
    time_limit: int
    layout: list[list[str]]
    player_start_coord_xy: tuple[int, int]
    vortex_coord_xy: tuple[int, int]
    boxes: list[BoxData]
    ice_x_coords_xy: list[tuple[int, int]]
    box_x_coords_xy: list[tuple[int, int]]
    enemies: list[EnemyData]

    def to_dict(self) -> dict:
        """Dict object of level in the valid format"""
        return {
            "id": "CUSTOM",
            "name": self.name,
            "time": self.time_limit,
            "layout": self.layout,
            "player_start": self.player_start_coord_xy,
            "vortex_pos": self.vortex_coord_xy,
            "box_poses": [b.coord_xy for b in self.boxes],
            "box_types": ["ice" if b.is_ice else "box" for b in self.boxes],
            "ice_x_poses": self.ice_x_coords_xy,
            "box_x_poses": self.box_x_coords_xy,
            "enemies": [
                {
                    "path_dir": e.path_directions,
                    "path_dist": e.path_lengths,
                    "start_pos": e.start_coord_xy
                } for e in self.enemies
            ]
        }

    @staticmethod
    def from_dict(level_dict: dict) -> LevelData:
        """Build a level data object from a dictionary"""
        return LevelData(
            level_dict["name"],
            level_dict["time"],
            level_dict["layout"],
            level_dict["player_start"],
            level_dict["vortex_pos"],
            [BoxData(level_dict["box_poses"][i],
                     level_dict["box_types"][i] == "ice") for i in range(len(level_dict["box_poses"]))],
            [tuple(pos) for pos in level_dict["ice_x_poses"]],
            [tuple(pos) for pos in level_dict["box_x_poses"]],
            [EnemyData(e["start_pos"], e["path_dir"], e["path_dist"]) for e in level_dict["enemies"]]
        )

    @staticmethod
    def generate_default(level_name) -> LevelData:
        """Generate a default editor-valid level to serve as a starting point when creating a new level"""
        layout = [['W' for _ in range(Constants.GRID_DIMS[0])] for _ in range(Constants.GRID_DIMS[1])]
        for i in range(3):
            for j in range(3):
                layout[i][j] = "T"
                layout[Constants.GRID_DIMS[1] - i - 1][Constants.GRID_DIMS[0] - j - 1] = "T"
        return LevelData(level_name, 60, layout, (1, 1), (18, 10), [], [], [], [])
