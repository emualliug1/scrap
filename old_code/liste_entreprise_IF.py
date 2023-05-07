import requests
from bs4 import BeautifulSoup


#récupération de toute les pages listant les entreprises
def get_all_pages():
    number=2
    Liste_pages=["https://rubypayeur.com/annuaire/creations/regions/ile-de-france"]

    for i in range(number,160):
        i=f"https://rubypayeur.com/annuaire/creations/regions/ile-de-france/page/{number}"
        number+=1
        Liste_pages.append(i)
    print(Liste_pages)
    return Liste_pages



#récupération des liens des entreprises
def recup_lien():
    pages = get_all_pages()
    liste = []
    for page in pages:
        reque = requests.get(page)
        soup = BeautifulSoup(reque.content ,"html.parser")
        entreprises = soup.find_all("tr")
        for link in entreprises:
            balise_lien = link.find("a")
            if balise_lien is not None:
                liens = balise_lien.get("href")
                liste.append(liens)
    return liste






#recupere chaque url d'entreprise
def get_all_link_entreprise():
    Liste_pages_entreprise=[]
    liens = recup_lien()

    for lien in liens:
        i = f"https://rubypayeur.com/{lien}"
        Liste_pages_entreprise.append(i)

    with open('Liste_lien_entreprise.txt', 'a', encoding='utf-8') as f:
        i=0
    # écrire du texte dans le fichier
        while i<=len(Liste_pages_entreprise):
            f.write(f"<a href='{Liste_pages_entreprise[i-1]}'></a>\n\n")
            i+=1













#récupération des infos entreprises
def get_entreprise(url):
    vivi=[]
    nono=[]
    reque= requests.get(url)
    soup= BeautifulSoup(reque.content ,"html.parser")
    
    entreprises=soup.find_all("tr")
    
    #récupération des noms des entreprises
    for entre in entreprises:
        nom = entre.find('a')
        if nom is not None:
            nom_text = nom.text
            nono.append(nom_text)

    #récupération des villes des entreprises
    for _ville_ in entreprises:
        ville = _ville_.find('td', class_="nowrap not-mobile")
        if ville is not None:
            ville_ = ville.text
            vivi.append(ville_)

    with open('Liste_entreprise_info.txt', 'a', encoding='utf-8') as f:
        i=0
    # écrire du texte dans le fichier
        while i<=len(vivi):
            f.write(f"{vivi[i]} / ")
            f.write(f"{nono[i]}\n\n")
            i+=1







#recupere chaque infos que chaque page
def get_all_pages_entreprise():
    pages= get_all_pages()
    for page in pages:
        get_entreprise(page)






                
if __name__ == "__main__":
    get_all_link_entreprise()
    get_all_pages_entreprise()




