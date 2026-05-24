import sys
from dataclasses import dataclass, field
from typing import List, Dict, Any

"""
📿 DROS Standard Type Definitions - Python Edition
RFC 001: Unified Multi-Language µDROS Core Specification
"""

@dataclass
class DrosSynapse:
    target: str      # 目標節點的 T-Number (例如 T0002)
    relation: str    # 關係類型
    weight: float    # 突觸權重

@dataclass
class DrosNode:
    id: str
    canonical: str
    aliases: List[str]
    weights: Dict[str, float]
    definition: str
    synapses: List[DrosSynapse] = field(default_factory=list)

@dataclass
class DrosManifest:
    version: str
    metadata: Dict[str, Any]
    nodes: Dict[str, DrosNode]

@dataclass
class DrosMatch:
    node_id: str
    start_index: int
    end_index: int
    matched_text: str

@dataclass
class ActiveNeighbor:
    node_id: str
    canonical: str
    relation: str
    source_node_id: str
    weight: float

def parse_manifest(data: Dict[str, Any]) -> DrosManifest:
    """
    將原生的 JSON 字典高度健壯地轉換為強類型 DrosManifest 物件
    """
    nodes = {}
    for node_id, node_data in data.get("nodes", {}).items():
        synapses = [
            DrosSynapse(
                target=s.get("target", ""),
                relation=s.get("relation", ""),
                weight=float(s.get("weight", 0.0))
            )
            for s in node_data.get("synapses", [])
        ]
        
        nodes[node_id] = DrosNode(
            id=node_data.get("id", node_id),
            canonical=node_data.get("canonical", ""),
            aliases=node_data.get("aliases", []),
            weights={k: float(v) for k, v in node_data.get("weights", {}).items()},
            definition=node_data.get("definition", ""),
            synapses=synapses
        )
        
    return DrosManifest(
        version=data.get("version", ""),
        metadata=data.get("metadata", {}),
        nodes=nodes
    )
