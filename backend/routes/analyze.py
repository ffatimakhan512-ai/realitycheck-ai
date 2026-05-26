from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from backend.services.analyzer import analyze_content

router = APIRouter()

class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[str] = None

class HighlightItem(BaseModel):
    word: str
    category: str
    explanation: str
    start_idx: int
    end_idx: int

class AnalysisData(BaseModel):
    input_type: str
    source: str
    text_length: int
    word_count: int
    score: int
    fake_probability: float
    bias: str
    highlights: List[HighlightItem]
    explanations: List[str]
    fallback_used: bool
    scrape_error: Optional[str] = None
    raw_text: str

class AnalyzeResponse(BaseModel):
    status: str
    data: AnalysisData

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest):
    """
    POST /analyze
    Consumes a text block or target news URL and triggers credibility computations.
    """
    # Quick client-side validation check
    if not payload.text and not payload.url:
        raise HTTPException(
            status_code=400, 
            detail="Invalid request. Please input a URL link or a news article text block."
        )
        
    try:
        result = analyze_content(text=payload.text, url=payload.url)
        return result
    except ValueError as val_err:
        # Catch business logic/validation exceptions and map to clean HTTP 400 Bad Requests
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as exc:
        # Catch unexpected server faults and map to HTTP 500 Internal Server Errors
        raise HTTPException(status_code=500, detail=f"Analysis Engine Error: {str(exc)}")
