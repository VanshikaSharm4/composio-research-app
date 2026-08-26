from typing import Literal
from pydantic import BaseModel, Field


class ResearchResult(BaseModel):
    app_id: int
    app_name: str
    category: str

    description: str = Field(
        description="One-line description of what the application does."
    )

    auth_methods: list[str] = Field(
        description="Authentication methods such as OAuth2, API key, Basic, bearer token, JWT, etc."
    )

    self_serve: Literal[
        "free",
        "trial",
        "paid",
        "admin_required",
        "partner_gated",
        "contact_sales",
        "unknown"
    ]

    self_serve_details: str

    api_type: list[str] = Field(
        description="API types such as REST, GraphQL, SOAP, SDK, webhook, etc."
    )

    api_breadth: Literal[
        "broad",
        "moderate",
        "narrow",
        "unknown"
    ]

    mcp_available: bool | None

    mcp_details: str

    buildability: Literal[
        "easy",
        "possible",
        "difficult",
        "blocked",
        "unknown"
    ]

    main_blocker: str

    evidence_url: str

    evidence_quote: str

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )