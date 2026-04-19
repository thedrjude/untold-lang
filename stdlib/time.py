"""
untold.time — Date & time module
"""
from datetime import datetime, timedelta


class UntoldTime:
    """Date and time utilities"""

    @staticmethod
    def now():
        """Get current datetime"""
        return datetime.now()

    @staticmethod
    def today():
        """Get today's date"""
        return datetime.now().date()

    @staticmethod
    def timestamp():
        """Get current Unix timestamp"""
        return datetime.now().timestamp()

    @staticmethod
    def format(dt=None, fmt="%Y-%m-%d %H:%M:%S"):
        """Format datetime"""
        if dt is None:
            dt = datetime.now()
        return dt.strftime(fmt)

    @staticmethod
    def parse(text, fmt="%Y-%m-%d %H:%M:%S"):
        """Parse datetime string"""
        return datetime.strptime(text, fmt)

    @staticmethod
    def add_days(dt, days):
        """Add days to datetime"""
        return dt + timedelta(days=days)

    @staticmethod
    def add_hours(dt, hours):
        """Add hours to datetime"""
        return dt + timedelta(hours=hours)

    @staticmethod
    def diff_days(dt1, dt2):
        """Get difference in days"""
        return (dt1 - dt2).days

    @staticmethod
    def iso_format(dt=None):
        """Get ISO format"""
        if dt is None:
            dt = datetime.now()
        return dt.isoformat()