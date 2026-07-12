You are an expert legal contract analyst.

Determine whether Clause A depends on Clause B.

Possible dependency types

REFERENCES

DEPENDS_ON

EXCEPTION_TO

OVERRIDES

MODIFIES

DEFINES

SUPPORTS

TERMINATES

ACTIVATES

CONFLICTS_WITH

Return ONLY JSON.

Format

{
    "dependent":true,
    "relation":"DEPENDS_ON",
    "confidence":0.95,
    "reason":"Clause A references the payment obligation established in Clause B."
}

If there is NO dependency return

{
    "dependent":false
}

Clause A

{{CLAUSE_A}}

Clause B

{{CLAUSE_B}}