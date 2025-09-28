from typing import List, Dict, Any, Optional, Tuple
import uuid
from neo4j import GraphDatabase, Result, Record
import json
from python_driver.entities import TNode, TArc

class GraphRepository:
    def __init__(self, uri: str, user: str, password: str, database: str = "neo4j"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database
        
    def close(self):
        self.driver.close()

    # method to use with with ... as construction
    def __enter__(self):
        return self

    # method to use with with ... as consturction
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    
    ######################################
    #   Node getter methods   #
    ######################################
    def get_all_nodes(self) -> List[TNode]:        
        with self.driver.session(database=self.database) as session:
            result = session.run("MATCH (n) RETURN n")

            nodes = [self._collect_node(record["n"]) for record in result]    
            return nodes
        
    def get_nodes_by_labels(self, labels: List[str]) -> List[TNode]:
        if not labels:
            return self.get_all_nodes()
        
        query = f"""MATCH (n:{self._transform_labels(labels)}) RETURN n"""
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query)
            
            nodes = [self._collect_node(record["n"]) for record in result]    
            return nodes


    def get_node_by_uri(self, uri: str) -> Optional[TNode]:
        query = """MATCH (n {uri: $uri}) RETURN n"""
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, uri=uri)
            record = result.single()
            
            if record:
                return self._collect_node(record["n"])
            
            return None
        
    def get_arcs_from_node(self, uri: str) -> List[TNode]:
        query = """
        MATCH (parent {uri: $uri})-[arc]->(child)
        RETURN arc, child, type(arc) as arc_type
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, uri=uri)
            children = []
            
            for record in result:
                child_data = record["child"]
                child_node = self._collect_node(child_data)
                children.append(child_node)
            
            return children

    def get_arcs_to_node(self, uri: str) -> List[TNode]:
        query = """
        MATCH (parent)-[arc]->(child {uri: $uri})
        RETURN arc, parent, type(arc) as arc_type
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, uri=uri)
            parents = []
            
            for record in result:
                parent_data = record["parent"]
                
                # Создаем объект родительского узла
                parent_node = self._collect_node(parent_data)
                parents.append(parent_node)

            return parents

    def get_all_nodes_and_arcs(self) -> List[TNode]:
        query = """
        MATCH (n)-[r]->(m)
        RETURN n, r, m.uri as to_uri, type(r) as rel_type
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query)
            nodes_dict = {}
            
            for record in result:
                node_data = record["n"]
                arc_data = record["r"]
                to_uri = record["to_uri"]
                rel_type = record["rel_type"]
                
                node_uri = node_data.get("uri")
                
                # Создаем или получаем узел
                if node_uri not in nodes_dict:
                    nodes_dict[node_uri] = self._collect_node(node_data)
                    nodes_dict[node_uri].arcs = []
                
                # Создаем дугу и добавляем к узлу
                arc = self._collect_arc(arc_data)
                arc.node_uri_from = node_uri
                arc.node_uri_to = to_uri
                arc.label = rel_type
                nodes_dict[node_uri].arcs.append(arc)
            
            return list(nodes_dict.values())

    ######################################
    #   Node creation/deletion methods   #
    ######################################
    def create_node(self, labels: List[str], props: Dict[str, Any]) -> TNode:
        # Генерируем URI если не предоставлен
        if "uri" not in props:
            props["uri"] = self._generate_random_uri()
        
        str_labels = self._transform_labels(labels)
        str_props = self._transform_props(props)
        query = f"""CREATE (n:{str_labels} {str_props}) RETURN n"""
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query)
            record = result.single()
            
            if record:
                return self._collect_node(record["n"])
                
            raise Exception("Failed to create node")
    

    def delete_node_by_uri(self, uri: str) -> bool:
        """
        Returns:
            bool: True если узел удален, False если не найден
        """
        query = """
            MATCH (n {uri: $uri})
            DETACH DELETE n
            RETURN count(n) as deleted_count
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, uri=uri)
            record = result.single()
            
            if record and record["deleted_count"] > 0:
                return True
            
            return False

    def update_node(self, uri: str, 
                    add_labels: Optional[List[str]] = None,
                    remove_labels: Optional[List[str]] = None,
                    set_props: Optional[Dict[str, Any]] = None,
                    remove_props: Optional[List[str]] = None) -> Optional[TNode]:
        """
        Обновить узел: добавление/удаление меток и свойств
        """
        if not any([add_labels, remove_labels, set_props, remove_props]):
            return self.get_node_by_uri(uri)
        
        clauses = []
        params = {"uri": uri}
        
        if remove_labels:
            for label in remove_labels:
                if label.strip():
                    clauses.append(f"REMOVE n:`{label}`")
        
        if remove_props:
            remove_clauses = []
            for prop in remove_props:
                if prop.strip() and key != "uri":
                    remove_clauses.append(f"n.{prop}")
            if remove_clauses:
                clauses.append(f"REMOVE {', '.join(remove_clauses)}")
        
        if add_labels:
            for label in add_labels:
                if label.strip():
                    clauses.append(f"SET n:`{label}`")
        
        if set_props:
            set_clauses = []
            for key, value in set_props.items():
                if key.strip() and key != "uri":
                    param_name = f"set_{key}"
                    set_clauses.append(f"n.{key} = ${param_name}")
                    params[param_name] = value
            if set_clauses:
                clauses.append(f"SET {', '.join(set_clauses)}")
        
        query = f"""
        MATCH (n {{uri: $uri}})
        {' '.join(clauses)}
        RETURN n
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, **params)
            record = result.single()
            
            if record:
                return self._collect_node(record["n"])
            
            return None

    ######################################
    #   Arc creation/deletion methods    #
    ######################################
    def create_arc(self, from_uri: str, to_uri: str, arc_label: str, props: Dict[str, Any] = {}) -> TArc:
        query = f"""
        MATCH (a {{uri: $from_uri}}), (b {{uri: $to_uri}})
        CREATE (a)-[r:{arc_label}]->(b)
        SET r = $props
        RETURN r, a.uri as from_uri, b.uri as to_uri
        """
        
        with self.driver.session(database=self.database) as session:
            result = session.run(query, from_uri=from_uri, to_uri=to_uri, props=props)
            record = result.single()
            
            if record:
                arc_data = record["r"]
                arc = self._collect_arc(arc_data)
                arc.node_uri_from = from_uri
                arc.node_uri_to = to_uri
                return arc
            
            raise Exception("Failed to create arc")

    def delete_arc_by_id(self, arc_id: int) -> bool:
        """            
        Returns:
            bool: True если связь удалена, False если не найдена
        """

        query = """
            MATCH ()-[r]-()
            WHERE elementId(r)=$arc_id
            DELETE r
            RETURN count(r) as deleted_count
        """
        with self.driver.session(database=self.database) as session:
            result = session.run(query, arc_id=arc_id)
            record = result.single()
            
            if record and record["deleted_count"] > 0:
                return True
            
            return False



    ######################################
    #   Additional and private methods   #
    ######################################
    def run_custom_query(self, query: str, **params) -> Result:
        with self.driver.session(database=self.database) as session:
            return session.run(query, **params)

    def _generate_random_uri(self, length: int = 16) -> str:
        return str(uuid.uuid4()).replace("-", "")[:length]

    def _collect_node_with_arcs(self, node_data) -> TNode:
        props = dict(node_data.items())
        
        return TNode(
            id=node_data.element_id,
            uri=props.get("uri", ""),
            labels=list(node_data.labels),
            props=props,
            arcs=None
        )
    
    def _collect_node(self, node_data) -> TNode:
        props = dict(node_data.items())
        
        return TNode(
            id=node_data.element_id,
            uri=props.get("uri", ""),
            labels=list(node_data.labels),
            props=props,
            arcs=None
        )

    def _collect_arc(self, arc_data) -> TArc:
        props = dict(arc_data.items())
        
        return TArc(
            id=arc_data.element_id,
            label=arc_data.type,
            props=props,
            node_uri_from="",  
            node_uri_to=""    
        )
    
    def _transform_labels(self, labels, separator = ':'):
        if len(labels) == 0:
            return '``'
        res = ''
        for l in labels:
            i = '`{l}`'.format(l=l) + separator
            res +=i
        return res[:-1]


    def _transform_props(self, props):
        if len(props) == 0:
            return ''
        data = "{"
        for p in props:
            temp = "`{p}`".format(p=p)
            temp +=':'
            temp += "{val}".format(val = json.dumps(props[p]))
            data += temp + ','
        data = data[:-1]
        data += "}"

        return data
