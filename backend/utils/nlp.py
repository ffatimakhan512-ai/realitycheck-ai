import re
import math

# Compiled regex for clickbait & sensational triggers
CLICKBAIT_TRIGGERS = [
    (r"\bshocking\b", "shocking", "Sensational trigger designed to induce raw shock or emotional response rather than objective reporting."),
    (r"\byou won't believe\b", "you won't believe", "Classic clickbait hyperbole used to exploit the curiosity gap."),
    (r"\bmiracle cure\b", "miracle cure", "Unscientific claim of a simple remedy for complex health issues."),
    (r"\bsecret trick\b", "secret trick", "Implies a hidden hack, standard sensationalism to drive clicks."),
    (r"\bsecret revealed\b", "secret revealed", "Conspiratorial tone implying hidden knowledge is finally disclosed."),
    (r"\bconspiracy\b", "conspiracy", "Implies systemic hidden plots, typical of unverified news sources."),
    (r"\bproof they are hiding\b", "proof they are hiding", "Conspiratorial hype implying malicious concealment by authorities."),
    (r"\bdevastating truth\b", "devastating truth", "Highly emotional hyperbole intended to stir negative sentiment."),
    (r"\bmind-blowing\b", "mind-blowing", "Sensationalist adjective indicating extreme hyperbole."),
    (r"\bsensational\b", "sensational", "Highly emotional adjective seeking to exaggerate normal news."),
    (r"\bbreaking alert\b", "breaking alert", "Urgent framing used to construct fake panic or artificial urgency."),
    (r"\bunbelievable\b", "unbelievable", "Undermines factual reporting by appealing to incredulity."),
    (r"\bsecret agenda\b", "secret agenda", "Suggests paranoid framing without objective proof."),
    (r"\bwhat they don't want you to know\b", "what they don't want you to know", "Classic conspiracy catchphrase designed to induce suspicion.")
]

# Compiled regex for bias & extreme polarizing language
BIAS_TRIGGERS = [
    (r"\bobviously\b", "obviously", "Presumptuous wording that asserts a claim without presenting objective facts."),
    (r"\beveryone knows\b", "everyone knows", "Bandwagon fallacy, appealing to universal agreement rather than physical evidence."),
    (r"\bundeniably\b", "undeniably", "Blocks critical evaluation by declaring a controversial topic closed."),
    (r"\bdisastrous\b", "disastrous", "Extreme negative modifier showing heavy editorial slant rather than objective detail."),
    (r"\bevil\b", "evil", "Moralistic labeling which is subjective and emotionally charged."),
    (r"\bpure genius\b", "pure genius", "Extreme positive hyperbole reflecting an editorial fan base."),
    (r"\bunprecedented scandal\b", "unprecedented scandal", "Sensationalist framing of administrative actions to drum up outrage."),
    (r"\bcorrupt politicians\b", "corrupt politicians", "Broad generalization representing deep political cynicism and bias."),
    (r"\bmainstream media lies\b", "mainstream media lies", "Highly defensive polarizing narrative aimed at undermining media trust.")
]

def extract_keywords(text: str):
    """
    Scans the text for sensational clickbait or biased triggers.
    Returns a list of dicts with matching keywords, categories, descriptions, and text offsets.
    """
    highlights = []
    if not text:
        return highlights

    # Search for Clickbait triggers
    for pattern, name, desc in CLICKBAIT_TRIGGERS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            highlights.append({
                "word": match.group(0),
                "category": "clickbait",
                "explanation": desc,
                "start_idx": match.start(),
                "end_idx": match.end()
            })

    # Search for Bias triggers
    for pattern, name, desc in BIAS_TRIGGERS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            highlights.append({
                "word": match.group(0),
                "category": "bias",
                "explanation": desc,
                "start_idx": match.start(),
                "end_idx": match.end()
            })

    # Sort highlights by start_idx to maintain textual order
    highlights.sort(key=lambda x: x["start_idx"])
    return highlights

def detect_bias(text: str) -> str:
    """
    Determines bias category based on frequency of triggers, all-caps yelling, and punctuation.
    Categories: 'Neutral', 'Sensationalist', 'Highly Polarized'
    """
    if not text:
        return "Neutral"

    # Count bias and clickbait occurrences
    highlights = extract_keywords(text)
    bias_count = sum(1 for h in highlights if h["category"] == "bias")
    clickbait_count = sum(1 for h in highlights if h["category"] == "clickbait")

    # Count punctuation triggers
    exclamation_count = text.count("!")
    question_count = text.count("?")
    extreme_punc = len(re.findall(r"[!?]{2,}", text))

    # All caps word ratios (words of length >= 4 that are fully capitalized)
    words = re.findall(r"\b[A-Za-z]{4,}\b", text)
    caps_words = [w for w in words if w.isupper()]
    caps_ratio = len(caps_words) / len(words) if words else 0.0

    score_metric = bias_count * 2.0 + clickbait_count * 1.5 + exclamation_count * 0.8 + extreme_punc * 2.5 + caps_ratio * 5.0

    if score_metric >= 7.0:
        return "Highly Polarized"
    elif score_metric >= 2.5:
        return "Sensationalist"
    else:
        return "Neutral"

def calculate_score(text: str, is_trusted_domain: bool = None, is_blocked_domain: bool = False) -> tuple:
    """
    Computes a multi-dimensional credibility score (0 - 100) and fake news probability (0 - 100).
    Returns (credibility_score, fake_probability, explanations)
    """
    explanations = []
    
    if not text or len(text.strip()) == 0:
        return 0, 100.0, ["No text content provided for analysis."]

    credibility = 100.0

    # 1. Evaluate length. Very short text (< 30 characters) is harder to verify and prone to rumors.
    text_len = len(text.strip())
    if text_len < 50:
        credibility -= 15.0
        explanations.append("The analyzed content is very short. Brief fragments are highly prone to rumor-spreading due to lack of standard journalistic context.")
    elif text_len < 150:
        credibility -= 5.0
        explanations.append("The content is relatively brief. Headlines and soundbites often oversimplify news context.")

    # 2. Clickbait and Bias matches
    highlights = extract_keywords(text)
    clickbait_count = sum(1 for h in highlights if h["category"] == "clickbait")
    bias_count = sum(1 for h in highlights if h["category"] == "bias")

    if clickbait_count > 0:
        deduction = min(clickbait_count * 8.0, 30.0)
        credibility -= deduction
        clickbait_samples = [f"'{h['word']}'" for h in highlights if h['category'] == 'clickbait'][:2]
        clickbait_str = ", ".join(clickbait_samples)
        explanations.append(f"Detected {clickbait_count} sensationalist/clickbait trigger phrase(s) (e.g. {clickbait_str}). Authentic news uses objective reporting lines.")

    if bias_count > 0:
        deduction = min(bias_count * 10.0, 35.0)
        credibility -= deduction
        bias_samples = [f"'{h['word']}'" for h in highlights if h['category'] == 'bias'][:2]
        bias_str = ", ".join(bias_samples)
        explanations.append(f"Detected {bias_count} heavily biased or opinionated phrase(s) (e.g. {bias_str}). Reliable journalism aims for neutral and non-partisan framing.")

    # 3. Punctuation abnormalities
    exclamation_count = text.count("!")
    if exclamation_count > 0:
        deduction = min(exclamation_count * 4.0, 15.0)
        credibility -= deduction
        explanations.append(f"Found excessive exclamation marks ({exclamation_count}). Professional journalism relies on facts rather than punctuation to imply significance.")

    # Multiple consecutive punctuation marks (e.g., !!!, !?, ??)
    consec_punc = len(re.findall(r"[!?]{2,}", text))
    if consec_punc > 0:
        credibility -= 15.0
        explanations.append("Contains highly informal multiple consecutive punctuation marks (like '!!!' or '!?'). This suggests emotional pleading, standard in misinformation.")

    # 4. Yelling Ratio (ALL CAPS)
    words = re.findall(r"\b[A-Za-z]{4,}\b", text)
    caps_words = [w for w in words if w.isupper()]
    if words and len(caps_words) > 0:
        caps_ratio = len(caps_words) / len(words)
        if caps_ratio > 0.1:
            deduction = min(caps_ratio * 40.0, 25.0)
            credibility -= deduction
            explanations.append(f"High capitalization density detected ({caps_ratio:.1%} of words are ALL CAPS). Capitalization is often used online to mimic yelling and drive shock value.")

    # 5. Domain trust evaluations (if URL analyzed)
    if is_blocked_domain:
        credibility -= 40.0
        explanations.append("The source domain is flagged in our database as a known unreliable, satirical, or fake news publication network.")
    elif is_trusted_domain is True:
        credibility += 15.0
        explanations.append("The source domain is matched against our registry of highly verified press agencies and neutral institutional outlets.")
    elif is_trusted_domain is False:
        credibility -= 10.0
        explanations.append("The source domain is an unverified, generic, or fringe publisher. Exercise analytical caution.")

    # Bound credibility between 0 and 100
    credibility = max(0.0, min(100.0, credibility))
    credibility = round(credibility)

    # 6. Calculate Fake News Probability based on credibility and extreme characteristics
    # Higher bias + hyperbole = higher fake news probability
    fake_prob = 100.0 - credibility
    if clickbait_count > 2 or bias_count > 2:
        fake_prob = max(fake_prob, 75.0)

    # Let's adjust fake news probability if there is a known fake domain
    if is_blocked_domain:
        fake_prob = max(fake_prob, 90.0)
    elif is_trusted_domain is True:
        fake_prob = min(fake_prob, 15.0)

    fake_prob = round(fake_prob, 1)

    if len(explanations) == 0:
        explanations.append("The analyzed content is written with clean, highly neutral grammar and objective vocabulary. No anomalies or clickbait detected.")

    return credibility, fake_prob, explanations
