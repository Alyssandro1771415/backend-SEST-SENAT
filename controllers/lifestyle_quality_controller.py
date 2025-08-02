import pandas as pd


class LifestyleQualityController:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        print(f"\033[95mIniciando o controller de relatório de saúde\033[m")
        self.dataFrame = pd.read_csv("./db/Relatorio_de_saude_2025.csv", sep="|", encoding="utf-8")
        print(f"\033[95mDataFrame carregado com {self.dataFrame.shape[0]} linhas e {self.dataFrame.shape[1]} colunas\033[m")
        LifestyleQualityController._initialized = True

    def get_lifestyle_quality(self, regiao, filters):
        """
        Method to get the lifestyle quality data based on region and filters.
        """
        if regiao != "all":
            df = self.dataFrame[self.dataFrame['regiao'] == regiao]
        else:
            df = self.dataFrame

        if filters:
            for filter in filters:
                for key, value in filter.items():
                    if key in df.columns:
                        df = df[df[key] == value]

        response_life_style = self.calc_average(df, 'indice_estilo_vida')
        response_hearth_avaliation = self.calc_average(df, 'indice_avaliacao_saude')

        response = {"indice_estilo_de_vida": response_life_style,
                    "indice_avaliacao_de_saude": response_hearth_avaliation}
        
        return response

    def calc_average(self, df, column):
        """
        Method to calculate the average of a given column in the DataFrame.
        """
        total_sum = sum(df[column])
        total_registers = len(df)

        if total_registers == 0:
            return 0
        else:
            average = float(round(total_sum/total_registers, 2))

        return average
