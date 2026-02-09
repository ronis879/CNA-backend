from fastapi import FastAPI
from pydantic import BaseModel
from templates_registry import TEMPLATE_REGISTRY

app = FastAPI(title="CNA Backend", version="Phase 3")

# -------------------------
# Utilities
# -------------------------
def resolve_template(law: str, notice_type: str):
    law = law.upper()
    notice_type = notice_type.upper()

    if law not in TEMPLATE_REGISTRY:
        return None

    return TEMPLATE_REGISTRY[law].get(notice_type)

# -------------------------
# Health Check
# -------------------------
@app.get("/")
def root():
    return {"message": "CNA Phase 3 is running"}

@app.get("/health")
def health():
    return {
        "status": "OK",
        "module": "CNA Phase 3 – Analysis + Draft Engine"
    }

# -------------------------
# Template Resolver
# -------------------------
class TemplateResolveRequest(BaseModel):
    law: str
    notice_type: str

@app.post("/resolve-template")
def resolve_template_api(payload: TemplateResolveRequest):
    result = resolve_template(payload.law, payload.notice_type)

    if not result:
        return {"error": "No matching template found"}

    return {"template_selected": result}

# -------------------------
# Phase B1 – Notice Analyzer
# -------------------------
@app.post("/analyze-notice")
def analyze_notice(payload: dict):
    law = payload.get("law")
    notice_type = payload.get("notice_type")
    section = payload.get("section")

    if not law or not notice_type or not section:
        return {"error": "law, notice_type, and section are required"}

    law = law.upper()
    notice_type = notice_type.upper()
    section = str(section)

    if law == "GST" and notice_type == "DRC-01":
        if section == "73":
            return {
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
                "suggested_template": "GST_DRC01_73_REPLY",
                "next_action": "Proceed to draft generation"
            }

        if section == "74":
            return {
                "law": "GST",
                "notice_type": "DRC-01",
                "section": "74",
                "risk_level": "Very High",
                "fraud_category": "Fraud / Wilful Misstatement",
                "mandatory_fields": [
                    "financial_year",
                    "taxpayer_name",
                    "gstin",
                    "issue_summary",
                    "supporting_documents"
                ],
                "suggested_template": "GST_DRC01_74_REPLY",
                "next_action": "High-risk detailed defense required"
            }

    return {"error": "Unsupported notice type or law"}

# -------------------------
# Phase 2 – Draft Generator
# -------------------------
class GSTDraftRequest(BaseModel):
    notice_type: str
    section: str
    financial_year: str
    taxpayer_name: str
    issue_summary: str

@app.post("/draft/gst-reply")
def generate_gst_draft(data: GSTDraftRequest):
    draft = f"""
To  
The Proper Officer  
GST Department  

Subject: Reply to {data.notice_type} issued under Section {data.section}  
Financial Year: {data.financial_year}

Respected Sir/Madam,

This is in reference to the above-mentioned notice issued to
{data.taxpayer_name}.

Issue:
{data.issue_summary}

The taxpayer submits that all statutory compliances have been duly complied with.
Any apparent discrepancy is explainable and non-fraudulent.

It is requested that this reply be kindly considered and an opportunity of being
heard be granted before passing any adverse order.

Thanking you.

Yours faithfully,  
Authorized Signatory
"""

    return {
        "status": "Draft Generated",
        "draft_text": draft.strip()
    }
