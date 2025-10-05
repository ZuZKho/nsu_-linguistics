from typing import List, Optional, Dict, Any
from .python_driver.driver import GraphRepository
from .entities import Class, ClassSignature, Object, ObjectProperty, DatatypeProperty, Ontology
from .python_driver.entities import TNode, TArc
from .onthology_namespace import *

class OntologyRepository:
    def __init__(self, uri: str, user: str, password: str):
        self.graph_repository = GraphRepository(uri, user, password)
        
    def close(self):
        self.graph_repository.close()

    # method to use with with ... as construction
    def __enter__(self):
        return self

    # method to use with with ... as consturction
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    ######################################
    #      Ontology  methods             #
    ######################################
    def get_ontology(self) -> Ontology: 
        classes = self.graph_repository.get_all_nodes()
        signatures = [self.collect_signature(cls.uri) for cls in classes if cls.labels.count(CLASS)]

        objects_query = self.graph_repository.get_all_nodes()
        objects = [self._collect_from_node(obj) for obj in objects_query if obj.labels.count(OBJECT)]

        return Ontology(signatures, objects)

    def get_ontology_parent_classes(self) -> List[Class]:
        all_nodes = self.graph_repository.get_all_nodes()
        root_classes = []
        
        for node in all_nodes:
            if CLASS in node.labels:
                # Проверяем, есть ли у класса родители
                parents = self.get_class_parents(node.props.get(self.URI))
                if not parents:  # Если родителей нет - это корневой класс
                    class_obj = self._collect_from_node(node)
                    if isinstance(class_obj, Class):
                        root_classes.append(class_obj)
        
        return root_classes

    ######################################
    #   Class management methods         #
    ######################################
    def get_class(self, uri: str):
        node = self.graph_repository.get_node_by_uri(uri)
        collected = self._collect_from_node(node)
        if type(collected) is Class:
            return collected 
        return None

    def get_class_parents(self, uri: str) -> List[Class]:
        result = self.graph_repository.get_arcs_from_node(uri)
        nodes = [self._collect_from_node(node) for node in result]    
        return nodes

    def get_class_children(self, uri: str) -> List[Class|Object|DatatypeProperty|ObjectProperty]:
        result = self.graph_repository.get_arcs_to_node(uri)
        nodes = [self._collect_from_node(node) for node in result]    
        return nodes

    def get_class_objects(self, uri: str) -> List[Object]:
        children = self.get_class_children(uri)
        return [child for child in children if type(child) is Object]   

    def update_class(self, uri: str, title: str, description: str):
        self.graph_repository.update_node(uri, set_props={self.TITLE: title, self.DESCRIPTION: description})

    def create_class(self, title: str, description: str, parent_uri: str = None):
        node = self.graph_repository.create_node([CLASS], {self.TITLE: title, self.DESCRIPTION: description})
        if parent_uri != None:
            self.graph_repository.create_arc(node.uri, parent_uri, SUB_CLASS)
        return node.uri
    
    def add_class_parent(self, parent_uri: str, target_uri: str): 
        self.graph_repository.create_arc(target_uri, parent_uri, SUB_CLASS)

    def delete_class(self, uri: str):
        node = self.graph_repository.get_node_by_uri(uri)
        nodes = self.graph_repository.get_arcs_to_node(uri)
        self.graph_repository.delete_node_by_uri(uri)

        while len(nodes):
            new_nodes = []
            for node in nodes:
                children = self.graph_repository.get_arcs_to_node(node.props.get(self.URI))
                for child in children:
                    new_nodes.append(child)
                self.graph_repository.delete_node_by_uri(node.props.get(self.URI))
            nodes = new_nodes
          
    #######################################
    # Class attributes management methods #
    #######################################
    def add_class_attribute(self, class_uri: str, datatype_title: str):
        node = self.graph_repository.create_node([PROPERTY_LABEL], {self.TITLE: datatype_title})
        self.graph_repository.create_arc(node.uri, class_uri, PROPERTY_DOMAIN)
        return node.uri

    def delete_class_attribute(self, attribute_uri: str):
        self.graph_repository.delete_node_by_uri(attribute_uri)

    def add_class_object_attribute(self, class_uri: str, attr_name: str, range_class_uri: str): 
        node = self.graph_repository.create_node([PROPERTY_LABEL_OBJECT], {self.TITLE: attr_name})
        self.graph_repository.create_arc(node.props.get(self.URI), class_uri, PROPERTY_DOMAIN)
        self.graph_repository.create_arc(node.props.get(self.URI), range_class_uri, PROPERTY_RANGE)
        return node.uri
    
    def delete_class_object_attribute(self, object_property_uri: str): 
        # all connections will be destroed as we are using DETACH delete
        self.graph_repository.delete_node_by_uri(object_property_uri)

    #######################################
    #    Object management methods        #
    #######################################
    def get_object(self, uri: str):
        return self._collect_from_node(self.graph_repository.get_node_by_uri(uri))

    def delete_object(self, uri: str):
        return self.graph_repository.delete_node_by_uri(uri)

    def delete_object(self, uri: str):
        return self.graph_repository.delete_node_by_uri(uri)

    def create_object(self, class_uri: str, title: str, description: str = "", 
                     properties: Dict[str, Any] = {}, 
                     object_properties: Dict[str, str] = None) -> str:
        properties.update({
            self.TITLE: title,
            self.DESCRIPTION: description
        })
         
        node = self.graph_repository.create_node([OBJECT], properties)
        self.graph_repository.create_arc(node.uri, class_uri, HAS_TYPE)
        
        if object_properties:
            for prop_label, target_uri in object_properties.items():
                self.graph_repository.create_arc(node.uri, target_uri, prop_label)
        
        return node.uri

    def update_object(self, uri: str, title: str = None, description: str = None,
                     properties: Dict[str, Any] = None,
                     new_connections: Dict[str, str] = None) -> bool:
        set_props = {}
        if title is not None:
            set_props[self.TITLE] = title
        if description is not None:
            set_props[self.DESCRIPTION] = description
        
        if properties:
            set_props.update(properties)
        
        if set_props:
            self.graph_repository.update_node(uri, set_props=set_props)
        
        if new_connections:
            for prop_label, target_uri in new_connections.items():
                self.graph_repository.create_arc(uri, target_uri, prop_label, {})
        
        return True
    
    def collect_signature(self, class_uri: str) -> ClassSignature:
        datatype_properties = []
        object_properties = []

        frontier = [class_uri]
        while len(frontier):
            new_frontier = []
            for front in frontier:
                toclass_edges = self.get_class_children(front)
                [datatype_properties.append(datap) for datap in toclass_edges if type(datap) is DatatypeProperty]
                [object_properties.append(objectp) for objectp in toclass_edges if type(objectp) is ObjectProperty]
            
                fromclass_edges = self.get_class_parents(front)
                [new_frontier.append(child.uri) for child in fromclass_edges if type(child) is Class]    

            frontier = new_frontier
    
        return ClassSignature(class_uri, datatype_properties, object_properties)


    def _collect_from_node(self, node: TNode) -> Optional[Class|Object|DatatypeProperty|ObjectProperty]:
        if node == None or node.props.get(self.URI) == None or node.props.get(self.TITLE) == None:
            return None
        
        uri = node.props.get(self.URI)
        title = node.props.get(self.TITLE)

        if node.labels.count(CLASS):
            return Class(uri, title, node.props.get(self.DESCRIPTION))
        elif node.labels.count(OBJECT):
            return Object(uri, title, node.props.get(self.DESCRIPTION))
        elif node.labels.count(PROPERTY_LABEL):
            return DatatypeProperty(uri, title)
        elif node.labels.count(PROPERTY_LABEL_OBJECT):
            return ObjectProperty(uri, title)
        else:
            return None
        
    URI: str = "uri"
    DESCRIPTION: str = "description"
    TITLE: str = "title"