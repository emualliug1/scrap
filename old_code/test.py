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
    return Liste_pages






# récupération des liens des entreprises
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



# récupération des infos entreprises
def get_entreprise_nom(url):
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

    return nono



def get_entreprise_ville(url):
    vivi=[]
    reque= requests.get(url)
    soup= BeautifulSoup(reque.content ,"html.parser")
    
    entreprises=soup.find_all("tr")

    #récupération des villes des entreprises
    for _ville_ in entreprises:
        ville = _ville_.find('td', class_="nowrap not-mobile")
        if ville is not None:
            ville_ = ville.text
            vivi.append(ville_)

    return vivi


# recupere chaque url d'entreprise
#récupere chaque url d'entreprise
def get_all_link_entreprise():
    Liste_pages_entreprise=[]
    vivi=get_all_pages()
    nono=get_all_pages()
    liens = recup_lien()
    nom_=[]
    vivi_=[]

    for lien in liens:
        i = f"https://rubypayeur.com/{lien}"
        Liste_pages_entreprise.append(i)

    for page in nono:
        i = get_entreprise_nom(page)
        nom_.append(i)

    for page in vivi:
        i = get_entreprise_ville(page)
        vivi_.append(i)


    with open('Liste_lien_entreprise.txt', 'a', encoding='utf-8') as f:
        n=0
        # écrire du texte dans le fichier
        while n<=len(vivi):
            f.write(f"{Liste_pages_entreprise[n]} / {nom_[n]} / {vivi_[n]} \n\n")
            n+=1




                
if __name__ == "__main__":
    get_all_link_entreprise()

