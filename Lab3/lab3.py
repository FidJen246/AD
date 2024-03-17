from cleaner import clean, index_replace
from spyre import server


class SlidersApp(server.App):
    title = "NOAA data vizualization"

    inputs = [{"type": "dropdown",
                "label": "Оберіть тип індексу для графіку",
                "options": [{"label": "VCI", "value": "VCI"},
                            {"label": "TCI", "value": "TCI"},
                            {"label": "VHI", "value": "VHI"},],
                "key": "data_type",
                "action_id": "update_data"},
            {"type": "dropdown",
                "label": "Оберіть область України:",
                "options": [{"label": "Вінницька", "value": "1"},
                            {"label": "Волинська", "value": "2"},
                            {"label": "Дніпропетровська", "value": "3"},
                            {"label": "Донецька", "value": "4"},
                            {"label": "Житомирська", "value": "5"},
                            {"label": "Закарпатська", "value": "6"},
                            {"label": "Запорізька", "value": "7"},
                            {"label": "Івано-Франківська", "value": "8"},
                            {"label": "Київська", "value": "9"},
                            {"label": "Кіровоградська", "value": "10"},
                            {"label": "Луганська", "value": "11"},
                            {"label": "Львівська", "value": "12"},
                            {"label": "Миколаївська", "value": "13"},
                            {"label": "Одеська", "value": "14"},
                            {"label": "Полтавська", "value": "15"},
                            {"label": "Рівенська", "value": "16"},
                            {"label": "Сумська", "value": "17"},
                            {"label": "Тернопільська", "value": "18"},
                            {"label": "Харківська", "value": "19"},
                            {"label": "Херсонська", "value": "20"},
                            {"label": "Хмельницька", "value": "21"},
                            {"label": "Черкаська", "value": "22"},
                            {"label": "Чернівецька", "value": "23"},
                            {"label": "Чернігівська", "value": "24"},
                            {"label": "Крим", "value": "25"}],
                "key": "province",
                "action_id": "update_data"},
            {"type": "text",
                "label": "Оберіть інтервал тижнів:",
                "key": "weeks",
                "value": "10-30",
                "action_id": "update_data"},
            {"type": "slider",
                "label": "Оберіть рік:",
                "min": 1981,
                "max": 2024,
                "key": "year",
                "action_id": "update_data"}]
    controls = [{"type": "hidden", "id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{"type": "plot", 
                "id": "plot", 
                "control_id": 
                "update_data", 
                "tab": "Plot"},
            {"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": True}]


    def getData(self, params):
        province = params["province"]
        weeks = params["weeks"]
        year = params["year"]
        df = index_replace(clean("./DataCSV"))
        df = df[df["ID"] == int(province)]
        start_week, end_week = map(int, weeks.split("-"))
        df = df[(df["week"] >= start_week) & (df["week"] <= end_week) & (df["year"] == int(year))]
        return df[["year", "week", "SMN", "SMT", "VCI", "TCI", "VHI"]]


    def getPlot(self, params):
        df = self.getData(params)
        data_type = params["data_type"]
        plt_obj = df.plot(x="week", y=data_type)
        return plt_obj.get_figure()


if __name__ == "__main__":
    app = SlidersApp()
    app.launch()
