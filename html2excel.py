#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import pandas as pd


def HTML_parser(filepath):
    # 临时表
    df = pd.DataFrame()

    # 打开 html 文件
    with open(filepath) as fp:
        soup = BeautifulSoup(fp, "html5lib")

    # 解析 html 文档树
    div = soup.find_all("div", style = "clear: left")
    for i in div:
        title = i.h3.string
        table = i.find_all("div", class_ = "case-stage")

        Set_up = None
        Actions = None
        Expected_Results = None
        Breakdown = None
        for j in table:
            h4 = j.h4.string
            p = j.p.getText() if j.p is not None else ""
            if h4 == "Set up":
                Set_up = p.split("\n")
            elif h4 == "Actions":
                Actions = p.split("\n")
            elif h4 == "Expected Results":
                Expected_Results = p.split("\n")
            elif h4 == "Breakdown":
                Breakdown = p.split("\n")
        Title = []
        Title.append(title)
        L_max = max(len(Title), len(Set_up), len(Actions), len(Expected_Results), len(Breakdown))
        if len(Title) < L_max:
            Title += [""] * (L_max - len(Title))
        if len(Set_up) < L_max:
            Set_up += [""] * (L_max - len(Set_up))
        if len(Actions) < L_max:
            Actions += [""] * (L_max - len(Actions))
        if len(Expected_Results) < L_max:
            Expected_Results += [""] * (L_max - len(Expected_Results))
        if len(Breakdown) < L_max:
            Breakdown += [""] * (L_max - len(Breakdown))

        # 将数据转换为 pd.DataFrame
        tab = {
            "Title": Title,
            "Set up": Set_up,
            "Actions": Actions,
            "Expected Results": Expected_Results,
            "Breakdown": Breakdown
        }
        df_in = pd.DataFrame(tab)
        print(df_in)
        df = pd.concat([df, df_in], axis = 0)

        # 将表保存在 excel 文件中
        df.to_excel("./output/html2excel.xlsx", index = False, index_label = None)


def main():
    filepath = "./input/Printable_copy_for_test_cases.html"
    HTML_parser(filepath)

if __name__ == "__main__":
    main()

