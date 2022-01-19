from glob import glob
import pandas as pd
import toml
from pathlib import Path

file_config = Path(__file__).resolve().parent
settings = toml.load(file_config / "csv_test_settings.toml")

input_path = Path(settings["file_config"]["file_paths"]["input_file_path"])
output_path = Path(settings["file_config"]["file_paths"]["output_file_path"])
sheet_name = settings["file_config"]["files"]["sheet_name"]
file_type = settings["file_config"]["files"]["file_type"]
column_validation = set(settings["file_config"]["column_validation"]["headers"])
index_header = settings["file_config"]["index"]["header_location"]
index_skip_rows = settings["file_config"]["index"]["skip_rows"]


class Amalgamater:
    def __init__(self, input_path: str, output_path: str, sheet_name: str, file_type: str, column_validation: str, index_header: int, index_skip_rows= int):
        """

        :type input_path: object
        """
        self.path = glob(str(input_path / file_type))
        self.input_path = input_path
        self.output_path = output_path
        self.sheet_name = sheet_name
        self.file_type = file_type
        self.column_validation = column_validation
        self.index_header = index_header
        self.index_skip_rows = index_skip_rows

    def validate(self):
        """
        validating headers
        """
        for file in self.path:
            df = pd.read_excel(file, sheet_name=self.sheet_name, header=[self.index_header], skiprows=[self.index_skip_rows])
            unique_column = set(df.columns.tolist())
            if unique_column != self.column_validation:
                print("error in " + str(file) + " check before proceeding. Column " + str(
                    self.column_validation - unique_column) + " is missing.")
                return False
        return True

    def amalgamate(self) -> pd.DataFrame:
        """
        append data to csv
        """
        data = []
        for file in self.path:
            df = pd.read_excel(file, sheet_name=self.sheet_name, header=[self.index_header], skiprows=[self.index_skip_rows], names=self.column_validation, axis=0)
            df = df.dropna(how='all')
            data.append(df)
        return data

    def concat_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """concatenate data
        :rtype: object
        """
        return pd.concat(data)

    def convert_to_csv(self, data: pd.DataFrame) -> pd.DataFrame:
        """convert to csv"""

        return data.to_csv(self.output_path)


if __name__ != "__main__":
    if Amalgamater.validate(input_path) is False:
        print("see above error")
    else:
        data = Amalgamater.amalgamate(input_path)
        data_final = Amalgamater.concat_data(data)
        data_final_csv = Amalgamater.convert_to_csv(data_final)
        print(data_final_csv)