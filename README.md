# Semantic network

A semantic network stores concepts within a graph-based data structure and accessible via an API. Each semantic network will be atomic for a specific subject, for example, a Python coding semantic network or a semantic network based on your email inbox. A Python coding semantic network may be read-only and publicly accessible while your email inbox semantic network would be read/write and private. The concepts and relationships will be added to the semantic network via an orchestrator.

# Development

1. Ensure you have [pipenv](https://pipenv.pypa.io/en/latest/) installed
2. Run `pipenv install` to install the dependencies
3. Run `pipenv shell` to shell into your environment

# Deployment

Example `docker-compose.yaml`

```
version: '3'
services:
  web:
    image: ghcr.io/reasonableai/semantic-network:latest
    ports:
      - "5000:5000"
    environment:
      - NEO4J_URI=neo4j://db:7687
      - NEO4J_USERNAME=neo4j
      - NEO4J_PASSWORD=superlongsecret
      - |
        API_DOCUMENTATION=API documentation
        This API is useful for answering questions about Python coding.
    depends_on:
      - db

  db:
    image: neo4j:latest
    environment:
      - NEO4J_AUTH=neo4j/superlongsecret
    ports:
      - "7687:7687"
    volumes:
      - neo4j_data:/data

volumes:
  neo4j_data:
```

```bash
$ docker-compose up
```

# API Documentation

This API is built using Flask and Neo4j. It provides endpoints to create, read, update, delete and search nodes and relationships in a Neo4j graph database.

## Models

### Node

A `Node` represents a document in the system. It has the following fields:

- `document`: (String) The content of the document. This field is required.
- `keywords`: (List of Strings) Keywords associated with the document.
- `source`: (String) The source of the document.
- `credibility`: (Float) The credibility score of the document, ranging from 0 to 1.
- `accuracy`: (Float) The accuracy score of the document, ranging from 0 to 1.
- `authenticity`: (Float) The authenticity score of the document, ranging from 0 to 1.
- `confidence`: (Float) The confidence score of the document, ranging from 0 to 1.
- `relevance`: (Float) The relevance score of the document, ranging from 0 to 1.
- `type`: (String) The type of the document.
- `created_at`: (DateTime) The time when the document was created.

### Relationship

A `Relationship` represents a connection between two nodes. It has the following fields:

- `target_id`: (Integer) The id of the target node. This field is required.
- `weight`: (Float) The weight of the relationship, ranging from 0 to 1.
- `accuracy`: (Float) The accuracy score of the relationship, ranging from 0 to 1.
- `authenticity`: (Float) The authenticity score of the relationship, ranging from 0 to 1.
- `confidence`: (Float) The confidence score of the relationship, ranging from 0 to 1.
- `relevance`: (Float) The relevance score of the relationship, ranging from 0 to 1.
- `credibility`: (Float) The credibility score of the relationship, ranging from 0 to 1.
- `reasoning`: (String) The reasoning behind the relationship.
- `created_at`: (DateTime) The time when the relationship was created.

# Flask API Documentation

This API is built using Flask and Neo4j. It provides endpoints for creating, updating, retrieving, and deleting nodes and relationships in a Neo4j graph database. It also provides a search functionality to find nodes based on various parameters.

## Endpoints

### POST /nodes

Creates a new node.

**Request**

```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "document": "document1",
    "keywords": ["keyword1", "keyword2"],
    "source": "source1",
    "credibility": 0.8,
    "accuracy": 0.9,
    "authenticity": 0.7,
    "confidence": 0.6,
    "relevance": 0.5,
    "type": "type1"
}' "http://localhost:5000/nodes"
```

**Response**

```json
{
    "id": 1
}
```

### GET /nodes/{id}

Retrieves a node by its ID.

**Request**

```bash
curl -X GET "http://localhost:5000/nodes/1"
```

**Response**

```json
{
    "document": "document1",
    "keywords": ["keyword1", "keyword2"],
    "source": "source1",
    "credibility": 0.8,
    "accuracy": 0.9,
    "authenticity": 0.7,
    "confidence": 0.6,
    "relevance": 0.5,
    "type": "type1",
    "created_at": "2022-01-01T00:00:00Z"
}
```

### PUT /nodes/{id}

Updates a node by its ID.

**Request**

```bash
curl -X PUT -H "Content-Type: application/json" -d '{
    "document": "document2",
    "keywords": ["keyword3", "keyword4"],
    "source": "source2",
    "credibility": 0.7,
    "accuracy": 0.8,
    "authenticity": 0.6,
    "confidence": 0.5,
    "relevance": 0.4,
    "type": "type2"
}' "http://localhost:5000/nodes/1"
```

**Response**

```json
{
    "document": "document2",
    "keywords": ["keyword3", "keyword4"],
    "source": "source2",
    "credibility": 0.7,
    "accuracy": 0.8,
    "authenticity": 0.6,
    "confidence": 0.5,
    "relevance": 0.4,
    "type": "type2",
    "created_at": "2022-01-01T00:00:00Z"
}
```

### DELETE /nodes/{id}

Deletes a node by its ID.

**Request**

```bash
curl -X DELETE "http://localhost:5000/nodes/1"
```

**Response**

```json
{
    "message": "Node '1' deleted successfully"
}
```

### GET /search

Searches for nodes based on various parameters. 

**Parameters:**

- `query`: A string that should be contained in the document of the nodes.
- `keywords`: A comma-separated list of keywords that should be contained in the keywords of the nodes.
- `min_credibility`: The minimum credibility score of the nodes.
- `min_accuracy`: The minimum accuracy score of the nodes.
- `min_authenticity`: The minimum authenticity score of the nodes.
- `min_confidence`: The minimum confidence score of the nodes.
- `min_relevance`: The minimum relevance score of the nodes.
- `type`: The type of the nodes.
- `regex`: A regular expression that the document of the nodes should match.

**Examples:**

1. Search for nodes containing a specific query in the document:

    **Request**

    ```bash
    curl -X GET "http://localhost:5000/search?query=document2"
    ```

2. Search for nodes containing specific keywords:

    **Request**

    ```bash
    curl -X GET "http://localhost:5000/search?keywords=keyword3,keyword4"
    ```

3. Search for nodes with a minimum credibility score:

    **Request**

    ```bash
    curl -X GET "http://localhost:5000/search?min_credibility=0.7"
    ```

4. Search for nodes of a specific type:

    **Request**

    ```bash
    curl -X GET "http://localhost:5000/search?type=type2"
    ```

5. Search for nodes matching a regular expression:

    **Request**

    ```bash
    curl -X GET "http://localhost:5000/search?regex=document.*"
    ```

6. Search for nodes using a combination of parameters:

    **Request**

    ```bash
    curl -X GET "http://localhost:5000/search?query=document2&keywords=keyword3,keyword4&min_credibility=0.7&min_accuracy=0.8&min_authenticity=0.6&min_confidence=0.5&min_relevance=0.4&type=type2&regex=document.*"
    ```

**Response**

```json
[
    {
        "node_id": 1,
        "document": "document2",
        "keywords": ["keyword3", "keyword4"],
        "source": "source2",
        "credibility": 0.7,
        "accuracy": 0.8,
        "authenticity": 0.6,
        "confidence": 0.5,
        "relevance": 0.4,
        "type": "type2",
        "created_at": "2022-01-01T00:00:00Z"
    }
]
```

### POST /nodes/{id}/relationships

Creates a new relationship from a node.

**Request**

```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "target_id": 2,
    "weight": 0.9,
    "accuracy": 0.8,
    "authenticity": 0.7,
    "confidence": 0.6,
    "relevance": 0.5,
    "credibility": 0.4,
    "reasoning": "reasoning1"
}' "http://localhost:5000/nodes/1/relationships"
```

**Response**

```json
{
    "relationship_id": 1
}
```

### GET /nodes/{id}/relationships

Retrieves relationships of a node.

**Request**

```bash
curl -X GET "http://localhost:5000/nodes/1/relationships?order_by=weight"
```

**Response**

```json
[
    {
        "relationship_id": 1,
        "node_id": 2,
        "weight": 0.9,
        "accuracy": 0.8,
        "authenticity": 0.7,
        "confidence": 0.6,
        "relevance": 0.5,
        "credibility": 0.4,
        "reasoning": "reasoning1",
        "created_at": "2022-01-01T00:00:00Z"
    }
]
```

### DELETE /relationships/{id}

Deletes a relationship by its ID.

**Request**

```bash
curl -X DELETE "http://localhost:5000/relationships/1"
```

**Response**

```json
{
    "message": "Relationship '1' deleted successfully"
}
```

### GET /documentation

Retrieves the documentation of the API.

**Request**

```bash
curl -X GET "http://localhost:5000/documentation"
```

**Response**

```json
{
    "name": "Flask API",
    "description": "This API is built using Flask and Neo4j."
}
```

### DELETE /delete_all

Deletes all nodes and relationships.

**Request**

```bash
curl -X DELETE "http://localhost:5000/delete_all"
```

**Response**

```json
{
    "message": "All nodes and relationships deleted successfully"
}
