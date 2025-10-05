from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Class:
    uri: str
    title: str
    description: str

@dataclass
class DatatypeProperty:
    uri: str
    title: str

@dataclass
class ObjectProperty:
    uri: str
    title: str
#    allowed_classes: List[Class]

@dataclass
class Object:
    uri: str
    title: str
    description: str
    # properties: Dict[str, Any]  # (DatatypeProperty.title, property_value)
    # object_properties: Dict[str, str] # (ObjectProperty.title, object_uri)

@dataclass
class ClassSignature:
    uri: str
    params: List[DatatypeProperty]  
    obj_params: List[ObjectProperty]    

@dataclass
class Ontology:
    signatures: List[ClassSignature]
    objects: List[Object]