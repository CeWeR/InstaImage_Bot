from bs4 import BeautifulSoup
import requests

def parseImage(urlCheck):
    res = '-1'
    try:
        req = requests.get(urlCheck)
    except requests.exceptions.RequestException as e:
        return res

    if req.status_code == 200:
        soup = BeautifulSoup(req.content,"html.parser")

        ans = soup.find_all(property='og:image')

        if len(ans) > 0:
            tmp = ans[0]['content']
            if tmp is not None:
                res = tmp

    return res