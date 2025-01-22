import requests
import pandas as pd
from io import StringIO
from app.api.core.helper import normalize_text
from app.core.exceptions import ExtractionErrorException, LoadErrorException, TransformationErrorException
from config.db.factory_db import FactoryDB
import config.enviroment as env
from app.core.component.base_component import BaseComponent


class EtlDataWifi(BaseComponent):
    """ETL in charge of extracting, transforming, and loading information."""

    def __init__(self, base_date: str = None) -> None:
        self.__base_date = base_date
        self.run()

    def extraction(self) -> None:
        """Extract data from the source."""
        try:
            url = env.URL_BASE.format(BASE_DATE=self.__base_date)
            response = requests.get(url)
            response.raise_for_status()
            csv_content = StringIO(response.text)
            self.__data_frame = pd.read_csv(csv_content, encoding='latin1')
        except Exception as e:
            raise ExtractionErrorException(f"Extraction failed: {str(e)}")

    def transformation(self) -> None:
        """Transform the extracted data."""
        try:
            # Initialize colonies
            self.__colonies = self.set_colonies()

            # Clean and transform latitude and longitude
            self.__data_frame['latitud'] = (
                self.__data_frame['latitud'].astype(str)
                .apply(self.clean_coordinate)
                .apply(self.transform_coordinate)
            )
            self.__data_frame['longitud'] = (
                self.__data_frame['longitud'].astype(str)
                .apply(self.clean_coordinate)
                .apply(self.transform_coordinate)
            )

            # Convert coordinates to numeric and drop invalid rows
            self.__data_frame['latitud'] = pd.to_numeric(self.__data_frame['latitud'], errors='coerce')
            self.__data_frame['longitud'] = pd.to_numeric(self.__data_frame['longitud'], errors='coerce')
            self.__data_frame.dropna(subset=['latitud', 'longitud'], inplace=True)

            # Merge with colonies and format the final DataFrame
            self.__data_frame = self.__data_frame.merge(
                self.__colonies[['id', 'colonia', 'alcaldia']],
                on=['colonia', 'alcaldia'],
                how='left'
            )
            self.__data_frame.rename(columns={'id_y': 'id_colonia', 'id_x': 'id'}, inplace=True)
            self.__data_frame = self.__data_frame[['id', 'id_colonia', 'programa', 'fecha_instalacion', 'latitud', 'longitud']]
        except Exception as e:
            raise TransformationErrorException(f"Transformation failed: {str(e)}")

    def clean_coordinate(self, value: str) -> str:
        """Clean coordinate values."""
        return value.replace(' ', '').replace(',', '').replace('.', '')

    def transform_coordinate(self, value: str) -> str:
        """Transform coordinate into the correct format."""
        if value.startswith('-'):
            return f"{value[:3]}.{value[3:6]}{value[6:]}"
        return f"{value[:2]}.{value[3:6]}{value[6:]}"

    def set_colonies(self) -> pd.DataFrame:
        """Generate a DataFrame for unique colonies."""
        # Filter out invalid colony values
        self.__data_frame = self.__data_frame[self.__data_frame['colonia'] != '#¡REF!']
        self.__data_frame.reset_index(drop=True, inplace=True)

        # Normalize text for 'colonia' and 'alcaldia'
        self.__data_frame['colonia'] = self.__data_frame['colonia'].apply(normalize_text)
        self.__data_frame['alcaldia'] = self.__data_frame['alcaldia'].apply(normalize_text)

        # Create unique combinations and generate IDs
        colonies = (
            self.__data_frame.groupby(['colonia', 'alcaldia'])
            .size()
            .reset_index(name='count')
            .reset_index(drop=True)
        )
        colonies['id'] = colonies.index + 1
        return colonies[['id', 'colonia', 'alcaldia']]

    def load(self) -> None:
        """Load transformed data into the database."""
        try:
            database = FactoryDB.set_database()
            database.save_data(self.__data_frame, 'wifi_logs')
            database.save_data(self.__colonies, 'colonies')
            database.disconnect()
        except Exception as e:
            raise LoadErrorException(f"Load failed: {str(e)}")
