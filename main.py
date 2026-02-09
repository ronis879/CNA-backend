from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from templates_registry import TEMPLATE_REGISTRY
from template_metadata import TEMPLATE_METADATA

app = FastAPI(
    title="CNA Backend",
    version="Phase C2.2",
    description="AI-powered backend for tax & compliance drafting"
)

# -------------------------------------------------
# Utilities
# -------------------------------------------------
def resolve_template(law: str, notice_type: str):
    law = law.upper()
    notice_type = notice_type.upper()

    if law not in TEMPLATE_REGISTRY:
        return None

    return TEMPLATE_REGISTRY[law].get(notice_type)


# -------------------------------------------------
# Health & Root
# -------------------------------------------------
@app.get("/")
def root():
    return {"message": "CNA Backend is running"}

@app.get("/health")
def health():
    return {
        "status": "OK",
        "module": "CNA Draft Engine",
        "phase": "C2.2"
    }


# -------------------------------------------------
# Phase B – Template Resolver
# -------------------------------------------------
class TemplateResolveRequest(BaseModel):
    law: str
    notice_type: str

@app.post("/resolve-template")
def resolve_template_api(payload: TemplateResolveRequest):
    result = resolve_template(payload.law, payload.notice_type)

    if not result:
        return {"error": "No matching template found"}

    return {"template_selected": result}


# -------------------------------------------------
# Phase B1 – Notice Analysis Engine
# -------------------------------------------------
class AnalyzeNoticeRequest(BaseModel):
    law: str
    notice_type: str
    section: str

@app.post("/analyze-notice")
def analyze_notice(payload: AnalyzeNoticeRequest):
    law = payload.law.upper()
    notice_type = payload.notice_type.upper()
    section = str(payload.section)

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
                "next_action": "High-risk notice – detailed defense required"
            }

    return {"error": "Unsupported notice type or law"}


# -------------------------------------------------
# Phase C1 – GST Draft Generator
# -------------------------------------------------
class GSTDraftRequest(BaseModel):
    notice_type: str
    section: str
    financial_year: str
    taxpayer_name: str
    gstin: str
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

This is in reference to the above-mentioned notice issued to {data.taxpayer_name}.

The notice states the following issue:
{data.issue_summary}

At the outset, the taxpayer submits that all statutory compliances
have been duly complied with. Any apparent discrepancy may be due
to clerical or reconciliation differences, which are explainable
with supporting records.

The taxpayer humbly requests your good office to kindly consider
this reply and grant an opportunity of being heard before passing
any adverse order.

Thanking you.

Yours faithfully,  
Authorized Signatory
"""

    return {
        "status": "Draft Generated",
        "draft_text": draft.strip()
    }


# -------------------------------------------------
# Phase C2.2 – Unified CNA Draft Engine (FINAL)
# -------------------------------------------------
class CNADraftRequest(BaseModel):
    law: str
    notice_type: str
    section: str
    financial_year: str
    taxpayer_name: str
    gstin: str
    issue_summary: str
    drafting_mode: Optional[str] = "normal"  # OPTIONAL & DEFAULT

@app.post("/cna/draft")
def cna_draft(payload: CNADraftRequest):
    law = payload.law.upper()
    notice_type = payload.notice_type.upper()
    section = payload.section
    mode = payload.drafting_mode.lower()

    template_key = f"{law}_{notice_type}_{section}_REPLY"

    metadata = TEMPLATE_METADATA.get(template_key)
    if not metadata:
        return {"error": "No template metadata found"}

    # Tone handling (Phase C2.2)
    tone_map = {
        "normal": "professional and balanced",
        "concise": "brief and precise",
        "aggressive": "firm and strongly defensive"
    }

    tone = tone_map.get(mode, tone_map["normal"])

    draft = f"""
To  
The Proper Officer  
{metadata['authority']}  

Subject: {metadata['subject']}  
Financial Year: {payload.financial_year}

Respected Sir/Madam,

This reply is submitted in response to the notice issued to
{payload.taxpayer_name} (GSTIN: {payload.gstin}).

Issue under reference:
{payload.issue_summary}

The taxpayer submits this reply in a {tone} manner.
All statutory compliances have been duly fulfilled.
Any perceived discrepancy is explainable and supported
by records available on file.

The taxpayer respectfully requests an opportunity of
being heard before any adverse decision is taken.

Thanking you.

Yours faithfully,  
Authorized Signatory
"""

    return {
        "status": "CNA Draft Generated",
        "drafting_mode": mode,
        "template_used": template_key,
        "draft_text": draft.strip()
    }
