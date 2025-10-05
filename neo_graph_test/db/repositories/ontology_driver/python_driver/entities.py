from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class TArc:
    id: str
    label: str  
    props: Dict[str, Any]
    node_uri_from: str
    node_uri_to: str

@dataclass
class TNode:
    id: str
    uri: str
    labels: List[str]
    props: Dict[str, Any]
    arcs: Optional[List[TArc]] = None
