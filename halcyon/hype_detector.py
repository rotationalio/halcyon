import regex as re

import emoji
import numpy as np

from halcyon.scorer import TextScorer

MAX_HYPE_ELEM_CT = 15


class HypeDetector(TextScorer):
    """
    The HypeDetector uses ML to detect hype in online content
    """

    def __init__(self, model: object):
        self.model = model[0]
        self.vectorizer = model[1]
        self.labels = ["not_hype", "hype"]

    def _normalize(self, value: int, min_value: int, max_value: int) -> float:
        """
        Normalize a value to the range [0, 1].
        """

        if value < min_value:
            return 0
        if value > max_value:
            return 1
        return (value - min_value) / (max_value - min_value)

    def clean_text(self, text: str) -> str:
        """
        Strip out common text
        """
        all_patterns = [
            "…see more",
            "https://lnkd.in/",
            "www.bit.ly/",
            "http://bit.ly",
            "#",
        ]
        regex_pattern = r"|".join(map(r"(?:{})".format, all_patterns))
        cleaned_text = re.sub(regex_pattern, "", text)
        return cleaned_text

    def _hype_score(self, text: str) -> float:
        """
        Returns a score in the range [0, 1] that is a representation of
        the number of hashtags, exclamation points, and emojis used in
        a post.  This scores gives further insight into how much a post
        is hyped up by the use of hashtags, emojis, and exclamation points
        to capture attention.
        """
        ht_count = text.count("#")
        exclamation_count = text.count("!")
        emoji_count = emoji.emoji_count(text)
        total_hype_elem_ct = ht_count + exclamation_count + emoji_count
        return self._normalize(total_hype_elem_ct, 1, MAX_HYPE_ELEM_CT)

    def score(self, text: str) -> dict:
        """
        Return a dict of scores that represents how likely the text
        represents hyped up or promotional content.
        """
        text_cleaned = self.clean_text(text)
        text_vec = self.vectorizer.transform([text_cleaned]).toarray()
        probs = self.model.predict_proba(text_vec)
        pred = self.model.predict(text_vec)
        model_score = round(np.max(probs), 3)
        hype_score = self._hype_score(text)
        return {
            "classification": self.labels[pred[0]],
            "model_score": round(model_score, 3),
            "hype_score": round(hype_score, 3),
        }
