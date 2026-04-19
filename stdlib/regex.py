"""
untold.regex — Regular expressions module
"""
import re


class UntoldRegex:
    """Regular expression utilities"""

    @staticmethod
    def match(pattern, text):
        """Check if pattern matches text"""
        return re.match(pattern, text) is not None

    @staticmethod
    def search(pattern, text):
        """Search for pattern in text"""
        match = re.search(pattern, text)
        return match.group() if match else None

    @staticmethod
    def find_all(pattern, text):
        """Find all matches"""
        return re.findall(pattern, text)

    @staticmethod
    def replace(pattern, replacement, text):
        """Replace pattern with replacement"""
        return re.sub(pattern, replacement, text)

    @staticmethod
    def split(pattern, text):
        """Split text by pattern"""
        return re.split(pattern, text)

    @staticmethod
    def groups(pattern, text):
        """Get capture groups"""
        match = re.search(pattern, text)
        return match.groups() if match else None

    @staticmethod
    def valid(pattern):
        """Check if pattern is valid regex"""
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False