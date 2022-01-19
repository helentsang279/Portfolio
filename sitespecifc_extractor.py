import pandas as pd


class Site_Specific_Extractor:
    """Class to extract site specific demand and generation tables
    """

    def __init__(self, all_df: pd.DataFrame, index_table_dict: dict, demand_content_position_from_top: int,
                 demand_content_position_from_bottom: int, demand_header_position_from_top: int,
                 generation_header_position_from_top: int, generation_content_position_from_top: int):
        self.df = all_df
        self.index_table_dict = index_table_dict
        self.demand_index_top = demand_content_position_from_top
        self.demand_index_bottom = demand_content_position_from_bottom
        self.demand_header_index = demand_header_position_from_top
        self.generation_header_index = generation_header_position_from_top
        self.generation_index_top = generation_content_position_from_top

    def site_specific_demand_table_extractor(self) -> pd.DataFrame:
        """Function finds demand table via indexation of table from the header of the demand table and
        extracts the table.
        :return: demand dataframe
        """
        # Finding the header of the table, it is just one below the 'Demand Table Index' row.
        new_header = self.df.loc[(self.index_table_dict["Demand Table Index"] + self.demand_header_index)]

        # Isolating only the information related to generic LLFs
        sspec_df_d = self.df.loc[
                     (self.index_table_dict["Demand Table Index"] + self.demand_index_top):(
                             self.index_table_dict["Generation Table Index"] - self.demand_index_bottom)]

        # Redefining new column according to the desired header
        sspec_df_d.columns = new_header

        # Import/Export indicator
        sspec_df_d['Import/Export'] = "Import"

        return sspec_df_d.reset_index().drop('index', 1)

    def site_specific_generation_table_extractor(self) -> pd.DataFrame:
        """Function finds the generation table via indexation of table from the header of the generation table and
        extracts the table. The function also detects another table call 'CSV site specific LLFs' and truncates
        all data passed this point to return only the generation table. Not all charging statements have this table
        but this will bbe detected by the if statement.
        :return: generation dataframe
        """
        # Finding the header of the table, it is just one below the 'Generation Table Index' row.
        new_header = self.df.loc[(self.index_table_dict["Generation Table Index"] + self.generation_header_index)]

        # Isolating only the information related to generation LLFs
        sspec_df_gen = self.df.loc[
                       (self.index_table_dict["Generation Table Index"]) + self.generation_index_top:
                       ]

        # Redefining new column according to the desired header
        sspec_df_gen.columns = new_header

        # Import/Export indicator
        sspec_df_gen['Import/Export'] = "Export"

        # Drop everything from CVA table onwards
        last_row = sspec_df_gen['Site'].eq('CVA site specific LLFs')
        max_last_row = last_row.idxmax()
        if last_row.any():
            sspec_df_gen = sspec_df_gen.loc[:max_last_row - 1]
        return sspec_df_gen.reset_index().drop('index', 1)

    def join_frames(self, sspec_df_gen, sspec_df_d) -> pd.DataFrame:
        """combines site specific dataframes by column headers

        param sspec_df_gen: generation dataframe
        param sspec_df_d: demand dataframe
        return: combined dataframe
        """
        sspec_df_final = pd.concat([sspec_df_gen, sspec_df_d])
        return sspec_df_final
