from app.api.core.process import ApiProcess


class ApiHandler:
    @staticmethod
    def list_all_handler(offset: int, limit: int) -> dict:
        return ApiProcess.list_all_process(offset=offset, limit=limit)

    @staticmethod
    def data_by_id_handler(id: str) -> dict:
        return ApiProcess.data_by_id_process(id=id)

    @staticmethod
    def data_by_colony_handler(colony: str, offset: int, limit: int) -> dict:
        return ApiProcess.data_by_colony_process(colony=colony, offset=offset, limit=limit)

    @staticmethod
    def wifi_ordered_by_proximity_handler(latitude: float, longitude: float, offset: int, limit: int) -> list:
        return ApiProcess.wifi_ordered_by_proximity_process(latitude=latitude, longitude=longitude, offset=offset, limit=limit)
