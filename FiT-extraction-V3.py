import pandas as pd
import os
import glob

path = r"//customer/userdat$/crawley/Tsang1H/FiT/"


def convert_excel_to_csv(path):
    """
    Converts excel spreadsheet in file path to csv
    """
    for file in glob.glob(os.path.join(path, '*.xlsx')):
        read_file = pd.read_excel(file, engine='openpyxl')
        file_name = os.path.splitext(os.path.basename(file))[0]
        read_file.to_csv(os.path.join(path, file_name + '.csv'))


def clean_installation_reports(path):
    """
    cleans installation reports and appends results into csv
    """
    report_final = pd.DataFrame(columns=["Technology", "Installed capacity", "Tariff code"])
    for file in glob.glob(os.path.join(path, 'Installation*.csv')):
        report = pd.read_csv(file, skiprows=4, index_col=None, low_memory=False)
        report = report.filter(items=["Technology", "Installed capacity", "TariffCode"])
        report.columns = (["Technology", "Installed capacity", "Tariff code"])
        report_final = report_final.append(report)
    return report_final


def clean_tariff_reports(path):
    """
    cleans tariff report data and appends results into csv
    """
    for file in glob.glob(os.path.join(path, '*Tariff Codes.csv')):
        tariff_summary = pd.read_csv(file, index_col=None, low_memory=False)
        tariff_summary = tariff_summary.filter(items=["Tariff code", "Tariff"])
        tariff_summary_report = pd.DataFrame(tariff_summary)
        return tariff_summary_report

#%%
def map_and_create_new_column_data(tariff_summary_report, report_final, path):
    """
    merges dataframes by tariff code
    """
    final_fit_data = pd.merge(tariff_summary_report, report_final, on=["Tariff code"]) #specify argument inner or outer
    final_fit_data["WA"] = final_fit_data["Installed capacity"] * final_fit_data["Tariff"]
    final_fit_data = final_fit_data.groupby(final_fit_data["Technology"]).sum() #dropNAN
    final_fit_data["WA Tariff"] = final_fit_data["WA"] / final_fit_data["Installed capacity"]
    final_fit_data = final_fit_data[["Installed capacity", "WA Tariff"]]
    return final_fit_data.to_csv(os.path.join(path, 'final_summary_data.csv'))
#%%

if __name__ == '__main__':
    convert_excel_to_csv(path)
    report_final = clean_installation_reports(path)
    tariff_summary_report = clean_tariff_reports(path)
    map_and_create_new_column_data(tariff_summary_report, report_final, path)



