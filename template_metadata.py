# template_metadata.py
# Phase C2 – Template Intelligence Layer

TEMPLATE_METADATA = [
    {
        "template_id": "GST_DRC01_73_REPLY",
        "law": "GST",
        "notice_type": "DRC-01",
        "section": "73",
        "risk_level": "High",
        "fraud_category": "Non-Fraud",
        "mandatory_fields": [
            "financial_year",
            "taxpayer_name",
            "gstin",
            "issue_summary"
        ],
        "supported_actions": ["reply"],
        "draft_styles": ["standard", "brief", "detailed"]
    },
    {
        "template_id": "GST_DRC01_74_REPLY",
        "law": "GST",
        "notice_type": "DRC-01",
        "section": "74",
        "risk_level": "Very High",
        "fraud_category": "Fraud",
        "mandatory_fields": [
            "financial_year",
            "taxpayer_name",
            "gstin",
            "issue_summary",
            "supporting_documents"
        ],
        "supported_actions": ["reply"],
        "draft_styles": ["detailed", "legal_defense"]
    }
]


def find_template(law: str, notice_type: str, section: str):
    law = law.upper()
    notice_type = notice_type.upper()
    section = str(section)

    for tpl in TEMPLATE_METADATA:
        if (
            tpl["law"] == law and
            tpl["notice_type"] == notice_type and
            tpl["section"] == section
        ):
            return tpl

    return None
