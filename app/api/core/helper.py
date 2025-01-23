

from app.api.core.models import WifiRecord
import unicodedata


def build_combined_records(wifi_records: WifiRecord):
    ''' Build a list of dictionaries by combining WifiRecord and Colony data '''
    combined_records = []
    for wifi_record, colony in wifi_records:
        record_dict = wifi_record.as_dict()
        colony_dict = colony.as_dict()
        record_dict.update(colony_dict)
        combined_records.append(record_dict)
    return combined_records


def normalize_text(text):
    if isinstance(text, str):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text
