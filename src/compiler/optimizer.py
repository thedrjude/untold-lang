import re


class Optimizer:
    """
    Basic source optimizer for Untold Lang.
    Strips comments, blank lines, normalizes whitespace.
    """

    def __init__(self, source):
        self.source = source

    def optimize(self, level=1):
        if level == 0:
            return self.source
        source = self._strip_comments(self.source)
        source = self._strip_blank_lines(source)
        if level >= 2:
            source = self._normalize_whitespace(source)
        return source

    def _strip_comments(self, source):
        # Remove single-line comments
        source = re.sub(r"//.*$", "", source, flags=re.MULTILINE)
        # Remove multi-line comments
        source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
        return source

    def _strip_blank_lines(self, source):
        lines = [l for l in source.splitlines() if l.strip()]
        return "\n".join(lines)

    def _normalize_whitespace(self, source):
        lines = []
        for line in source.splitlines():
            lines.append(line.strip())
        return "\n".join(lines)

    def stats(self):
        original  = len(self.source)
        optimized = len(self.optimize())
        reduction = ((original - optimized) / original * 100) if original else 0
        return {
            "original_chars":  original,
            "optimized_chars": optimized,
            "reduction_pct":   round(reduction, 1)
        }
