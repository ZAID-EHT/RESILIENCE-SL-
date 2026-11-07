"""
Data acquisition interfaces and parameter specifications.
"""

from rsl.acquire.openmeteo import OpenMeteoAcquirer
from rsl.acquire.chirps import CHIRPSAcquirer
from rsl.acquire.imerg import IMERGAcquirer
from rsl.acquire.floodmap import FloodMapAcquirer
from rsl.acquire.landcover import LandCoverAcquirer

__all__ = [
    "OpenMeteoAcquirer",
    "CHIRPSAcquirer",
    "IMERGAcquirer",
    "FloodMapAcquirer",
    "LandCoverAcquirer",
]
