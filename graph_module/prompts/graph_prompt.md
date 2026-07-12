You are constructing a Legal Knowledge Graph.

Given the following clause, identify

1. Nodes
2. Edges
3. Entity Types
4. Relationships

Return ONLY JSON.

Example

{
    "nodes":[
        {
            "id":"N1",
            "label":"User",
            "type":"PARTY"
        }
    ],

    "edges":[
        {
            "source":"N1",
            "target":"N2",
            "relation":"HAS_OBLIGATION"
        }
    ]
}

Clause

{{CLAUSE}}