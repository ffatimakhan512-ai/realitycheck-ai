from backend.services.scraper import scrape_url
from backend.utils.nlp import calculate_score, detect_bias, extract_keywords

def analyze_content(text: str = None, url: str = None) -> dict:
    """
    Orchestrates the verification process. 
    Accepts text inputs, URL inputs, or both, performs validation,
    and returns a structured JSON payload for analysis metrics.
    """
    if not text and not url:
        raise ValueError("Empty request. Please supply either a URL link or a text block to analyze.")

    source_label = "Direct Text Input"
    analysis_text = text or ""
    is_trusted = None
    is_blocked = False
    input_type = "text"
    scrape_error = None
    fallback_used = False

    # 1. Scrape if a URL is provided
    if url:
        url_stripped = url.strip()
        if not url_stripped:
            raise ValueError("The provided URL cannot be empty.")
            
        input_type = "url"
        scrape_res = scrape_url(url_stripped)
        
        if not scrape_res["success"] and not scrape_res.get("fallback"):
            raise ValueError(scrape_res["error"])

        analysis_text = scrape_res["text"]
        source_label = scrape_res["domain"]
        is_trusted = scrape_res["is_trusted"]
        is_blocked = scrape_res["is_blocked"]
        fallback_used = scrape_res.get("fallback", False)
        if fallback_used:
            scrape_error = scrape_res["error"]
    else:
        # Simple text length check
        if not analysis_text.strip():
            raise ValueError("The provided text block is empty. Please enter content to proceed.")

    # 2. NLP Metric computations
    credibility_score, fake_probability, explanations = calculate_score(
        analysis_text, 
        is_trusted_domain=is_trusted, 
        is_blocked_domain=is_blocked
    )
    bias_rating = detect_bias(analysis_text)
    highlights = extract_keywords(analysis_text)

    # 3. Calculate some basic text summaries for UI display
    text_length = len(analysis_text)
    word_count = len(analysis_text.split())

    # Build and return standard payload
    return {
        "status": "success",
        "data": {
            "input_type": input_type,
            "source": source_label,
            "text_length": text_length,
            "word_count": word_count,
            "score": credibility_score,
            "fake_probability": fake_probability,
            "bias": bias_rating,
            "highlights": highlights,
            "explanations": explanations,
            "fallback_used": fallback_used,
            "scrape_error": scrape_error,
            "raw_text": analysis_text
        }
    }
