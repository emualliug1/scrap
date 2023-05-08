# -*- coding:Utf8 -*-
#############################################
# Programme Python type
#############################################
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from scrap import URL, URL_COMPANY, CSV_FILE, MAX_THREADS
import requests
import time
import csv
#############################################


class Scraper:

    def __init__(self, url: str):
        self.url = url
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.scraping_url = []

    def set_scraper(self, url: str):
        """
        Mise en place du scraper
        :param url : Url ou l'on veut scraper des informations
        """
        self.url = url
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

    def get_max_pagination(self) -> int:
        """
        Recuperation des urls de pagination
        :return: Le nombre maximum de pages de pagination du site
        """
        pagination_last = self.soup.find('li', class_='last').find('a')
        pagination_max = int(pagination_last['href'].split('/')[-1])
        return pagination_max

    def create_pagination_links(self) -> list:
        """
        Creation des liens de pagination
        :return: La totalité des liens de pagination des entreprises
        """
        pagination_links = []
        for pagination in range(1, self.get_max_pagination()):
            pagination_links.append(URL + "/page/" + str(pagination))
        return pagination_links

    def get_company_links(self) -> list:
        """
        Recuperation des urls d'entreprise
        :return: La totalité des liens sur une page de pagination
        """
        company_links = []
        directory_table = self.soup.find("table", class_="directory-table")
        for row in directory_table.findAll("tr"):
            link = row.find("a")
            if link is not None:
                href = link.get("href")
                company_links.append(URL_COMPANY + href)
        return company_links

    def get_all_company_links(self) -> list:
        """
        Recuperation de la totalité des liens d'entreprises
        :return: La totalité des liens des entreprises
        """
        self.scraping_url = [entreprise_link for pagination_link in self.create_pagination_links()
                             for entreprise_link in self.get_company_links()]
        return self.scraping_url

    def get_company_info(self, url: str) -> list:
        """
        Recuperation des informations d'une entreprise
        :param url: Url ou l'on veut scraper des informations
        :return: Toutes les informations scraper pour une entreprise
        """
        self.set_scraper(url)
        try:
            denomination = self.soup.find('td', text='Dénomination').find_next_sibling('td').text.strip()
        except AttributeError:
            denomination = ''

        try:
            status_insee = self.soup.find('td', text='Statut INSEE').find_next_sibling('td').text
        except AttributeError:
            status_insee = ''
        try:
            status_rcs = self.soup.find('td', text='Statut RCS').find_next_sibling('td').text
        except AttributeError:
            status_rcs = ''

        try:
            siren = self.soup.find('td', text='SIREN').find_next_sibling('td').text
        except AttributeError:
            siren = ''

        try:
            siret = self.soup.find('td', text='SIRET (siège)').find_next_sibling('td').text
        except AttributeError:
            siret = ''

        try:
            numero_rcs = self.soup.find('td', text='Numéro RCS').find_next_sibling('td').text
        except AttributeError:
            numero_rcs = ''

        try:
            adresse = self.soup.find('td', text='Adresse').find_next('span').text
        except AttributeError:
            adresse = ''

        try:
            capital_social = self.soup.find('td', text='Capital social').find_next_sibling('td').text
        except AttributeError:
            capital_social = ''

        try:
            forme_juridique = self.soup.find('td', text='Forme juridique').find_next_sibling('td').text
        except AttributeError:
            forme_juridique = ''

        try:
            greffe = self.soup.find('td', text='Greffe').find_next_sibling('td').text
        except AttributeError:
            greffe = ''

        try:
            secteur_activite = self.soup.find('td', text="Secteur d'activité").find_next_sibling('td').text
        except AttributeError:
            secteur_activite = ''

        try:
            code_nap = self.soup.find('td', text='Code NAF ou APE').find_next_sibling('td').text
        except AttributeError:
            code_nap = ''

        try:
            maj = self.soup.find('td', text='Dernière mise à jour de la fiche').find_next_sibling('td').text
        except AttributeError:
            maj = ''

        company_data = [{
            'Url': url,
            'Dénomination': denomination,
            'Status INSEE': status_insee,
            'Status RCS': status_rcs,
            'Siren': siren,
            'Siret': siret,
            'Numero RCS': numero_rcs,
            'Adresse': adresse,
            'Capital': capital_social,
            'Forme juridique': forme_juridique,
            'Greffe': greffe,
            "Secteur d'activité": secteur_activite,
            'Code NAF ou APE': code_nap,
            'Dernière mise à jour de la fiche': maj,
        }]

        return company_data

    @staticmethod
    def write_to_csv(data_list: list):
        """
        Ecrire les informations des entreprises dans un fichier csv"
        :param data_list: La liste que l'on veut ecrire dans le fichier csv
        """
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data_list[0].keys())
            writer.writeheader()
            for data in data_list:
                writer.writerow(data)

    def run_async(self):
        """
        Lancement du programme en asynchrone
        """
        start = time.time()
        self.get_all_company_links()
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = []
            for company_link in self.scraping_url:
                future = executor.submit(self.get_company_info, company_link)
                futures.append(future)
            results = []
            for data in tqdm(as_completed(futures), total=len(futures)):
                try:
                    company_data = data.result()
                except Exception as exc:
                    print(f"oups: {exc}")
                else:
                    results.extend(company_data)

        Scraper.write_to_csv(results)
        end = time.time()
        print(f"{end - start} seconds pour scraper {len(self.scraping_url)} entreprise.")
