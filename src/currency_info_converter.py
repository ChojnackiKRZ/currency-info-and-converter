# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 00:06:35 2023

@author: krzys
"""

# Potrzebujemy przeliczyć trochę waluty, czasy niepewne,
# warto mieć na uwadze swoją ulubioną walutę.
# Napisz klasę, która będzie zawierać dwie metody:

#       przeliczenie wybranej waluty z tabeli A na złotówki  <- dane wejściowe: kod waluty, ilość waluty
#       wskazanie aktualnego kursu z tabeli A <- dane wjećiowe: kod waluty

# Klasa w celu przeliczenia waluty powinna skorzystać z aktualnych kursów z Narodowego Banku Polskiego
# dokumentację API dla NBP znajdziesz pod adresem http://api.nbp.pl/

# Gdy skończysz prześlij mi swoje zadanie w postaci linku do swojego GitHuba, innych linków nie przyjmuję :)
# Na rozwiązanie czekam do końca dnia do niedzieli 22.01.2023

import requests
import pandas as pd


class CurrencyInfo:
    def __init__(self, base_currency: str, currency_qty: float):
        self.base_currency = base_currency
        self.currency_qty = currency_qty

    def calculate_to_pln(self) -> pd.DataFrame:
        """
        Function to calculate PLN amount accordingly to your currency of choice.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """
        req = requests.get(
            f"https://api.nbp.pl/api/exchangerates/rates/a/{self.base_currency}?format=json"
        )
        df = pd.DataFrame(req.json()["rates"])
        df = df.drop(columns=["no"], axis=1)
        df["INPUT_CURRENCY"] = pd.DataFrame([req.json()["code"]])
        df["RESULT_AMOUNT"] = pd.DataFrame(df["mid"] * self.currency_qty)
        df["RESULT_CURRENCY"] = pd.DataFrame(["PLN"])
        df.columns = df.columns.str.upper()
        df.columns = [
            "MEASURE_DATE",
            "BASE_AMOUNT",
            "BASE_CURRENCY",
            "RESULT_AMOUNT",
            "RESULT_CURRENCY",
        ]
        return df

    def currency_price(self) -> float:
        """
        Function to reutrn price of your currency of choice. Price is shown in
        PLN.

        Returns
        -------
        float
            DESCRIPTION.

        """
        req = requests.get(
            f"https://api.nbp.pl/api/exchangerates/rates/a/{self.base_currency}?format=json"
        )
        df_currency_price = req.json()["rates"][0]["mid"]
        return float(df_currency_price)
