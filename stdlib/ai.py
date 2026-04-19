import json
import re


class UntoldAI:
    """untold.ai — AI & ML module"""

    # ── Text utilities ────────────────────────────────────────
    @staticmethod
    def tokenize(text):
        return re.findall(r"\b\w+\b", text.lower())

    @staticmethod
    def word_count(text):
        return len(UntoldAI.tokenize(text))

    @staticmethod
    def char_count(text):
        return len(text)

    @staticmethod
    def sentences(text):
        return [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]

    @staticmethod
    def similarity(a, b):
        """Basic Jaccard similarity between two texts."""
        sa = set(UntoldAI.tokenize(a))
        sb = set(UntoldAI.tokenize(b))
        if not sa and not sb:
            return 1.0
        return len(sa & sb) / len(sa | sb)

    @staticmethod
    def sentiment(text):
        """Simple rule-based sentiment analysis."""
        positive = {"good","great","love","excellent","happy","best",
                    "awesome","fantastic","wonderful","amazing","perfect"}
        negative = {"bad","hate","terrible","awful","worst","horrible",
                    "poor","ugly","disgusting","broken","failed"}
        words    = set(UntoldAI.tokenize(text))
        pos      = len(words & positive)
        neg      = len(words & negative)
        if pos > neg:   return {"label": "positive", "score": pos}
        elif neg > pos: return {"label": "negative", "score": neg}
        else:           return {"label": "neutral",  "score": 0}

    @staticmethod
    def summarize(text, sentences=2):
        """Extractive summarization — returns top N sentences."""
        all_sentences = UntoldAI.sentences(text)
        words         = UntoldAI.tokenize(text)
        freq          = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1

        scored = []
        for s in all_sentences:
            score = sum(freq.get(w, 0) for w in UntoldAI.tokenize(s))
            scored.append((score, s))

        scored.sort(reverse=True)
        return " ".join(s for _, s in scored[:int(sentences)])

    @staticmethod
    def keywords(text, top=5):
        """Extract top N keywords by frequency."""
        stopwords = {"the","a","an","is","in","it","of","to","and",
                     "or","for","on","with","this","that","was","are"}
        words     = UntoldAI.tokenize(text)
        freq      = {}
        for w in words:
            if w not in stopwords:
                freq[w] = freq.get(w, 0) + 1
        return sorted(freq, key=freq.get, reverse=True)[:int(top)]

    # ── Math / ML helpers ─────────────────────────────────────
    @staticmethod
    def normalize(data):
        """Min-max normalize a list of numbers."""
        mn = min(data)
        mx = max(data)
        if mx == mn:
            return [0.0] * len(data)
        return [(x - mn) / (mx - mn) for x in data]

    @staticmethod
    def mean(data):
        return sum(data) / len(data)

    @staticmethod
    def median(data):
        s = sorted(data)
        n = len(s)
        if n % 2 == 0:
            return (s[n//2 - 1] + s[n//2]) / 2
        return s[n//2]

    @staticmethod
    def std(data):
        import math
        m = UntoldAI.mean(data)
        return math.sqrt(sum((x - m) ** 2 for x in data) / len(data))

    @staticmethod
    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))

    @staticmethod
    def cosine_similarity(a, b):
        import math
        dot   = UntoldAI.dot(a, b)
        mag_a = math.sqrt(UntoldAI.dot(a, a))
        mag_b = math.sqrt(UntoldAI.dot(b, b))
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot / (mag_a * mag_b)

    # ── Simple classifier ─────────────────────────────────────
    @staticmethod
    def classify(text, labels):
        """
        Zero-shot classify text into labels using keyword overlap.
        labels: list of label strings
        Returns: {"label": best_label, "scores": {label: score}}
        """
        tokens = set(UntoldAI.tokenize(text))
        scores = {}
        for label in labels:
            label_tokens = set(UntoldAI.tokenize(label))
            scores[label] = len(tokens & label_tokens)
        best = max(scores, key=scores.get)
        return {"label": best, "scores": scores}

    # ── API caller (OpenAI-compatible) ────────────────────────
    @staticmethod
    def chat(prompt, api_key, model="gpt-3.5-turbo", system="You are a helpful assistant."):
        """
        Call any OpenAI-compatible chat API.
        Works with OpenAI, Groq, Together, Ollama, etc.
        """
        import urllib.request
        payload = json.dumps({
            "model":    model,
            "messages": [
                {"role": "system",  "content": system},
                {"role": "user",    "content": prompt}
            ]
        }).encode()
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data    = payload,
            headers = {
                "Content-Type":  "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            method = "POST"
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
            return data["choices"][0]["message"]["content"]

    @staticmethod
    def chat_ollama(prompt, model="llama3", host="http://localhost:11434"):
        """Call a local Ollama model."""
        import urllib.request
        payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
        req = urllib.request.Request(
            f"{host}/api/generate",
            data    = payload,
            headers = {"Content-Type": "application/json"},
            method  = "POST"
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode())
            return data.get("response", "")

    # ── Dataset helpers ───────────────────────────────────────
    @staticmethod
    def load_csv(path):
        import csv
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    @staticmethod
    def save_csv(path, data):
        import csv
        if not data:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
