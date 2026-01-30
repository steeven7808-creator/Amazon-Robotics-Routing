"""
Amazon Robotics Hackathon - Routing API

This module defines the routing API for the Amazon Robotics Hackathon.
Students will implement the route_package function in this module.

*****IMPORTANT*****
Team name:
Email address:
*******************
"""

from typing import Optional
from ar_hackathon.models.game_state import GameState
from ar_hackathon.models.package import Package

def route_package(state: GameState, package: Package) -> Optional[str]:
    """
    Determine the next FC to route a package to.
    
    This is the function that students will implement. The game engine will call
    this function for each package at each time step to determine where to route it.
    
    Args:
        state: GameState object containing the current state of the network
        package: Package object containing information about the package
        
    Returns:
        next_fc_id: ID of the next FC to route the package to, or None to stay at current FC
    """
    # Student implementation here
from typing import Optional
import networkx as nx  # already installed with dependencies

from typing import Optional
import networkx as nx

# Global cache dictionary for (current, destination) -> path
_path_cache = {}

def route_package(state: GameState, package: Package) -> Optional[str]:
    """
    Shortest path routing with path caching.
    - Uses a global dictionary to store computed paths.
    - If the same (current, destination) is requested again, 
      return from cache instead of recomputing.
    - This improves speed in multi-package scenarios.
    """

    # 1) Get current and destination FCs
    current_fc = getattr(package, "current_fc", None)
    destination_fc = getattr(package, "destination_fc", None)
    if current_fc is None or destination_fc is None:
        return None
    if current_fc == destination_fc:
        return None  # Already at the destination

    # 2) Build a cache key
    cache_key = (current_fc, destination_fc)

    # 3) If path already cached, return next hop
    if cache_key in _path_cache:
        path = _path_cache[cache_key]
    else:
        # Extract graph from state
        def _extract_graph(s):
            for key in ("graph", "network", "fc_graph", "fc_network", "nx_graph"):
                if hasattr(s, key):
                    g = getattr(s, key)
                    if isinstance(g, (nx.Graph, nx.DiGraph)):
                        return g
            return None

        G = _extract_graph(state)
        if G is None or current_fc not in G or destination_fc not in G:
            return destination_fc  # Fallback: direct delivery

        # Choose weight attribute if available
        def _choose_weight_attr(graph: nx.Graph):
            try:
                _, _, data = next(iter(graph.edges(data=True)))
            except StopIteration:
                return None
            for attr in ("time", "cost", "weight", "distance", "duration"):
                if attr in data:
                    return attr
            return None

        weight_attr = _choose_weight_attr(G)

        try:
            if weight_attr:
                path = nx.shortest_path(G, current_fc, destination_fc, weight=weight_attr)
            else:
                path = nx.shortest_path(G, current_fc, destination_fc)
        except Exception:
            return destination_fc

        # Save path in cache
        _path_cache[cache_key] = path

    # 4) Return the next hop
    if not path or len(path) < 2:
        return None
    return path[1]
