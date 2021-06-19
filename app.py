import requests
from concurrent import futures
import bs4 as BeautifulSoup
import pandas as pd



def GetScore(Game):
    titleGame=Game['Titre']
    response=requests.get(f"https://www.metacritic.com/search/game/{titleGame}/results",headers=header)
    if response.status_code==200:
        soup = BeautifulSoup.BeautifulSoup(response.text, 'html.parser')
        Allresult_wrap=soup.find_all(class_="result_wrap")
        for result_wrap in Allresult_wrap:
            if result_wrap is not None:
                score=result_wrap.find(class_="metascore_w")
                try:
                    convert=int(score.text)
                    Game['Score']=score.text
                    break
                except ValueError:
                    pass
                except Exception:
                    pass
                


header={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}
parametre={
    "action":"ghostpool_ajax",
    "ajaxnonce":"23e1f1de4c",
    "querystring":"pagename=xbox-game-pass%2Fliste-jeux-xbox-game-pass-ultimate",
    "pagenumber":0,
    "type":"blog",
    "cats":"xgp-console-actuellement, xgp-pc-actuellement, ea-access",
    "posttypes":"page",
    "orderby":"title_az",
    "perpage":500,
    "featuredimage":"enabled",
    "titleposition":"title-over-thumbnail",
    "pagenumbers":"enabled"
}
allGames=[]
response=requests.get("https://xboxsquad.fr/wp-admin/admin-ajax.php",params=parametre)
if response.status_code==200:
    soup = BeautifulSoup.BeautifulSoup(response.text, 'html.parser')
    divTitle=soup.find_all(class_="gp-")
    for div in divTitle:
        G={}
        titreJeux=div.text.replace('\n','')
        if titreJeux !='':
            G['Titre']=titreJeux
            G['Score']='0'
            allGames.append(G)


with futures.ThreadPoolExecutor(max_workers=50) as executor:
    [executor.submit(GetScore,G) for G in allGames]
    

print(allGames)
df = pd.DataFrame.from_dict(allGames)
df.sort_values(by=['Score'], inplace=True,ascending=False)
df.to_csv('GamePass_Metacritic.csv', index = False, header=True)


