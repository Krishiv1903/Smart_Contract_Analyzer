You are an expert Legal Knowledge Graph builder.

Determine relationships BETWEEN entities inside the same clause.

Possible relations include

HAS_ACTION

PERFORMS

OWNS

USES

PAYS

RECEIVES

HAS_PERMISSION

HAS_PROHIBITION

HAS_CONDITION

HAS_OBLIGATION

HAS_RISK

REFERENCES

DEFINES

Return ONLY JSON.

Format

{
    "relations":[
        {
            "id":"R1",
            "source_entity":"E1",
            "target_entity":"E2",
            "relation":"HAS_OBLIGATION",
            "confidence":0.96
        }
    ]
}

Return empty list if no relations exist.

Clause

{{CLAUSE}}