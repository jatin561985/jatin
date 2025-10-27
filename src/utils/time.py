from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")

def get_ist_now() -> datetime:
    """
    Returns the current time in the IST timezone.
    """
    return datetime.now(IST)

if __name__ == "__main__":
    now_ist = get_ist_now()
    print(f"Current IST time: {now_ist}")
    print(f"Timezone: {now_ist.tzinfo}")
