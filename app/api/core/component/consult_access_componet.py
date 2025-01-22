from app.api.core.query_set import (
    get_all_wifi_records, search_wifi_records_like, get_wifi_record_by_id, get_all_wifi_proximity)


class ConsultAccessComponent:
    @staticmethod
    def all_info_run(offset: int, limit: int) -> list:
        records = get_all_wifi_records(offset, limit)      
        return records

    @staticmethod
    def by_colony_run(colony: str, offset, limit) -> list:
        records = search_wifi_records_like(colony, offset, limit)       
        return records

    @staticmethod
    def by_id_run(id: str) -> dict:
        record = get_wifi_record_by_id(id)
        return record

    @staticmethod
    def proximity_run(latitude: float, longitude: float, offset: int, limit: int) -> list:
        record = get_all_wifi_proximity(latitude, longitude, offset, limit)
        return record
