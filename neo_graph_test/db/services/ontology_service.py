from typing import List, Dict, Any, Optional
from dataclasses import asdict
from ..repositories.ontology_driver.driver import OntologyRepository

class OntologyService:
    def __init__(self, repository: OntologyRepository):
        self.repository = repository

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        if hasattr(self.repository, 'close'):
            self.repository.close()

    # Ontology methods
    def get_ontology(self) -> Dict[str, Any]:
        ontology = self.repository.get_ontology()
        return asdict(ontology)

    def get_ontology_parent_classes(self) -> List[Dict[str, Any]]:
        classes = self.repository.get_ontology_parent_classes()
        return [asdict(cls) for cls in classes]

    # Class methods
    def get_class(self, uri: str) -> Optional[Dict[str, Any]]:
        class_obj = self.repository.get_class(uri)
        return asdict(class_obj) if class_obj else None

    def get_class_parents(self, uri: str) -> List[Dict[str, Any]]:
        print(uri)
        parents = self.repository.get_class_parents(uri)
        return [asdict(parent) for parent in parents if parent]

    def get_class_children(self, uri: str) -> List[Dict[str, Any]]:
        children = self.repository.get_class_children(uri)
        return [asdict(child) for child in children if child]

    def get_class_objects(self, uri: str) -> List[Dict[str, Any]]:
        objects = self.repository.get_class_objects(uri)
        return [asdict(obj) for obj in objects]

    def create_class(self, title: str, description: str = "", parent_uri: str = None) -> str:
        return self.repository.create_class(title, description, parent_uri)

    def update_class(self, uri: str, title: str = None, description: str = None) -> bool:
        self.repository.update_class(uri, title, description)
        return True

    def delete_class(self, uri: str) -> bool:
        self.repository.delete_class(uri)
        return True

    def add_class_parent(self, parent_uri: str, target_uri: str) -> bool:
        self.repository.add_class_parent(parent_uri, target_uri)
        return True

    # Attribute methods
    def add_class_attribute(self, uri: str, datatype_title: str) -> str:
        return self.repository.add_class_attribute(uri, datatype_title)

    def delete_class_attribute(self, attribute_uri: str) -> bool:
        self.repository.delete_class_attribute(attribute_uri)
        return True

    def add_class_object_attribute(self, uri: str, attr_name: str, range_uri: str) -> str:
        return self.repository.add_class_object_attribute(uri, attr_name, range_uri)

    def delete_class_object_attribute(self, object_property_uri: str) -> bool:
        self.repository.delete_class_object_attribute(object_property_uri)
        return True

    # Object methods
    def get_object(self, uri: str) -> Optional[Dict[str, Any]]:
        obj = self.repository.get_object(uri)
        return asdict(obj) if obj else None

    def create_object(self, uri: str, title: str, description: str = "", 
                     properties: Dict[str, Any] = None, 
                     object_properties: Dict[str, str] = None) -> str:
        return self.repository.create_object(uri, title, description, properties or {}, object_properties or {})

    def update_object(self, uri: str, title: str = None, description: str = None,
                     properties: Dict[str, Any] = None,
                     new_connections: Dict[str, str] = None) -> bool:
        return self.repository.update_object(uri, title, description, properties or {}, new_connections or {})

    def delete_object(self, uri: str) -> bool:
        self.repository.delete_object(uri)
        return True

    # Signature method
    def collect_signature(self, uri: str) -> Dict[str, Any]:
        signature = self.repository.collect_signature(uri)
        return asdict(signature)