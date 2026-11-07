"""
Land cover product specifications and cross-sensor classification crosswalk.
"""

from typing import Dict, Any


class LandCoverAcquirer:
    """Class taxonomies and crosswalk definitions for ESA WorldCover and ESA CCI."""

    WORLDCOVER_CLASSES = {
        10: "Tree cover",
        20: "Shrubland",
        30: "Grassland",
        40: "Cropland",
        50: "Built-up",
        60: "Bare / sparse vegetation",
        70: "Snow and ice",
        80: "Permanent water bodies",
        90: "Herbaceous wetland",
        95: "Mangroves",
        100: "Moss and lichen",
    }

    CCI_CLASSES = {
        10: "Cropland, rainfed",
        11: "Cropland, rainfed herbaceous",
        20: "Cropland, irrigated or post-flooding",
        30: "Mosaic cropland (>50%) / natural vegetation (<50%)",
        40: "Mosaic natural vegetation (>50%) / cropland (<50%)",
        50: "Tree cover, broadleaved, evergreen, closed to open",
        60: "Tree cover, broadleaved, deciduous, closed to open",
        70: "Tree cover, needleleaved, evergreen, closed to open",
        80: "Tree cover, needleleaved, deciduous, closed to open",
        90: "Tree cover, mixed leaf type",
        100: "Mosaic tree and shrub (>50%) / herbaceous (<50%)",
        110: "Mosaic herbaceous (>50%) / tree and shrub (<50%)",
        120: "Shrubland",
        130: "Grassland",
        140: "Lichens and mosses",
        150: "Sparse vegetation",
        160: "Tree cover, flooded, fresh or brackish water",
        170: "Tree cover, flooded, saline water",
        180: "Shrub or herbaceous cover, flooded, fresh/saline/brackish water",
        190: "Urban areas",
        200: "Bare areas",
        210: "Water bodies",
        220: "Permanent snow and ice",
    }

    @classmethod
    def get_worldcover_name(cls, code: int) -> str:
        return cls.WORLDCOVER_CLASSES.get(code, f"Unknown ({code})")

    @classmethod
    def get_cci_name(cls, code: int) -> str:
        return cls.CCI_CLASSES.get(code, f"Unknown ({code})")
