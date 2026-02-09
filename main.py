from fastapi import FastAPI
from pydantic import BaseModel

from templates_registry import TEMPLATE_REGISTRY
from template_metadata import find_template

# -------------------------------------------------------------------
# App Init
# -------------------------------------------------------------------
app = FastAPI(
    title="CNA Backend",
    version="Phase C2.1",
    description="AI-powered backend for tax & compliance drafting"
)

# -------------------------------------------------------------------
# Utility: Resolve Template (Registry)
# -------------------------------------------------------------------
def resolve_template(law: str, notice_type: str):
    law = law.upper()
    notice_type = notice_type.upper()

    if law not in TEMPLATE_REGISTRY:
        return None

    return TEMPLATE_REGISTRY[law].get(notice_type)

# -------------------------------------------------------------------
# Health & Root
# -------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "CNA Backend is running"}

@app.get("/health")
def health():
    return {
        "status": "OK",
        "module": "CNA Phase C2.1 – Draft Intelligence Engine"
    }

# -------------------------------------------------------------------
# Data Models
# -------------------------------------------------------------------
class TemplateResolveRequest(BaseModel):
    law: str
    notice_type: str

class GSTDraftRequest(BaseModel):
    notice_type: str
    section: str
    financial_year: str
    taxpayer_name: str
    gstin: str
    issue_summary: str

class CNADraftRequest(BaseModel):
    law: str
    notice_type: str
    section: str
    financial_year: str
    taxpayer_name: str
    gstin: str
    issue_summary: str

# -------------------------------------------------------------------
# API: Resolve Template (Registry only)
# -------------------------------------------------------------------
@app.post("/resolve-template")
def resolve_template_api(payload: TemplateResolveRequest):
    result = resolve_template(payload.law, payload.notice_type)

    if not result:
        return {"error": "No matching template found"}

    return {"template_selected": result}

# -------------------------------------------------------------------
# API: Analyze Notice (Metadata Engine)  ✅ Phase C2.1
# -------------------------------------------------------------------
@app.post("/analyze-notice")
def analyze_notice(payload: dict):
    law = payload.get("law")
    notice_type = payload.get("notice_type")
    section = payload.get("section")

    if not law or not notice_type or not section:
        return {
            "error": "law, notice_type, and section are required"
        }

    template = find_template(law, notice_type, section)

    if not template:
        return {
            "error": "No template available for given notice"
        }

    return {
        "law": template["law"],
        "notice_type": template["notice_type"],
        "section": template["section"],
        "risk_level": template["risk_level"],
        "fraud_category": template["fraud_category"],
        "mandatory_fields": template["mandatory_fields"],
        "supported_actions": template["supported_actions"],
        "draft_styles": template["draft_styles"],
        "suggested_template": template["template_id"],
        "next_action": "Proceed to draft generation"
    }

# -------------------------------------------------------------------
# API: GST Draft Generator (Phase B)
# -------------------------------------------------------------------
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
{data.taxpayer_name} (GSTIN: {data.gstin}).

The notice states the following issue:
{data.issue_summary}

At the outset, the taxpayer submits that all statutory
compliances have been duly complied with. Any apparent
discrepancy may be due to clerical or reconciliation differences,
which are explainable with supporting records.

The taxpayer humbly requests your good office to kindly
consider this reply and grant an opportunity of being heard
before passing any adverse order.

Thanking you.

Yours faithfully,  
Authorized Signatory  
"""

    return {
        "status": "Draft Generated",
        "draft_text": draft.strip()
    }

# -------------------------------------------------------------------
# API: CNA Unified Draft (Phase C1)
# -------------------------------------------------------------------
@app.post("/cna/draft")
def cna_draft(payload: CNADraftRequest):

    # Step 1: Analyze notice
    template = find_template(payload.law, payload.notice_type, payload.section)

    if not template:
        return {
            "error": "No template available for given notice"
        }

    # Step 2: Validate mandatory fields
    missing = []
    for field in template["mandatory_fields"]:
        if not getattr(payload, field, None):
            missing.append(field)

    if missing:
        return {
            "status": "Validation Failed",
            "missing_fields": missing,
            "next_action": "Provide missing data"
        }

    # Step 3: Draft (GST handled internally for now)
    if payload.law.upper() == "GST":
        return generate_gst_draft(
            GSTDraftRequest(
                notice_type=payload.notice_type,
                section=payload.section,
                financial_year=payload.financial_year,
                taxpayer_name=payload.taxpayer_name,
                gstin=payload.gstin,
                issue_summary=payload.issue_summary
            )
        )

    return {
        "error": "Drafting not supported for this law yet"
    }
