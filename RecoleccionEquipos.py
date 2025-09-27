from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from selenium.webdriver.chrome.options import Options


class EquipmentCollection:
    def __init__(self):
        options = Options()
        # Modo sin interfaz gráfica

        # Opciones útiles
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('disable-blink-features=AutomationControlled')  # Evita detección
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36")

        # Configuración de Selenium con ChromeDriver
        service =  Service('chromedriver.exe')
        self.driver = webdriver.Chrome(service=service, options=options)

        self.urls_torneos = ['https://www.google.com/search?q=la+liga&oq=la+liga&gs_lcrp=EgZjaHJvbWUqBwgAEAAYjwIyBwgAEAAYjwIyDwgBEC4YQxixAxiABBiKBTIMCAIQLhgnGIAEGIoFMgwIAxAAGEMYgAQYigUyDAgEEAAYQxiABBiKBTIHCAUQLhiABDINCAYQLhjUAhixAxiABDINCAcQLhjUAhixAxiABDINCAgQLhjUAhixAxiABDIHCAkQABiPAtIBCDE0MzFqMGo3qAIIsAIB8QUgjQlHmnomSw&sourceid=chrome&ie=UTF-8#wptab=si:AMgyJEt5t4vh4BTDGNRc9eoUcUrmfcvMYzufJ68Rq3PlbQtYfPCifPjjSTG3or6l6ixS2NmNBb_uzUXj37OWVd0ltWWKyv33iF1yZy_Zu5Rk74D7goegDi6OJrX6sXJfFGfheLVFqmZZulfH1hi8lhqQnLeOsN9Rp07SxhD5ijFIuSG0ZONWcO5BbgMT0lbN3EhrKHU4Cmnh',
                             'https://www.google.com/search?q=la+liga+2&sca_esv=39d1a7f4746557b0&sxsrf=AE3TifNuavM3mJz3OlcHzQ2d_JKYVve-aQ%3A1757116804501&ei=hHm7aI-wHvOYwbkPuvjRAQ&si=AMgyJEtYqtmzTTrmPEFQA4SKez0BIlL2aEFv9YB4iAyEtV8s2x775lu127J0CcrlHhzlR8qAA7mkrHSMzuDjKRlcQiBSiGbxuNuQVNbVNLhygc_H7dPA6mTx-fjStIKy17B2SIqOOCDM&ictx=1&ved=2ahUKEwjX0OS96sKPAxVpQjABHfXvBFcQyNoBKAB6BAgSEAA#wptab=si:AMgyJEs0lkXDKp29s4e2JxzKQdkb-EYXoqe3WZJvB8oB-kjD4VYMtq8wyxDEBTdoORTeLnBaL9WJG6VPvdcMpzAnfgNSKFWmbkCskGhNAwrvVb2VS7Z5f_YxFBdWYKvk16NpjPysvFExWODzk6mXLpDtyDTpjqGxPKlj0XVq_wSKrAQmkmAIBSE0O4lrdXtpNGGhm4cIHWfk',
                             'https://www.google.com/search?q=ligue+1&sca_esv=39d1a7f4746557b0&sxsrf=AE3TifPLRZa9Chqlm4k3Nr6wkGSaEY1yKQ%3A1757116931460&ei=A3q7aPDsG8uDwbkPgPzNqQ8&gs_ssp=eJzj4tTP1TcwMcmoyDFg9GLPyUwvTVUwBAA64QWs&oq=ligue+1&gs_lp=Egxnd3Mtd2l6LXNlcnAiB2xpZ3VlIDEqAggBMgoQLhiABBgnGIoFMg0QLhiABBixAxhDGIoFMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBgUGIcCMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgUQABiABDIFEAAYgAQyBRAAGIAEMhwQLhiABBixAxhDGIoFGJcFGNwEGN4EGOAE2AEBSOAwUJwBWKwCcAN4AJABAZgBpAGgAaQBqgEDMC4xuAEByAEA-AEBmAIIoALCYMICBxAuGLADGCfCAgoQABiwAxjWBBhHwgINEAAYgAQYsAMYQxiKBcICDhAAGLADGOQCGNYE2AEBwgITEC4YgAQYsAMYQxjIAxiKBdgBAcICChAuGIAEGEMYigXCAhcQLhiABBiKBRiXBRjcBBjeBBjgBNgBAZgDAIgGAZAGE7oGBggBEAEYCZIHDTMuNC0xLjctMS4yLjGgB8gZsgcAuAcAwgcFMC41LjPIBxI&sclient=gws-wiz-serp#wptab=si:AMgyJEsv3PmLaKFqbPTQ9CSol7BvG13LDiFVNQjxDtWGc_GjI5YJ0LJQxzO5oEHS-IrjIUbh06oLTuUMusm4FjL3m9-tDR0HfqWCPe3Ume4J3B8FhlIRWDN94j-P3FwLBIAHujPtekL7yrFVTKYVG8ySSoRNQhYWWPnyWAH6XE0xbn3gGZ5ylMAvtqNZcgnUnxgDt6cqc17X',
                             'https://www.google.com/search?q=ligue+2&sca_esv=39d1a7f4746557b0&sxsrf=AE3TifPWC4Ef8oXK76BmH8qJc75SRud7Jg%3A1757116934217&ei=Bnq7aOyFDaGOwbkPn7m-kQE&ved=0ahUKEwjsoMXV6sKPAxUhRzABHZ-cLxIQ4dUDCBA&uact=5&oq=ligue+2&gs_lp=Egxnd3Mtd2l6LXNlcnAiB2xpZ3VlIDIyChAjGIAEGCcYigUyChAuGIAEGCcYigUyDRAuGIAEGLEDGEMYigUyChAAGIAEGEMYigUyChAAGIAEGBQYhwIyChAAGIAEGEMYigUyChAuGIAEGEMYigUyChAAGIAEGEMYigUyBRAAGIAEMgUQABiABEi2K1DnHViYKnACeAGQAQCYAagBoAHLCKoBAzAuN7gBA8gBAPgBAZgCCaAC8AjCAgQQIxgnwgIZEC4YgAQYQxiKBRiXBRjcBBjeBBjgBNgBAcICDRAuGIAEGLEDGBQYhwLCAhAQLhiABBixAxhDGMkDGIoFwgILEAAYgAQYkgMYigXCAgUQLhiABMICBxAuGLADGCfCAgoQABiwAxjWBBhHwgINEAAYgAQYsAMYQxiKBcICExAuGIAEGLADGEMYyAMYigXYAQGYAwCIBgGQBhS6BgYIARABGBSSBwMyLjegB7xrsgcDMC43uAfnCMIHAzItOcgHIA&sclient=gws-wiz-serp#wptab=si:AMgyJEsv3PmLaKFqbPTQ9CSol7BvG13LDiFVNQjxDtWGc_GjI5YJ0LJQxzO5oEHS-IrjIUbh06oLTuUMusm4FjL3m9-tDR0HfqWCPe3Ume4J3B8FhoA5tNac0m5Y3B8dFiIyLKoFQA7IKKn3azvDfs_zeu8Wp8yY2So9aFuGrtMthBA5_gExZ-QwhtKUkpOoDV0h66QGfOXq',
                             'https://www.google.com/search?q=premier+league&sca_esv=39d1a7f4746557b0&sxsrf=AE3TifMcXdyQGtfYfmke3zwaWD4RlX3sqw%3A1757116963816&ei=I3q7aP7NMf-cwbkPzpPHoAY&oq=premier&gs_lp=Egxnd3Mtd2l6LXNlcnAiB3ByZW1pZXIqAggAMgoQIxiABBgnGIoFMgoQLhiABBgnGIoFMg0QLhiABBixAxhDGIoFMg0QABiABBixAxgUGIcCMgoQABiABBhDGIoFMgoQABiABBhDGIoFMgoQABiABBgUGIcCMgoQABiABBhDGIoFMg0QABiABBixAxhDGIoFMggQABiABBixA0iFHVCgCliOFXACeAGQAQCYAbgBoAGmDaoBBDAuMTC4AQPIAQD4AQGYAgygAtQNwgIFEAAYgATCAgcQABiABBgKwgIIEAAYBxgKGB7CAgYQABgHGB7CAgoQLhiABBhDGIoFwgIEECMYJ8ICDRAjGIAEGCcYyQIYigXCAg4QABiABBixAxiDARiKBcICCxAAGIAEGLEDGIMBwgIOEC4YgAQYsQMYgwEYigXCAggQLhiABBixA8ICHBAuGIAEGLEDGEMYigUYlwUY3AQY3gQY4ATYAQHCAhEQLhiABBixAxjHARiOBRivAcICDhAuGIAEGLEDGMcBGK8BmAMAugYGCAEQARgUkgcEMi4xMKAH1pYBsgcEMC4xMLgHzA3CBwUwLjYuNsgHKA&sclient=gws-wiz-serp#wptab=si:AMgyJEt5t4vh4BTDGNRc9eoUcUrmfcvMYzufJ68Rq3PlbQtYfPCifPjjSTG3or6l6ixS2NmNBb_uzUXj37OWVd0ltWWKyv33iF1yZy_Zu5Rk74D7gmsi5pPSHM5ANvemOYyaPkdBxTl_-TJz-dgkPlH38qvPN006VxbKieErolRGzO9reuWm3vQ4llp5oEzWBK4fHksXS_0e',
                             'https://www.google.com/search?q=Premier+League+2+Division+One&sca_esv=39d1a7f4746557b0&sxsrf=AE3TifMerbCU6d1PqLIKJjgclEfrs4C1cQ%3A1757116994593&ei=Qnq7aKb4I4OLwbkP28GhiQc&ved=0ahUKEwimoary6sKPAxWDRTABHdtgKHEQ4dUDCBA&uact=5&oq=Premier+League+2+Division+One&gs_lp=Egxnd3Mtd2l6LXNlcnAiHVByZW1pZXIgTGVhZ3VlIDIgRGl2aXNpb24gT25lMgUQLhiABDIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIUEC4YgAQYlwUY3AQY3gQY4ATYAQFI1BJQ_QVYpxBwA3gBkAEAmAGkAaABpAGqAQMwLjG4AQPIAQD4AQL4AQGYAgSgArUBwgIKEAAYsAMY1gQYR8ICDRAAGIAEGLADGEMYigXCAg4QABiwAxjkAhjWBNgBAcICExAuGIAEGLADGEMYyAMYigXYAQGYAwCIBgGQBhK6BgYIARABGAmSBwMzLjGgB7cJsgcDMC4xuAenAcIHAzItNMgHDw&sclient=gws-wiz-serp#wptab=si:AMgyJEstvAlbidYYPsj14XSglLZot4wTOrJM2HzG0MF2pnM9oRgh869eCD71uw1Q7FJJ1C3fbeK5jIbERFnnfvH288R1NKebZG_BAX_L2y5lZ188EadUaEvAcYkk-X_xfcx8gMrbpaMwU65cakRPAt_teg5fYx6rHYCCopLV5sO742J0NXmnZZ2VWIhl2RVKC8nnVzvrx4lP',
                             'https://www.google.com/search?q=serie+a&sca_esv=39d1a7f4746557b0&sxsrf=AE3TifP_Ikwrwf6tA9FsBwLpoj14HFKJ_A%3A1757117006127&ei=Tnq7aL-_B6aCkvQP-96TsQ8&ved=0ahUKEwi_nur36sKPAxUmgYQIHXvvJPYQ4dUDCBA&uact=5&oq=serie+a&gs_lp=Egxnd3Mtd2l6LXNlcnAiB3NlcmllIGEyChAuGIAEGCcYigUyChAuGIAEGCcYigUyChAjGIAEGCcYigUyChAAGIAEGEMYigUyChAAGIAEGEMYigUyChAAGIAEGBQYhwIyChAAGIAEGEMYigUyChAAGIAEGEMYigUyChAAGIAEGEMYigUyCBAuGIAEGLEDMhcQLhiABBiKBRiXBRjcBBjeBBjgBNgBAUicGlDsBFjNGHACeAGQAQCYAcQBoAGmD6oBBDAuMTK4AQPIAQD4AQGYAg6gAt4PwgIIEAAYgAQYogTCAgUQABjvBcICBBAjGCfCAgoQLhiABBhDGIoFwgINEC4YgAQYQxjUAhiKBcICEBAjGPAFGIAEGCcYyQIYigXCAhIQIxjwBRiABBgTGCcYyQIYigXCAgsQLhiABBixAxiDAcICBRAAGIAEwgILEC4YgAQYxwEYrwHCAhkQLhiABBhDGIoFGJcFGNwEGN4EGN8E2AEBwgIHEC4YgAQYCsICDRAAGIAEGLEDGIMBGArCAhAQABiABBixAxiDARiKBRgKwgIKEAAYgAQYsQMYCsICBRAuGIAEwgINEC4YgAQYsQMYQxiKBZgDALoGBggBEAEYFJIHBjIuMTEuMaAH29MBsgcGMC4xMS4xuAfVD8IHBjAuMy4xMcgHMg&sclient=gws-wiz-serp#wptab=si:AMgyJEt5t4vh4BTDGNRc9eoUcUrmfcvMYzufJ68Rq3PlbQtYfPCifPjjSTG3or6l6ixS2NmNBb_uzUXj37OWVd0ltWWKyv33iF1yZy_Zu5Rk74D7gt5mVIS3TxC5xjsZ0vo5c1q0aDz13nThGaDavFuoS7ITRDaMhKEl-n8aMTaGX2TTNnkB3dzbQSZ2SDDktdnTxM93PBMo',
                             'https://www.google.com/search?q=serie+a+segunda+division+italia&sca_esv=39d1a7f4746557b0&sxsrf=AE3TifPrrd8vK3tuaBHgYq_hZejj_PRX7A%3A1757117023578&ei=X3q7aMKKI4-XwbkP6quC2A8&gs_ssp=eJzj4tTP1Tcwyi4sLDFg9JIvTi3KTFVIVChOTS_NS0lUSMksyyzOzM9TyCxJzMlMBABETA9V&oq=ser&gs_lp=Egxnd3Mtd2l6LXNlcnAiA3NlcioCCAEyEBAjGPAFGIAEGCcYyQIYigUyChAuGIAEGCcYigUyChAuGIAEGCcYigUyChAjGIAEGCcYigUyChAuGIAEGEMYigUyChAAGIAEGEMYigUyChAAGIAEGEMYigUyChAAGIAEGEMYigUyChAAGIAEGEMYigUyChAuGIAEGEMYigVIhBdQkgxYwxBwAHgBkAEAmAGiAaAB3wSqAQMwLjS4AQHIAQD4AQGYAgSgAvAEwgINEAAYgAQYsQMYQxiKBcICBRAAGIAEwgIEECMYJ8ICEhAjGPAFGIAEGBMYJxjJAhiKBcICCxAuGIAEGLEDGIMBmAMAkgcDMC40oAeHQbIHAzAuNLgH8ATCBwUwLjEuM8gHDg&sclient=gws-wiz-serp#wptab=si:AMgyJEsv3PmLaKFqbPTQ9CSol7BvG13LDiFVNQjxDtWGc_GjI5YJ0LJQxzO5oEHS-IrjIUbh06oLTuUMusm4FjL3m9-tDR0HfqWCPe3Ume4J3B8FhkPfxnujurHcKONjXsWPjihzZXeSONGtpUry4_J8c403QfvDdRl6yri1qFPkRqavw2FxywAf-1uepIktj_uBpU66YSPl',
                             'https://www.google.com/search?q=bundesliga&sca_esv=39d1a7f4746557b0&sxsrf=AE3TifPdr-MIkyaK7dnKQDRXaCpUnUhhEQ%3A1757117037432&ei=bXq7aIKXGsyOwbkP6ZCpsAk&gs_ssp=eJzj4tTP1TcwNjc0szRg9OJKKs1LSS3OyUxPBABGIwa8&oq=bun&gs_lp=Egxnd3Mtd2l6LXNlcnAiA2J1bioCCAEyChAuGIAEGCcYigUyChAuGIAEGCcYigUyChAAGIAEGBQYhwIyChAAGIAEGEMYigUyChAAGIAEGEMYigUyChAuGIAEGEMYigUyChAAGIAEGEMYigUyChAAGIAEGEMYigUyChAAGIAEGEMYigUyChAAGIAEGEMYigUyFxAuGIAEGIoFGJcFGNwEGN4EGOAE2AEBSMNHUABY3ztwAXgBkAEAmAHDAaABwgSqAQMwLjO4AQPIAQD4AQGYAgWgAsQPqAIRwgIHECMYJxjqAsICBxAuGCcY6gLCAhQQABiABBjjBBi0AhjpBBjqAtgBAcICFxAuGIAEGOMEGLQCGMgDGOkEGOoC2AEBwgIKECMYgAQYJxiKBcICDRAuGIAEGLEDGEMYigXCAg4QABiABBixAxiDARiKBZgDBvEFwPgVvF0inmq6BgYIARABGAGSBwcxLjMuNy0xoAejOrIHAzAuM7gHzwTCBwUwLjEuNMgHEQ&sclient=gws-wiz-serp#wptab=si:AMgyJEsv3PmLaKFqbPTQ9CSol7BvG13LDiFVNQjxDtWGc_GjI5YJ0LJQxzO5oEHS-IrjIUbh06oLTuUMusm4FjL3m9-tDR0HfqWCPe3Ume4J3B8Fhne6-GaXYrDYwnawf39o64h7LaMJrycTCobO7kqXnclo874Gp3baNhYqiiaq3ywU8228hEmE3vP0dY4Jt_oOJBQOxTdB',
                             'https://www.google.com/search?q=bundesliga+2&sca_esv=39d1a7f4746557b0&sxsrf=AE3TifNvvJXkyNOJ7VqRpb6Xv8mOpW8htg%3A1757117082087&ei=mnq7aIuGBaSXwbkPrvmR2QU&gs_ssp=eJzj4tTP1TewTMuyKDdg9OJJKs1LSS3OyUxPVDACAGDOB74&oq=bundes&gs_lp=Egxnd3Mtd2l6LXNlcnAiBmJ1bmRlcyoCCAAyChAuGIAEGCcYigUyChAuGIAEGCcYigUyChAAGIAEGEMYigUyChAAGIAEGEMYigUyChAAGIAEGEMYigUyChAAGIAEGBQYhwIyChAAGIAEGEMYigUyChAAGIAEGEMYigUyChAAGIAEGEMYigUyBRAuGIAEMhcQLhiABBiKBRiXBRjcBBjeBBjgBNgBAUinSVDNKVjlQ3ADeAGQAQCYAbMBoAHGDaoBBDAuMTG4AQHIAQD4AQGYAg-gAtkWwgIKECMYgAQYJxiKBcICBRAAGIAEwgIHECMYsAIYJ8ICBxAAGIAEGA3CAgoQLhiABBhDGIoFwgIEEAAYA8ICCBAAGIAEGLEDmAMAugYGCAEQARgUkgcIMy4xMS43LTGgB-l-sgcEMC4xMbgH7A3CBwUwLjguN8gHKg&sclient=gws-wiz-serp#wptab=si:AMgyJEsv3PmLaKFqbPTQ9CSol7BvG13LDiFVNQjxDtWGc_GjI5YJ0LJQxzO5oEHS-IrjIUbh06oLTuUMusm4FjL3m9-tDR0HfqWCPe3Ume4J3B8FhkjPOYt4KL6SdA2It2YoJ8XECYR7nthXO6Sg6oApJvRVahLHWR_DpBIVf1DcgA0mrdSWi0Npdp_e4ng0iycDjDCNM8wo',
                             'https://www.google.com/search?q=liga+portugal&sca_esv=39d1a7f4746557b0&sxsrf=AE3TifOG8x20fCc7uGunE35kCScNbzg6CA%3A1757117102620&ei=rnq7aJzLJYqIwbkP2J2HwQo&oq=liga+por&gs_lp=Egxnd3Mtd2l6LXNlcnAiCGxpZ2EgcG9yKgIIADISEC4YgAQYsQMYQxhGGIoFGP0BMgoQLhiABBhDGIoFMgoQABiABBgUGIcCMgUQABiABDIFEAAYgAQyChAAGIAEGBQYhwIyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMh4QABiABBixAxhDGEYYigUY_QEYlwUYjAUY3QTYAQFI6SNQkQtYnBZwAngBkAEAmAGDAqAB7QyqAQUwLjguMbgBA8gBAPgBAZgCDKAC-RfCAgoQIxiABBgnGIoFwgIEECMYJ8ICGRAuGIAEGEMYigUYlwUY3AQY3gQY4ATYAQHCAgoQLhiABBgnGIoFwgINEC4YgAQYsQMYQxiKBcICHBAuGIAEGLEDGEMYigUYlwUY3AQY3gQY4ATYAQHCAhAQLhiABBixAxhDGIMBGIoFwgINEC4YgAQYQxjUAhiKBcICBRAuGIAEmAMAugYGCAEQARgUkgcJMi44LjEuNy0xoAeWtAGyBwUwLjguMbgHlQ3CBwYwLjIuMTDIBys&sclient=gws-wiz-serp#wptab=si:AMgyJEsv3PmLaKFqbPTQ9CSol7BvG13LDiFVNQjxDtWGc_GjI5YJ0LJQxzO5oEHS-IrjIUbh06oLTuUMusm4FjL3m9-tDR0HfqWCPe3Ume4J3B8FhvRfmV-zL6dRLxUulq-f58E2ma8nkTjoseIEZVi9xA10OhjUuPn5I6830g1KTDz_Mfl3JURDUc2HnDXMhwoFfvoKX25m',
                             'https://www.google.com/search?q=liga+arabia&sca_esv=39d1a7f4746557b0&sxsrf=AE3TifMFaUKYuCyWZpUQschJqn6t28KU9A%3A1757117116229&ei=vHq7aKTjDYCSwbkP-PSQaQ&gs_ssp=eJzj4tTP1TdINjeuyDVg9OLOyUxPVEgsSkzKTAQAViEHZA&oq=liga+arab&gs_lp=Egxnd3Mtd2l6LXNlcnAiCWxpZ2EgYXJhYioCCAAyCBAuGIAEGLEDMgwQABiABBhDGIoFGAoyBRAAGIAEMgoQABiABBgUGIcCMgUQABiABDIIEC4YgAQY1AIyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMhcQLhiABBixAxiXBRjcBBjeBBjgBNgBAUicLFDQDFjiIXADeAGQAQCYAfkBoAGOD6oBBjAuMTAuMbgBA8gBAPgBAZgCDqACxA_CAgoQIxiABBgnGIoFwgIEECMYJ8ICChAuGIAEGEMYigXCAg0QLhiABBixAxhDGIoFwgIKEC4YgAQYJxiKBcICGRAuGIAEGEMYigUYlwUY3AQY3gQY4ATYAQHCAgoQLhiABBgUGIcCwgIOEC4YgAQYsQMYxwEYrwHCAggQABiABBixA8ICHBAuGIAEGLEDGEMYigUYlwUY3AQY3gQY4ATYAQHCAgUQLhiABMICFBAuGIAEGJcFGNwEGN4EGOAE2AEBmAMAugYGCAEQARgUkgcGMy4xMC4xoAeIxgGyBwYwLjEwLjG4B7sPwgcGMC4zLjExyAcw&sclient=gws-wiz-serp#wptab=si:AMgyJEsv3PmLaKFqbPTQ9CSol7BvG13LDiFVNQjxDtWGc_GjI5YJ0LJQxzO5oEHS-IrjIUbh06oLTuUMusm4FjL3m9-tDR0HfqWCPe3Ume4J3B8FhtH1movEJsI5nJhb2ILBUQTEptUm93rBQ63-9BZlpNEYdOth1OJ-KxULFNqQiNuEuA6ZXFp5FutNfD-6Eikt2cB8Vb_-83WgCjW9D3-CbgzPF1OCfA%3D%3D'
                             ] #Links de google donde estan la lista de equipos de un campeonato
        self.equipos_dict = self.get_dict_of_csv()

    def get_dict_of_csv(self):
        if os.path.isfile('team_list/teams.csv'):
            df = pd.read_csv('team_list/teams.csv', sep=';', quotechar='"')
            self.df = df  # guardamos el dataframe entero
            # Creamos un diccionario solo para saber qué equipos existen
            return dict(zip(df["Equipo"], df["ID"]))
        else:
            # DataFrame inicial con un equipo desconocido
            self.df = pd.DataFrame([{
                "Equipo": "Equipo Desconocido",
                "ID": -1,
                "ID_365": "",
                "Name365": ""
            }])
            return {"Equipo Desconocido": -1}

    def save_csv(self):
        self.df.to_csv('team_list/teams.csv', sep=';', index=False)

    def getTeams(self, soup):
        try:
            campeonato = soup.find('div', class_='PZPZlf ssJ7i')
            team_tables = soup.find_all('table', class_='Jzru1c')  # Encuentra todas las tablas

            for team_table in team_tables:  # Itera sobre cada tabla encontrada
                rows = team_table.select('tr.imso-loa.imso-hov')  # Selecciona las filas dentro de cada tabla
                for row in rows:
                    team_name = row.get("aria-label")
                    if team_name and team_name not in self.equipos_dict:
                        new_id = len(self.df)
                        # Agregamos fila nueva con valores vacíos en ID_365 y Name365
                        self.df.loc[len(self.df)] = [team_name, new_id, "", ""]
                        self.equipos_dict[team_name] = new_id

        except Exception as e:
            print(f"Error al obtener equipos para {campeonato}: {e}")

    # Función para procesar las URLs
    def procesar_urls(self, urls):
        for url in urls:
            try:
                self.driver.delete_all_cookies()
                self.driver.get(url)
                time.sleep(4)
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                self.getTeams(soup)
                
            except Exception as e:
                print(f"Error procesando la URL {url}: {e}")

        # Cerrar el navegador
        self.driver.quit()
            
if __name__ == "__main__":
    equipment_collection = EquipmentCollection()
    df = equipment_collection.procesar_urls(equipment_collection.urls_torneos)
    equipment_collection.save_csv()