#!/usr/bin/env python3
"""
User-generated News Feed Tool (OOP Demo)

Implements:
1. News      – text + city, publish date/time calculated automatically.
2. PrivateAd – text + expiration date, "days left" calculated automatically.
3. Event     – unique type: title + event date + optional location with rules:
   - Title normalized to Title Case
   - Tag: UPCOMING (≤7 days), PLANNED (>7 days), PAST (already happened)
   - Shows relative time like "in 5 days" or "2 days ago".

Each record is appended to a text file in a fixed formatted block.
"""

from datetime import datetime, date
from pathlib import Path
from typing import Optional, Type, Dict


# ---------- helpers ----------

def parse_date(datestr: str) -> date:
    """Parse date in YYYY-MM-DD format."""
    return datetime.strptime(datestr.strip(), "%Y-%m-%d").date()


def plural(n: int, one: str, many: str) -> str:
    """Return '1 day' / '2 days' style text."""
    return f"{n} {one if n == 1 else many}"


# ---------- base class ----------

class Post:
    """Abstract base class for feed records."""
    FILE_PATH: Path = Path("feed.txt")  # class variable: where to write

    def __init__(self, text: str) -> None:
        # private attribute with basic normalization
        self.__text = text.strip()

    @property
    def text(self) -> str:
        """Read-only access to text (encapsulation)."""
        return self.__text

    def formatted_body(self) -> str:
        """Subclasses must override this to provide formatted text."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Magic method used when converting object to string."""
        return self.formatted_body()

    @classmethod
    def set_output(cls, path: str | Path) -> None:
        """Change output file for all posts."""
        cls.FILE_PATH = Path(path)

    @staticmethod
    def now_str() -> str:
        """Current datetime in human-friendly format."""
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    def publish(self) -> Path:
        """Append this record to the feed file and return the path."""
        self.FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with self.FILE_PATH.open("a", encoding="utf-8") as f:
            f.write(str(self).rstrip() + "\n" + "-" * 40 + "\n")
        return self.FILE_PATH


# ---------- News ----------

class News(Post):
    """News: text + city; date/time calculated at publish time."""

    def __init__(self, text: str, city: str) -> None:
        super().__init__(text)
        self.city = city.strip().title()

    @classmethod
    def from_input(cls) -> "News":
        """Factory that reads all required data from user input."""
        text = input("News text: ").strip()
        city = input("City: ").strip()
        return cls(text, city)

    def formatted_body(self) -> str:
        header = "News ----------------------------"
        line1 = self.text
        line2 = f"City: {self.city} | Published: {self.now_str()}"
        return f"{header}\n{line1}\n{line2}"


# ---------- Private Ad ----------

class PrivateAd(Post):
    """Private advertisement: text + expiration date, days left calculated."""

    def __init__(self, text: str, expiration: date) -> None:
        super().__init__(text)
        self.expiration = expiration

    @classmethod
    def from_input(cls) -> "PrivateAd":
        text = input("Ad text: ").strip()
        while True:
            raw = input("Expiration date (YYYY-MM-DD): ").strip()
            try:
                exp = parse_date(raw)
                break
            except ValueError:
                print("Wrong format. Please use YYYY-MM-DD.")
        return cls(text, exp)

    def days_left(self) -> int:
        return max(0, (self.expiration - date.today()).days)

    def formatted_body(self) -> str:
        header = "Private Ad ----------------------"
        dl = self.days_left()
        status = "EXPIRED" if dl == 0 else f"{plural(dl, 'day', 'days')} left"
        return (
            f"{header}\n"
            f"{self.text}\n"
            f"Actual until: {self.expiration.isoformat()} | {status}"
        )


# ---------- Event (unique type) ----------

class Event(Post):
    """
    Unique record type: Event with title + event date + optional location.

    Special rules:
    - Title is normalized to Title Case.
    - Tag:
        * UPCOMING – event within next 7 days
        * PLANNED  – event more than 7 days in future
        * PAST     – event already happened
    - Shows relative difference: "in X days" or "X days ago".
    """

    def __init__(self, title: str, event_date: date,
                 location: Optional[str] = None) -> None:
        super().__init__(title)
        self.event_date = event_date
        self.location = (location or "").strip().title() or "N/A"

    @classmethod
    def from_input(cls) -> "Event":
        title = input("Event title: ").strip()
        loc = input("Location (optional): ").strip()
        while True:
            raw = input("Event date (YYYY-MM-DD): ").strip()
            try:
                dt = parse_date(raw)
                break
            except ValueError:
                print("Wrong format. Please use YYYY-MM-DD.")
        return cls(title, dt, loc)

    def _tag(self) -> str:
        delta = (self.event_date - date.today()).days
        if delta < 0:
            return "PAST"
        elif delta <= 7:
            return "UPCOMING"
        else:
            return "PLANNED"

    def formatted_body(self) -> str:
        header = "Event ---------------------------"
        title = self.text.title()  # enforce Title Case rule
        delta = (self.event_date - date.today()).days
        when = (
            f"in {plural(delta, 'day', 'days')}"
            if delta >= 0 else
            f"{plural(abs(delta), 'day', 'days')} ago"
        )
        tag = self._tag()
        return (
            f"{header}\n"
            f"{title}\n"
            f"Date: {self.event_date.isoformat()} ({when}) | "
            f"Tag: {tag} | Location: {self.location}"
        )


# ---------- Menu & main loop ----------

def menu() -> None:
    print("\nUser Generated News Feed")
    print("[1] Publish News")
    print("[2] Publish Private Ad")
    print("[3] Publish Event (unique)")
    print("[4] Change output file (current:", Post.FILE_PATH, ")")
    print("[0] Exit")


TYPE_MAP: Dict[str, Type[Post]] = {
    "1": News,
    "2": PrivateAd,
    "3": Event,
}


def main() -> None:
    while True:
        menu()
        choice = input("Select: ").strip()

        if choice == "0":
            print("Bye!")
            break

        elif choice == "4":
            new_path = input("Enter new output file path: ").strip()
            Post.set_output(new_path)
            print(f"Output set to: {Post.FILE_PATH}")
            continue

        cls = TYPE_MAP.get(choice)
        if not cls:
            print("Unknown option.")
            continue

        try:
            item = cls.from_input()   # classmethod factory
            path = item.publish()     # append to file
            print(f"✓ Published to {path.resolve()}")
        except KeyboardInterrupt:
            print("\nCancelled.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
