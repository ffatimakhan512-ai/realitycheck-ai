import unittest
from backend.utils.nlp import calculate_score, detect_bias, extract_keywords

class TestNLPAlgorithms(unittest.TestCase):
    """
    Unit testing suite for core rule-based NLP analyzer functions.
    Verifies calculation models, sensationalism density, and bias categorizations.
    """

    def test_clean_objective_news(self):
        """
        Tests a perfectly formal, neutral press release. 
        It should register high credibility, zero clickbait matches, and neutral bias.
        """
        text = (
            "The Department of Energy announced a new federal grant program "
            "designed to improve domestic silicon solar cell manufacturing. "
            "The initiative allocates fifty million dollars to research centers "
            "aimed at increasing photolithic module efficiency levels next year."
        )
        
        # Verify keywords/highlights
        highlights = extract_keywords(text)
        self.assertEqual(len(highlights), 0)

        # Verify bias classification
        bias = detect_bias(text)
        self.assertEqual(bias, "Neutral")

        # Verify credibility scoring
        cred, fake, explanations = calculate_score(text)
        self.assertGreaterEqual(cred, 90)
        self.assertLessEqual(fake, 15)
        self.assertIn("written with clean, highly neutral grammar", explanations[0])

    def test_clickbait_trigger_words(self):
        """
        Tests sensationalist text including standard clickbait triggers.
        It should capture offsets and downgrade credibility.
        """
        text = "This mind-blowing miracle cure has a secret trick that you won't believe!"
        
        # Verify keywords/highlights
        highlights = extract_keywords(text)
        # Should flag "mind-blowing", "miracle cure", "secret trick", "you won't believe"
        flagged_words = [h["word"].lower() for h in highlights]
        self.assertTrue(any("mind-blowing" in w for w in flagged_words))
        self.assertTrue(any("miracle cure" in w for w in flagged_words))
        self.assertTrue(any("secret trick" in w for w in flagged_words))
        self.assertTrue(any("you won't believe" in w for w in flagged_words))

        # Verify bias categorization (should classify as Sensationalist)
        bias = detect_bias(text)
        self.assertEqual(bias, "Sensationalist")

        # Verify credibility scoring deductions
        cred, fake, explanations = calculate_score(text)
        self.assertLessEqual(cred, 65)
        self.assertGreater(fake, 40)
        self.assertTrue(any("sensationalist" in exp or "clickbait" in exp for exp in explanations))

    def test_polarized_yelling_punctuation(self):
        """
        Tests extreme political opinion/yelling with massive exclamation usage
        and consecutive punctuation. Should register as highly polarized.
        """
        text = (
            "THIS IS AN UNPRECEDENTED SCANDAL!!! "
            "The corrupt politicians are taking your money and obviously the mainstream media lies "
            "about everything! We must rise up right now!??"
        )
        
        # Verify bias classification
        bias = detect_bias(text)
        self.assertEqual(bias, "Highly Polarized")

        # Verify credibility scoring model
        cred, fake, explanations = calculate_score(text)
        self.assertLessEqual(cred, 30)
        self.assertGreaterEqual(fake, 70)
        
        # Verify explanatory flags
        exps_str = " ".join(explanations)
        self.assertIn("capitalization density", exps_str)
        self.assertIn("excessive exclamation", exps_str)
        self.assertIn("consecutive punctuation", exps_str)

    def test_domain_reputation_audits(self):
        """
        Asserts credibility impacts of trusted vs. untrusted domain classifications.
        """
        text = "The local board voted to adjust commercial zoning regulations on Main Street."
        
        # Case A: Evaluated on a trusted domain
        cred_trust, fake_trust, _ = calculate_score(text, is_trusted_domain=True, is_blocked_domain=False)
        
        # Case B: Evaluated on a blocked/satire domain
        cred_block, fake_block, _ = calculate_score(text, is_trusted_domain=False, is_blocked_domain=True)

        self.assertGreater(cred_trust, cred_block)
        self.assertLess(fake_trust, fake_block)

    def test_empty_and_short_inputs(self):
        """
        Tests edge case behaviors under empty or extremely brief fragments.
        """
        # Empty input
        cred, fake, explanations = calculate_score("")
        self.assertEqual(cred, 0)
        self.assertEqual(fake, 100.0)
        
        # Short fragment
        cred_s, fake_s, explanations_s = calculate_score("Breaking news report.")
        self.assertLess(cred_s, 90) # Penalty for ultra-short texts
        self.assertTrue(any("very short" in exp or "brief" in exp for exp in explanations_s))

if __name__ == "__main__":
    unittest.main()
