from flask import jsonify
from app import app, driver
from parser_args import node_args, relationship_args, search_args
from utils import build_search_where_clause
from errors import CustomFlaskParser
from webargs import fields, validate
from webargs.flaskparser import use_args
from neo4j.exceptions import ClientError

parser = CustomFlaskParser()

@app.route('/nodes', methods=['POST'])
@parser.use_args(node_args, location="json")
def create_node(args):
    with driver.session() as session:
        params = ', '.join(f"{key}: ${key}" for key in args)
        query = f"CREATE (n:Node {{{params}}}) RETURN id(n)"
        node_id = session.run(query, args).single().value()
    return jsonify({"id": node_id}), 201

@app.route('/nodes/<id>', methods=['GET'])
def get_node(id):
    with driver.session() as session:
        result = session.run("MATCH (n:Node) WHERE id(n) = $id RETURN n", {"id": int(id)}).single()
        if result is None:
            return jsonify({'error': 'Node not found'}), 404
        node = result.value()
        node_properties = dict(node)
        node_properties["created_at"] = node_properties["created_at"].isoformat()
    return jsonify(node_properties)

@app.route('/nodes/<id>', methods=['PUT'])
@parser.use_args(node_args, location="json")
def update_node(args, id):
    with driver.session() as session:
        params = ', '.join(f"{key}: ${key}" for key in args)
        query = f"MATCH (n:Node) WHERE id(n) = $id SET n += {{{params}}} RETURN n"
        node = session.run(query, {"id": int(id), **args}).single().value()
        node_properties = dict(node)
    return jsonify(node_properties)

@app.route('/nodes/<id>', methods=['DELETE'])
def delete_node(id):
    with driver.session() as session:
        query = """
            MATCH (n:Node)
            WHERE id(n) = $id
            DELETE n
            RETURN count(n) as deleted_count
        """
        deleted_count = session.run(query, {"id": int(id)}).single()["deleted_count"]
        if deleted_count == 0:
            return jsonify({"error": "Node not found"}), 404
    return jsonify({"message": f"Node '{id}' successfully deleted"}), 200

@app.route('/search', methods=['GET'])
@parser.use_args(search_args, location="query")
def search(args):
    where_caluses, params = build_search_where_clause(args)

    try:
        with driver.session() as session:
            query = f"""
                MATCH (n:Node)
                WHERE {" AND ".join(where_caluses)}
                RETURN id(n) as node_id, n as node
                ORDER BY n.weight DESC
            """
            
            nodes = session.run(query, params)
            nodes_properties = []
            for record in nodes:
                node_properties = dict(record["node"])
                node_properties["created_at"] = node_properties["created_at"].isoformat()
                nodes_properties.append({"node_id": record["node_id"], **node_properties})
    except ClientError as e:
        return jsonify({"error": e.message}), 400
    print(nodes_properties)
    return jsonify(nodes_properties)

@app.route('/nodes/<id>/relationships', methods=['POST'])
@parser.use_args(relationship_args, location="json")
def create_relationship(args, id):
    with driver.session() as session:
        query = """
            MATCH (a:Node), (b:Node)
            WHERE id(a) = $id AND id(b) = $target_id
            MERGE (a)-[r:RELATED_TO]->(b)
            SET r.weight = $weight, r.accuracy = $accuracy, r.authenticity = $authenticity, r.confidence = $confidence, r.relevance = $relevance, r.credibility = $credibility, r.reasoning = $reasoning, r.created_at = $created_at
            RETURN id(r) as relationship_id
        """
        relationship_id = session.run(query, {"id": int(id), **args}).single().value()
    return jsonify({"relationship_id": relationship_id}), 201

@app.route('/nodes/<id>/relationships', methods=['GET'])
@parser.use_args({"order_by": fields.Str(validate=validate.OneOf(["weight", "accuracy", "authenticity", "confidence", "relevance", "credibility"]), load_default="weight")}, location="query")
def get_relationships(args, id):
    order_by = args.get("order_by")
    with driver.session() as session:
        query = f"""
            MATCH (n:Node)-[r]->(m)
            WHERE id(n) = $id
            RETURN id(r) as relationship_id, id(m) as node_id, r.weight as weight, r.accuracy as accuracy, r.authenticity as authenticity, r.confidence as confidence, r.relevance as relevance, r.credibility as credibility, r.reasoning as reasoning, r.created_at as created_at
            ORDER BY r.{order_by} DESC
        """
        relationships = session.run(query, {"id": int(id)})
        relationships_properties = [{"relationship_id": record["relationship_id"], "node_id": record["node_id"], "weight": record["weight"], "accuracy": record["accuracy"], "authenticity": record["authenticity"], "confidence": record["confidence"], "relevance": record["relevance"], "credibility": record["credibility"], "reasoning": record["reasoning"], "created_at": record["created_at"].isoformat()} for record in relationships]
    return jsonify(relationships_properties)

@app.route('/relationships/<id>', methods=['DELETE'])
def delete_relationship(id):
    with driver.session() as session:
        query = """
            MATCH ()-[r]->()
            WHERE id(r) = $id
            DELETE r
            RETURN count(r) as deleted_count
        """
        deleted_count = session.run(query, {"id": int(id)}).single()["deleted_count"]
        if deleted_count == 0:
            return jsonify({"error": "Relationship not found"}), 404
    return jsonify({"message": "Relationship deleted successfully"}), 200

@app.route('/documentation', methods=['GET'])
def get_documentation():
    description = os.getenv("DESCRIPTION")
    name = os.getenv("NAME")
    return jsonify({"name": name, "description": description})

@app.route('/delete_all', methods=['DELETE'])
def delete_all():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    return jsonify({"message": "All nodes and relationships deleted successfully"}), 200
