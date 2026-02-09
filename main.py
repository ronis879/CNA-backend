from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CNA Backend", version="Phase 2")

# -------------------------
# Health Check
# -------------------------
@app.get("/")
def root():
    return {"message": "CNA Phase 2 is running"}

@app.get("/health")
def health():
    return {
        "status": "OK",
        "module": "CNA Phase 2 – Draft Engine"
    }

# -------------------------
# Data Model
# -------------------------
class GSTDraftRequest(BaseModel):
    notice_type: str
    section: str
    financial_year: str
    taxpayer_name: str
    issue_summary: str

# -------------------------
# Draft Generator (Logic v1)
# -------------------------
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
