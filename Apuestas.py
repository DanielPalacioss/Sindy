#Como la regresion logistica necesita mas de 1 variable para predecir el futuro, necesitamos que ya sea en los partidos del local o el visitante alla al un partido donde gane y otro donde pierda. si no da error
#Si no hay ningun gol de parte de un equipo en ninguno de los partidos a analizar dara error
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import math
import pandas as pd


# Configuración de Selenium con ChromeDriver
service =  Service(executable_path= 'chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Ingreso de datos por parte del usuario
equipo_objetivo_1 = "Real Madrid"#input("Ingresa el primer equipo objetivo: ")
equipo_objetivo_2 = "LOSC"#input("Ingresa el segundo equipo objetivo: ")

# Estadísticas a excluir (fijas como en el código original)
estadisticas_excluidas = ["Posesión", "Precisión de los pases", "Posición adelantada"]

# Ingreso de URLs
#num_urls = int(input("¿Cuántas URLs deseas ingresar? "))
urls_equipo_1 = ["https://www.google.com/search?sca_esv=22628e78e0652884&sca_upv=1&rlz=1C1UEAD_esCO992CO992&cs=0&q=Real+Madrid+Club+de+F%C3%BAtbol&stick=H4sIAAAAAAAAAONgVuLQz9U3MMsxMnrEaMwt8PLHPWEprUlrTl5jVOHiCs7IL3fNK8ksqRQS42KDsnikuLjgmngWsUoHpSbmKPgmphRlpig455QmKaSkKrgd3lWSlJ8DAEwS8v5gAAAA&ved=2ahUKEwjw6JLx2e6IAxUy8MkDHQtML4EQukt6BAgBEBY#sie=m;/g/11w3rxw5kw;2;/m/09gqx;dt;fp;1;;;&wptab=si:ACC90nzGOv0hOuVipoI1QtmCZV-chuqv391GCsKasZDU0KidW4lj7Tf6R_yBkXdJOw36Ekfq3ajaAiW9ybSeCd_pFvY6XeQBLX5jITNkAxM_sNo-gXd8jc8gc9frd98nYzp35r8hnmmXZnfuEuDdvOi90_B1E8-sNQRYtdAU0L8mnvSU7qj2ldn9e8difjiUJudpPoAgzDdTzKOFTnJZGJM4qXy-HcwCArAzQBKkKMzmUpD8J5PlYi4%3D",
"https://www.google.com/search?sca_esv=22628e78e0652884&sca_upv=1&rlz=1C1UEAD_esCO992CO992&cs=0&q=Real+Madrid+Club+de+F%C3%BAtbol&stick=H4sIAAAAAAAAAONgVuLQz9U3MMsxMnrEaMwt8PLHPWEprUlrTl5jVOHiCs7IL3fNK8ksqRQS42KDsnikuLjgmngWsUoHpSbmKPgmphRlpig455QmKaSkKrgd3lWSlJ8DAEwS8v5gAAAA&ved=2ahUKEwjw6JLx2e6IAxUy8MkDHQtML4EQukt6BAgBEBY#sie=m;/g/11w3rxnbjt;2;/m/09gqx;dt;fp;1;;;&wptab=si:ACC90nzGOv0hOuVipoI1QtmCZV-chuqv391GCsKasZDU0KidW4lj7Tf6R_yBkXdJOw36Ekfq3ajaAiW9ybSeCd_pFvY6XeQBLX5jITNkAxM_sNo-gXd8jc8gc9frd98nYzp35r8hnmmXZnfuEuDdvOi90_B1E8-sNQRYtdAU0L8mnvSU7qj2ldn9e8difjiUJudpPoAgzDdTzKOFTnJZGJM4qXy-HcwCArAzQBKkKMzmUpD8J5PlYi4%3D",
"https://www.google.com/search?sca_esv=22628e78e0652884&sca_upv=1&rlz=1C1UEAD_esCO992CO992&cs=0&q=Real+Madrid+Club+de+F%C3%BAtbol&stick=H4sIAAAAAAAAAONgVuLQz9U3MMsxMnrEaMwt8PLHPWEprUlrTl5jVOHiCs7IL3fNK8ksqRQS42KDsnikuLjgmngWsUoHpSbmKPgmphRlpig455QmKaSkKrgd3lWSlJ8DAEwS8v5gAAAA&ved=2ahUKEwjw6JLx2e6IAxUy8MkDHQtML4EQukt6BAgBEBY#sie=m;/g/11y5mkfnwd;2;/m/09gqx;dt;fp;1;;;&wptab=si:ACC90nzGOv0hOuVipoI1QtmCZV-chuqv391GCsKasZDU0KidW4lj7Tf6R_yBkXdJOw36Ekfq3ajaAiW9ybSeCd_pFvY6XeQBLX5jITNkAxM_sNo-gXd8jc8gc9frd98nYzp35r8hnmmXZnfuEuDdvOi90_B1E8-sNQRYtdAU0L8mnvSU7qj2ldn9e8difjiUJudpPoAgzDdTzKOFTnJZGJM4qXy-HcwCArAzQBKkKMzmUpD8J5PlYi4%3D",
"https://www.google.com/search?sca_esv=22628e78e0652884&sca_upv=1&rlz=1C1UEAD_esCO992CO992&cs=0&q=Real+Madrid+Club+de+F%C3%BAtbol&stick=H4sIAAAAAAAAAONgVuLQz9U3MMsxMnrEaMwt8PLHPWEprUlrTl5jVOHiCs7IL3fNK8ksqRQS42KDsnikuLjgmngWsUoHpSbmKPgmphRlpig455QmKaSkKrgd3lWSlJ8DAEwS8v5gAAAA&ved=2ahUKEwjw6JLx2e6IAxUy8MkDHQtML4EQukt6BAgBEBY#sie=m;/g/11wbz936w3;2;/m/0c1q0;dt;fp;1;;;&wptab=si:ACC90nzGOv0hOuVipoI1QtmCZV-chuqv391GCsKasZDU0KidW4lj7Tf6R_yBkXdJOw36Ekfq3ajaAiW9ybSeCd_pFvY6XeQBLX5jITNkAxM_sNo-gXd8jc8gc9frd98nYzp35r8hnmmXZnfuEuDdvOi90_B1E8-sNQRYtdAU0L8mnvSU7qj2ldn9e8difjiUJudpPoAgzDdTzKOFTnJZGJM4qXy-HcwCArAzQBKkKMzmUpD8J5PlYi4%3D",
"https://www.google.com/search?sca_esv=22628e78e0652884&sca_upv=1&rlz=1C1UEAD_esCO992CO992&cs=0&q=Real+Madrid+Club+de+F%C3%BAtbol&stick=H4sIAAAAAAAAAONgVuLQz9U3MMsxMnrEaMwt8PLHPWEprUlrTl5jVOHiCs7IL3fNK8ksqRQS42KDsnikuLjgmngWsUoHpSbmKPgmphRlpig455QmKaSkKrgd3lWSlJ8DAEwS8v5gAAAA&ved=2ahUKEwjw6JLx2e6IAxUy8MkDHQtML4EQukt6BAgBEBY#sie=m;/g/11w1j0_cxv;2;/m/09gqx;dt;fp;1;;;&wptab=si:ACC90nzGOv0hOuVipoI1QtmCZV-chuqv391GCsKasZDU0KidW4lj7Tf6R_yBkXdJOw36Ekfq3ajaAiW9ybSeCd_pFvY6XeQBLX5jITNkAxM_sNo-gXd8jc8gc9frd98nYzp35r8hnmmXZnfuEuDdvOi90_B1E8-sNQRYtdAU0L8mnvSU7qj2ldn9e8difjiUJudpPoAgzDdTzKOFTnJZGJM4qXy-HcwCArAzQBKkKMzmUpD8J5PlYi4%3D",
"https://www.google.com/search?sca_esv=22628e78e0652884&sca_upv=1&rlz=1C1UEAD_esCO992CO992&cs=0&q=Real+Madrid+Club+de+F%C3%BAtbol&stick=H4sIAAAAAAAAAONgVuLQz9U3MMsxMnrEaMwt8PLHPWEprUlrTl5jVOHiCs7IL3fNK8ksqRQS42KDsnikuLjgmngWsUoHpSbmKPgmphRlpig455QmKaSkKrgd3lWSlJ8DAEwS8v5gAAAA&ved=2ahUKEwjw6JLx2e6IAxUy8MkDHQtML4EQukt6BAgBEBY#sie=m;/g/11w3s1nv6p;2;/m/09gqx;dt;fp;1;;;&wptab=si:ACC90nzGOv0hOuVipoI1QtmCZV-chuqv391GCsKasZDU0KidW4lj7Tf6R_yBkXdJOw36Ekfq3ajaAiW9ybSeCd_pFvY6XeQBLX5jITNkAxM_sNo-gXd8jc8gc9frd98nYzp35r8hnmmXZnfuEuDdvOi90_B1E8-sNQRYtdAU0L8mnvSU7qj2ldn9e8difjiUJudpPoAgzDdTzKOFTnJZGJM4qXy-HcwCArAzQBKkKMzmUpD8J5PlYi4%3D",
"https://www.google.com/search?sca_esv=22628e78e0652884&sca_upv=1&rlz=1C1UEAD_esCO992CO992&cs=0&q=Real+Madrid+Club+de+F%C3%BAtbol&stick=H4sIAAAAAAAAAONgVuLQz9U3MMsxMnrEaMwt8PLHPWEprUlrTl5jVOHiCs7IL3fNK8ksqRQS42KDsnikuLjgmngWsUoHpSbmKPgmphRlpig455QmKaSkKrgd3lWSlJ8DAEwS8v5gAAAA&ved=2ahUKEwjw6JLx2e6IAxUy8MkDHQtML4EQukt6BAgBEBY#sie=m;/g/11w1j102n4;2;/m/09gqx;dt;fp;1;;;&wptab=si:ACC90nzGOv0hOuVipoI1QtmCZV-chuqv391GCsKasZDU0KidW4lj7Tf6R_yBkXdJOw36Ekfq3ajaAiW9ybSeCd_pFvY6XeQBLX5jITNkAxM_sNo-gXd8jc8gc9frd98nYzp35r8hnmmXZnfuEuDdvOi90_B1E8-sNQRYtdAU0L8mnvSU7qj2ldn9e8difjiUJudpPoAgzDdTzKOFTnJZGJM4qXy-HcwCArAzQBKkKMzmUpD8J5PlYi4%3D",
"https://www.google.com/search?sca_esv=22628e78e0652884&sca_upv=1&rlz=1C1UEAD_esCO992CO992&cs=0&q=Real+Madrid+Club+de+F%C3%BAtbol&stick=H4sIAAAAAAAAAONgVuLQz9U3MMsxMnrEaMwt8PLHPWEprUlrTl5jVOHiCs7IL3fNK8ksqRQS42KDsnikuLjgmngWsUoHpSbmKPgmphRlpig455QmKaSkKrgd3lWSlJ8DAEwS8v5gAAAA&ved=2ahUKEwjw6JLx2e6IAxUy8MkDHQtML4EQukt6BAgBEBY#sie=m;/g/11y5mkw2gl;2;/m/09gqx;dt;fp;1;;;&wptab=si:ACC90nzGOv0hOuVipoI1QtmCZV-chuqv391GCsKasZDU0KidW4lj7Tf6R_yBkXdJOw36Ekfq3ajaAiW9ybSeCd_pFvY6XeQBLX5jITNkAxM_sNo-gXd8jc8gc9frd98nYzp35r8hnmmXZnfuEuDdvOi90_B1E8-sNQRYtdAU0L8mnvSU7qj2ldn9e8difjiUJudpPoAgzDdTzKOFTnJZGJM4qXy-HcwCArAzQBKkKMzmUpD8J5PlYi4%3D",
"https://www.google.com/search?sca_esv=22628e78e0652884&sca_upv=1&rlz=1C1UEAD_esCO992CO992&cs=0&q=Real+Madrid+Club+de+F%C3%BAtbol&stick=H4sIAAAAAAAAAONgVuLQz9U3MMsxMnrEaMwt8PLHPWEprUlrTl5jVOHiCs7IL3fNK8ksqRQS42KDsnikuLjgmngWsUoHpSbmKPgmphRlpig455QmKaSkKrgd3lWSlJ8DAEwS8v5gAAAA&ved=2ahUKEwjw6JLx2e6IAxUy8MkDHQtML4EQukt6BAgBEBY#sie=m;/g/11w1j0jtm7;2;/m/09gqx;dt;fp;1;;;&wptab=si:ACC90nzGOv0hOuVipoI1QtmCZV-chuqv391GCsKasZDU0KidW4lj7Tf6R_yBkXdJOw36Ekfq3ajaAiW9ybSeCd_pFvY6XeQBLX5jITNkAxM_sNo-gXd8jc8gc9frd98nYzp35r8hnmmXZnfuEuDdvOi90_B1E8-sNQRYtdAU0L8mnvSU7qj2ldn9e8difjiUJudpPoAgzDdTzKOFTnJZGJM4qXy-HcwCArAzQBKkKMzmUpD8J5PlYi4%3D",
"https://www.google.com/search?sca_esv=22628e78e0652884&sca_upv=1&rlz=1C1UEAD_esCO992CO992&cs=0&q=Real+Madrid+Club+de+F%C3%BAtbol&stick=H4sIAAAAAAAAAONgVuLQz9U3MMsxMnrEaMwt8PLHPWEprUlrTl5jVOHiCs7IL3fNK8ksqRQS42KDsnikuLjgmngWsUoHpSbmKPgmphRlpig455QmKaSkKrgd3lWSlJ8DAEwS8v5gAAAA&ved=2ahUKEwjw6JLx2e6IAxUy8MkDHQtML4EQukt6BAgBEBY#sie=m;/g/11y4ydk586;2;/m/01xml3;dt;fp;1;;;&wptab=si:ACC90nzGOv0hOuVipoI1QtmCZV-chuqv391GCsKasZDU0KidW4lj7Tf6R_yBkXdJOw36Ekfq3ajaAiW9ybSeCd_pFvY6XeQBLX5jITNkAxM_sNo-gXd8jc8gc9frd98nYzp35r8hnmmXZnfuEuDdvOi90_B1E8-sNQRYtdAU0L8mnvSU7qj2ldn9e8difjiUJudpPoAgzDdTzKOFTnJZGJM4qXy-HcwCArAzQBKkKMzmUpD8J5PlYi4%3D"]
urls_equipo_2 = ["https://www.google.com/search?q=losc&rlz=1C1UEAD_esCO992CO992&oq=LosC&gs_lcrp=EgZjaHJvbWUqFQgAEAAYQxiDARjjAhixAxiABBiKBTIVCAAQABhDGIMBGOMCGLEDGIAEGIoFMhIIARAuGEMYgwEYsQMYgAQYigUyDAgCEAAYQxiABBiKBTIGCAMQABgDMg8IBBAuGAoYrwEYxwEYgAQyCQgFEAAYChiABDINCAYQLhivARjHARiABDIPCAcQLhgKGK8BGMcBGIAEMgcICBAuGIAEMgkICRAuGAoYgATSAQc4MTVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#sie=m;/g/11w3vpn404;2;/m/044hxl;dt;fp;1;;;&wptab=si:ACC90nxHVIQmruDWnwTL6DMm0w-fRIRhUxoHPNsJnEnV8zCuM5KLSWnMImIlpppFk_AeipYNPv1FwwzpZBUBlVSSfdvbonUvznept0lvJfSshjU2m85FZvNhYYWz3dx8wDv5Gwv566dzjLlYPXYup3sib3lzjWch_4OnxPTQ0aSv0KWanTvMYLbiOMwD_FqjmHVs0x7FCqLXSCGU0Y_Jkiaso8ei-8y6kKZcWZqISOWmXHX2Y_xf8Ys%3D",
"https://www.google.com/search?q=losc&rlz=1C1UEAD_esCO992CO992&oq=LosC&gs_lcrp=EgZjaHJvbWUqFQgAEAAYQxiDARjjAhixAxiABBiKBTIVCAAQABhDGIMBGOMCGLEDGIAEGIoFMhIIARAuGEMYgwEYsQMYgAQYigUyDAgCEAAYQxiABBiKBTIGCAMQABgDMg8IBBAuGAoYrwEYxwEYgAQyCQgFEAAYChiABDINCAYQLhivARjHARiABDIPCAcQLhgKGK8BGMcBGIAEMgcICBAuGIAEMgkICRAuGAoYgATSAQc4MTVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#sie=m;/g/11w1lq1bpq;2;/m/044hxl;dt;fp;1;;;&wptab=si:ACC90nxHVIQmruDWnwTL6DMm0w-fRIRhUxoHPNsJnEnV8zCuM5KLSWnMImIlpppFk_AeipYNPv1FwwzpZBUBlVSSfdvbonUvznept0lvJfSshjU2m85FZvNhYYWz3dx8wDv5Gwv566dzjLlYPXYup3sib3lzjWch_4OnxPTQ0aSv0KWanTvMYLbiOMwD_FqjmHVs0x7FCqLXSCGU0Y_Jkiaso8ei-8y6kKZcWZqISOWmXHX2Y_xf8Ys%3D",
"https://www.google.com/search?q=losc&rlz=1C1UEAD_esCO992CO992&oq=LosC&gs_lcrp=EgZjaHJvbWUqFQgAEAAYQxiDARjjAhixAxiABBiKBTIVCAAQABhDGIMBGOMCGLEDGIAEGIoFMhIIARAuGEMYgwEYsQMYgAQYigUyDAgCEAAYQxiABBiKBTIGCAMQABgDMg8IBBAuGAoYrwEYxwEYgAQyCQgFEAAYChiABDINCAYQLhivARjHARiABDIPCAcQLhgKGK8BGMcBGIAEMgcICBAuGIAEMgkICRAuGAoYgATSAQc4MTVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#sie=m;/g/11wbz9rl0d;2;/m/0c1q0;dt;fp;1;;;&wptab=si:ACC90nxHVIQmruDWnwTL6DMm0w-fRIRhUxoHPNsJnEnV8zCuM5KLSWnMImIlpppFk_AeipYNPv1FwwzpZBUBlVSSfdvbonUvznept0lvJfSshjU2m85FZvNhYYWz3dx8wDv5Gwv566dzjLlYPXYup3sib3lzjWch_4OnxPTQ0aSv0KWanTvMYLbiOMwD_FqjmHVs0x7FCqLXSCGU0Y_Jkiaso8ei-8y6kKZcWZqISOWmXHX2Y_xf8Ys%3D",
"https://www.google.com/search?q=losc&rlz=1C1UEAD_esCO992CO992&oq=LosC&gs_lcrp=EgZjaHJvbWUqFQgAEAAYQxiDARjjAhixAxiABBiKBTIVCAAQABhDGIMBGOMCGLEDGIAEGIoFMhIIARAuGEMYgwEYsQMYgAQYigUyDAgCEAAYQxiABBiKBTIGCAMQABgDMg8IBBAuGAoYrwEYxwEYgAQyCQgFEAAYChiABDINCAYQLhivARjHARiABDIPCAcQLhgKGK8BGMcBGIAEMgcICBAuGIAEMgkICRAuGAoYgATSAQc4MTVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#sie=m;/g/11y5qblzhl;2;/m/044hxl;dt;fp;1;;;&wptab=si:ACC90nxHVIQmruDWnwTL6DMm0w-fRIRhUxoHPNsJnEnV8zCuM5KLSWnMImIlpppFk_AeipYNPv1FwwzpZBUBlVSSfdvbonUvznept0lvJfSshjU2m85FZvNhYYWz3dx8wDv5Gwv566dzjLlYPXYup3sib3lzjWch_4OnxPTQ0aSv0KWanTvMYLbiOMwD_FqjmHVs0x7FCqLXSCGU0Y_Jkiaso8ei-8y6kKZcWZqISOWmXHX2Y_xf8Ys%3D",
"https://www.google.com/search?q=losc&rlz=1C1UEAD_esCO992CO992&oq=LosC&gs_lcrp=EgZjaHJvbWUqFQgAEAAYQxiDARjjAhixAxiABBiKBTIVCAAQABhDGIMBGOMCGLEDGIAEGIoFMhIIARAuGEMYgwEYsQMYgAQYigUyDAgCEAAYQxiABBiKBTIGCAMQABgDMg8IBBAuGAoYrwEYxwEYgAQyCQgFEAAYChiABDINCAYQLhivARjHARiABDIPCAcQLhgKGK8BGMcBGIAEMgcICBAuGIAEMgkICRAuGAoYgATSAQc4MTVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#sie=m;/g/11w1lqsgjw;2;/m/044hxl;dt;fp;1;;;&wptab=si:ACC90nxHVIQmruDWnwTL6DMm0w-fRIRhUxoHPNsJnEnV8zCuM5KLSWnMImIlpppFk_AeipYNPv1FwwzpZBUBlVSSfdvbonUvznept0lvJfSshjU2m85FZvNhYYWz3dx8wDv5Gwv566dzjLlYPXYup3sib3lzjWch_4OnxPTQ0aSv0KWanTvMYLbiOMwD_FqjmHVs0x7FCqLXSCGU0Y_Jkiaso8ei-8y6kKZcWZqISOWmXHX2Y_xf8Ys%3D",
"https://www.google.com/search?q=losc&rlz=1C1UEAD_esCO992CO992&oq=LosC&gs_lcrp=EgZjaHJvbWUqFQgAEAAYQxiDARjjAhixAxiABBiKBTIVCAAQABhDGIMBGOMCGLEDGIAEGIoFMhIIARAuGEMYgwEYsQMYgAQYigUyDAgCEAAYQxiABBiKBTIGCAMQABgDMg8IBBAuGAoYrwEYxwEYgAQyCQgFEAAYChiABDINCAYQLhivARjHARiABDIPCAcQLhgKGK8BGMcBGIAEMgcICBAuGIAEMgkICRAuGAoYgATSAQc4MTVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#sie=m;/g/11w9n40kyg;2;/m/0c1q0;dt;fp;1;;;&wptab=si:ACC90nxHVIQmruDWnwTL6DMm0w-fRIRhUxoHPNsJnEnV8zCuM5KLSWnMImIlpppFk_AeipYNPv1FwwzpZBUBlVSSfdvbonUvznept0lvJfSshjU2m85FZvNhYYWz3dx8wDv5Gwv566dzjLlYPXYup3sib3lzjWch_4OnxPTQ0aSv0KWanTvMYLbiOMwD_FqjmHVs0x7FCqLXSCGU0Y_Jkiaso8ei-8y6kKZcWZqISOWmXHX2Y_xf8Ys%3D",
"https://www.google.com/search?q=losc&rlz=1C1UEAD_esCO992CO992&oq=LosC&gs_lcrp=EgZjaHJvbWUqFQgAEAAYQxiDARjjAhixAxiABBiKBTIVCAAQABhDGIMBGOMCGLEDGIAEGIoFMhIIARAuGEMYgwEYsQMYgAQYigUyDAgCEAAYQxiABBiKBTIGCAMQABgDMg8IBBAuGAoYrwEYxwEYgAQyCQgFEAAYChiABDINCAYQLhivARjHARiABDIPCAcQLhgKGK8BGMcBGIAEMgcICBAuGIAEMgkICRAuGAoYgATSAQc4MTVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#sie=m;/g/11y5qbh0bl;2;/m/044hxl;dt;fp;1;;;&wptab=si:ACC90nxHVIQmruDWnwTL6DMm0w-fRIRhUxoHPNsJnEnV8zCuM5KLSWnMImIlpppFk_AeipYNPv1FwwzpZBUBlVSSfdvbonUvznept0lvJfSshjU2m85FZvNhYYWz3dx8wDv5Gwv566dzjLlYPXYup3sib3lzjWch_4OnxPTQ0aSv0KWanTvMYLbiOMwD_FqjmHVs0x7FCqLXSCGU0Y_Jkiaso8ei-8y6kKZcWZqISOWmXHX2Y_xf8Ys%3D",
"https://www.google.com/search?q=losc&rlz=1C1UEAD_esCO992CO992&oq=LosC&gs_lcrp=EgZjaHJvbWUqFQgAEAAYQxiDARjjAhixAxiABBiKBTIVCAAQABhDGIMBGOMCGLEDGIAEGIoFMhIIARAuGEMYgwEYsQMYgAQYigUyDAgCEAAYQxiABBiKBTIGCAMQABgDMg8IBBAuGAoYrwEYxwEYgAQyCQgFEAAYChiABDINCAYQLhivARjHARiABDIPCAcQLhgKGK8BGMcBGIAEMgcICBAuGIAEMgkICRAuGAoYgATSAQc4MTVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#sie=m;/g/11w39t5tp1;2;/m/0c1q0;dt;fp;1;;;&wptab=si:ACC90nxHVIQmruDWnwTL6DMm0w-fRIRhUxoHPNsJnEnV8zCuM5KLSWnMImIlpppFk_AeipYNPv1FwwzpZBUBlVSSfdvbonUvznept0lvJfSshjU2m85FZvNhYYWz3dx8wDv5Gwv566dzjLlYPXYup3sib3lzjWch_4OnxPTQ0aSv0KWanTvMYLbiOMwD_FqjmHVs0x7FCqLXSCGU0Y_Jkiaso8ei-8y6kKZcWZqISOWmXHX2Y_xf8Ys%3D",
"https://www.google.com/search?q=losc&rlz=1C1UEAD_esCO992CO992&oq=LosC&gs_lcrp=EgZjaHJvbWUqFQgAEAAYQxiDARjjAhixAxiABBiKBTIVCAAQABhDGIMBGOMCGLEDGIAEGIoFMhIIARAuGEMYgwEYsQMYgAQYigUyDAgCEAAYQxiABBiKBTIGCAMQABgDMg8IBBAuGAoYrwEYxwEYgAQyCQgFEAAYChiABDINCAYQLhivARjHARiABDIPCAcQLhgKGK8BGMcBGIAEMgcICBAuGIAEMgkICRAuGAoYgATSAQc4MTVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#sie=m;/g/11w1lqp059;2;/m/044hxl;dt;fp;1;;;&wptab=si:ACC90nxHVIQmruDWnwTL6DMm0w-fRIRhUxoHPNsJnEnV8zCuM5KLSWnMImIlpppFk_AeipYNPv1FwwzpZBUBlVSSfdvbonUvznept0lvJfSshjU2m85FZvNhYYWz3dx8wDv5Gwv566dzjLlYPXYup3sib3lzjWch_4OnxPTQ0aSv0KWanTvMYLbiOMwD_FqjmHVs0x7FCqLXSCGU0Y_Jkiaso8ei-8y6kKZcWZqISOWmXHX2Y_xf8Ys%3D",
"https://www.google.com/search?q=losc&rlz=1C1UEAD_esCO992CO992&oq=LosC&gs_lcrp=EgZjaHJvbWUqFQgAEAAYQxiDARjjAhixAxiABBiKBTIVCAAQABhDGIMBGOMCGLEDGIAEGIoFMhIIARAuGEMYgwEYsQMYgAQYigUyDAgCEAAYQxiABBiKBTIGCAMQABgDMg8IBBAuGAoYrwEYxwEYgAQyCQgFEAAYChiABDINCAYQLhivARjHARiABDIPCAcQLhgKGK8BGMcBGIAEMgcICBAuGIAEMgkICRAuGAoYgATSAQc4MTVqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#sie=m;/g/11w2x8pl9c;2;/m/0c1q0;dt;fp;1;;;&wptab=si:ACC90nxHVIQmruDWnwTL6DMm0w-fRIRhUxoHPNsJnEnV8zCuM5KLSWnMImIlpppFk_AeipYNPv1FwwzpZBUBlVSSfdvbonUvznept0lvJfSshjU2m85FZvNhYYWz3dx8wDv5Gwv566dzjLlYPXYup3sib3lzjWch_4OnxPTQ0aSv0KWanTvMYLbiOMwD_FqjmHVs0x7FCqLXSCGU0Y_Jkiaso8ei-8y6kKZcWZqISOWmXHX2Y_xf8Ys%3D"]

#print("Ingresa las URLs para el primer equipo:")
#for _ in range(num_urls):
#    url = input(f"URL #{len(urls_equipo_1) + 1}: ")
#    urls_equipo_1.append(url)

#print("Ingresa las URLs para el segundo equipo:")
#for _ in range(num_urls):
#    url = input(f"URL #{len(urls_equipo_2) + 1}: ")
#    urls_equipo_2.append(url)

# Diccionario para almacenar las estadísticas de los partidos
stats = {equipo_objetivo_1: {}, equipo_objetivo_2: {}}

def obtener_estadisticas(soup, equipo_objetivo):
    try:
        stats_table = soup.find('div', class_='lr-imso-ss-wdm')
        partido_stats = {}

        headers = stats_table.find_all('th', class_='jqZdce')
        equipo_columna = 0 if headers[0].find('img')['alt'] == equipo_objetivo else 1
        rows = stats_table.select('tr.MzWkAb')
        for row in rows:
            stat_name = row.find('th').text
            if stat_name not in estadisticas_excluidas:
                stat_value = int(row.find_all('td')[equipo_columna].text.strip())
                partido_stats[stat_name] = stat_value        

        return partido_stats
    except Exception as e:
        print(f"Error al obtener estadísticas para {equipo_objetivo}: {e}")
        return None

def obtener_goles_por_tiempo(soup, equipo_objetivo):
    goles_por_tiempo = {
        'goles_primera_mitad': 0, 
        'goles_segunda_mitad': 0,
        'goles_totales': 0,  # Campo para goles totales
        'gano': 0  # Nuevo campo booleano para indicar si ganó o no
    }

    try:
        # Encontrar la sección de resultados
        equipo_local = soup.find('div', class_='imso_mh__first-tn-ed').find('span').text
        equipo_visitante = soup.find('div', class_='imso_mh__second-tn-ed').find('span').text
        # Buscar los goles en el marcador principal
        marcador_local = int(soup.find('div', class_='imso_mh__l-tm-sc').text.strip())
        
        marcador_visitante = int(soup.find('div', class_='imso_mh__r-tm-sc').text.strip())
        
        # Si ambos equipos tienen 0 goles, retornar directamente
        if marcador_local == 0 and marcador_visitante == 0:
            print(f"Ambos equipos no tienen goles en el partido actual ({equipo_local} vs {equipo_visitante}).")
            return goles_por_tiempo

        # Buscar todos los eventos de goles directamente desde los spans
        eventos_goles = soup.find_all('span', class_='liveresults-sports-immersive__game-minute')

        # Limitar el recorrido solo a la cantidad de goles marcados
        goles_totales_en_partido = marcador_local + marcador_visitante
        eventos_goles = eventos_goles[:goles_totales_en_partido]  # Solo tomar el número exacto de eventos de goles

        # Procesar los eventos de goles
        for minuto_tag in eventos_goles:
            # Extraer el minuto del primer span hijo
            minuto = int(minuto_tag.find('span').text.strip())
            
            # Determinar a qué equipo pertenece el gol
            equipo_goleador = equipo_local if minuto_tag.find_parent('div', class_='imso_gs__left-team') else equipo_visitante
            
            if equipo_goleador == equipo_objetivo:
                if minuto <= 45:
                    goles_por_tiempo['goles_primera_mitad'] += 1
                else:
                    goles_por_tiempo['goles_segunda_mitad'] += 1

        # Calcular la cantidad total de goles
        goles_por_tiempo['goles_totales'] = goles_por_tiempo['goles_primera_mitad'] + goles_por_tiempo['goles_segunda_mitad']

        # Determinar si el equipo objetivo ganó o no
        if equipo_objetivo == equipo_local:
            goles_objetivo = marcador_local
            goles_rival = marcador_visitante
        else:
            goles_objetivo = marcador_visitante
            goles_rival = marcador_local

        # Si el equipo objetivo tiene más goles que el rival, ganó (1), si no, perdió o empató (0)
        if goles_objetivo > goles_rival:
            goles_por_tiempo['gano'] = 1
        else:
            goles_por_tiempo['gano'] = 0

        return goles_por_tiempo

    except Exception as e:
        print(f"Error al obtener goles para {equipo_objetivo}: {e}")
        return None
    

# Función para procesar las URLs
def procesar_urls(urls, equipo_objetivo):
    partido_stats = {}
    for idx, url in enumerate(urls, start=1):
        try:
            driver.delete_all_cookies()
            driver.get(url)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            stats = obtener_estadisticas(soup, equipo_objetivo)
            goles_por_tiempo = obtener_goles_por_tiempo(soup, equipo_objetivo)

            if stats and goles_por_tiempo:
                partido_key = f"Partido #{idx}"
                partido_stats[partido_key] = {**stats, **goles_por_tiempo}
            else:
                print(f"El equipo {equipo_objetivo} no se encontró en la URL: {url}")
        except Exception as e:
            print(f"Error procesando la URL {url} para {equipo_objetivo}: {e}")
    return partido_stats



# Procesar las URLs de ambos equipos
stats[equipo_objetivo_1] = procesar_urls(urls_equipo_1, equipo_objetivo_1)
stats[equipo_objetivo_2] = procesar_urls(urls_equipo_2, equipo_objetivo_2)

# Cerrar el navegador
driver.quit()




def calcular_desviacion_estandar_y_datos(stats):
    # Obtener los nombres de los equipos (las claves del diccionario)
    equipo1, equipo2 = list(stats.keys())
    # Asignar los partidos de cada equipo desde el diccionario
    partidos_equipo1 = dict(list(stats[equipo1].items())[:6])
    partidos_equipo2 = dict(list(stats[equipo2].items())[:6])
    p = len(partidos_equipo1)  # Número de partidos

    # Variables acumulativas para el equipo 1
    Tgoles, Tcorner, TrematesAr, Tremates, TtarjetasA, Tfaltas, Tpases, TgolesPT, TgolesST = 0, 0, 0, 0, 0, 0, 0, 0, 0
    goles_equipo1, corner_equipo1 = [], []

    # Variables acumulativas para el equipo 2
    Tgoles2, Tcorner2, TrematesAr2, Tremates2, TtarjetasA2, Tfaltas2, Tpases2, TgolesPT2, TgolesST2 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    goles_equipo2, corner_equipo2 = [], []

    # Acumular datos del equipo 1 y 2
    for partidosN in partidos_equipo1:
        partido = partidos_equipo1[partidosN]
        goles = partido['goles_totales']
        corner = partido['Tiros de esquina']
        remates_arco = partido['Remates al arco']
        remates = partido['Remates']
        tarjetas_amarillas = partido['Tarjetas amarillas']
        faltas = partido['Faltas']
        pases = partido['Pases']
        goles_primera_mitad = partido['goles_primera_mitad']
        goles_segunda_mitad = partido['goles_segunda_mitad']

        # Sumar estadísticas
        Tgoles += goles
        Tcorner += corner
        TrematesAr += remates_arco
        Tremates += remates
        TtarjetasA += tarjetas_amarillas
        Tfaltas += faltas
        Tpases += pases
        TgolesPT += goles_primera_mitad
        TgolesST += goles_segunda_mitad

        goles_equipo1.append(goles)
        corner_equipo1.append(corner)

    for partidosN in partidos_equipo2:
        partido = partidos_equipo2[partidosN]
        goles = partido['goles_totales']
        corner = partido['Tiros de esquina']
        remates_arco = partido['Remates al arco']
        remates = partido['Remates']
        tarjetas_amarillas = partido['Tarjetas amarillas']
        faltas = partido['Faltas']
        pases = partido['Pases']
        goles_primera_mitad = partido['goles_primera_mitad']
        goles_segunda_mitad = partido['goles_segunda_mitad']

        # Sumar estadísticas
        Tgoles2 += goles
        Tcorner2 += corner
        TrematesAr2 += remates_arco
        Tremates2 += remates
        TtarjetasA2 += tarjetas_amarillas
        Tfaltas2 += faltas
        Tpases2 += pases
        TgolesPT2 += goles_primera_mitad
        TgolesST2 += goles_segunda_mitad

        goles_equipo2.append(goles)
        corner_equipo2.append(corner)

    # Promedios
    Mean = Tgoles / p if p != 0 else 0
    Mean2 = Tgoles2 / p if p != 0 else 0
    MeanC = Tcorner / p if p != 0 else 0
    MeanC2 = Tcorner2 / p if p != 0 else 0

    # Desviación estándar y rangos
    if p != 0:
        Ds = math.sqrt(sum([(x - Mean) ** 2 for x in goles_equipo1]) / p)
        UVs, UVr = Mean + Ds, Mean - Ds
    else:
        UVs, UVr = Mean + 0, Mean - 0

    if p != 0:
        DsC = math.sqrt(sum([(x - MeanC) ** 2 for x in corner_equipo1]) / p)
        UVsC, UVrC = MeanC + DsC, MeanC - DsC
    else:
        UVsC, UVrC = MeanC + 0, MeanC - 0

    if p != 0:
        Ds2 = math.sqrt(sum([(x - Mean2) ** 2 for x in goles_equipo2]) / p)
        UVs2, UVr2 = Mean2 + Ds2, Mean2 - Ds2
    else:
        UVs2, UVr2 = Mean2 + 0, Mean2 - 0

    if p != 0:
        DsC2 = math.sqrt(sum([(x - MeanC2) ** 2 for x in corner_equipo2]) / p)
        UVsC2, UVrC2 = MeanC2 + DsC2, MeanC2 - DsC2
    else:
        UVsC2, UVrC2 = MeanC2 + 0, MeanC2 - 0
    # Imprimir los resultados
    print(f"{'-' * 40} DATOS DEL {equipo1} {'-' * 40}")
    
    Pcorner = (Tcorner / p) - 1
    print(f"{equipo1}: Cantidad de tiros de esquina esperados >> {Pcorner:.2f}")
    print(f"Rango de la desviación estándar de corners: {UVrC:.2f} ---- {MeanC:.2f} ---- {UVsC:.2f}")
    
    Pgoles = (Tgoles / p) - 1
    print(f"{equipo1}: Cantidad de goles esperados >> {Pgoles:.2f}")
    print(f"Rango de la desviación estándar de goles: {UVr:.2f} ---- {Mean:.2f} ---- {UVs:.2f}")
    
    Pgoles_aciertos = (Tgoles * 100) / TrematesAr
    print(f"{equipo1}: Probabilidad de aciertos en remates >> {Pgoles_aciertos:.2f}%")
    print(f"Probabilidad de fallar >> {100 - Pgoles_aciertos:.2f}%")
    
    Premates = (TrematesAr * 100) / Tremates
    print(f"{equipo1}: Porcentaje de balones al arco >> {Premates:.2f}%")
    print(f"Porcentaje de balones fuera del arco >> {100 - Premates:.2f}%")
    
    PtarjetasA = (TtarjetasA * 100) / Tfaltas
    print(f"{equipo1}: Probabilidad de recibir tarjetas amarillas >> {PtarjetasA:.2f}%")
    
    PposesionB = (Tpases * 100) / (Tpases + Tpases2)
    print(f"{equipo1}: Promedio de posesión del balón >> {PposesionB:.2f}%")
    
    PgolesPT = (TgolesPT / p) - 1
    print(f"{equipo1}: Goles esperados en la primera mitad >> {PgolesPT:.2f}")
    
    PgolesST = (TgolesST / p) - 1
    print(f"{equipo1}: Goles esperados en la segunda mitad >> {PgolesST:.2f}")
    
    print(f"{'-' * 40} DATOS DEL {equipo2} {'-' * 40}")
    
    Pcorner2 = (Tcorner2 / p) - 1
    print(f"{equipo2}: Cantidad de tiros de esquina esperados >> {Pcorner2:.2f}")
    print(f"Rango de la desviación estándar de corners: {UVrC2:.2f} ---- {MeanC2:.2f} ---- {UVsC2:.2f}")
    
    Pgoles2 = (Tgoles2 / p) - 1
    print(f"{equipo2}: Cantidad de goles esperados >> {Pgoles2:.2f}")
    print(f"Rango de la desviación estándar de goles: {UVr2:.2f} ---- {Mean2:.2f} ---- {UVs2:.2f}")
    
    Pgoles2_aciertos = (Tgoles2 * 100) / TrematesAr2
    print(f"{equipo2}: Probabilidad de aciertos en remates >> {Pgoles2_aciertos:.2f}%")
    print(f"Probabilidad de fallar >> {100 - Pgoles2_aciertos:.2f}%")
    
    Premates2 = (TrematesAr2 * 100) / Tremates2
    print(f"{equipo2}: Porcentaje de balones al arco >> {Premates2:.2f}%")
    print(f"Porcentaje de balones fuera del arco >> {100 - Premates2:.2f}%")
    
    PtarjetasA2 = (TtarjetasA2 * 100) / Tfaltas2
    print(f"{equipo2}: Probabilidad de recibir tarjetas amarillas >> {PtarjetasA2:.2f}%")
    
    PposesionB2 = (Tpases2 * 100) / (Tpases + Tpases2)
    print(f"{equipo2}: Promedio de posesión del balón >> {PposesionB2:.2f}%")
    
    PgolesPT2 = (TgolesPT2 / p) - 1
    print(f"{equipo2}: Goles esperados en la primera mitad >> {PgolesPT2:.2f}")
    
    PgolesST2 = (TgolesST2 / p) - 1
    print(f"{equipo2}: Goles esperados en la segunda mitad >> {PgolesST2:.2f}")

# 1. Convertir el diccionario de stats a DataFrame
def convertir_a_dataframe(stats):
    datos = []
    for equipo, partidos in stats.items():
        for partido, estadisticas in partidos.items():
            fila = {'Equipo': equipo, 'Partido': partido}
            fila.update(estadisticas)
            datos.append(fila)
    
    df = pd.DataFrame(datos)
    return df

df_stats = convertir_a_dataframe(stats)

# 2. Preparar los datos para el modelo
# Seleccionamos las columnas con estadísticas y el objetivo
X = df_stats[['Remates', 'Remates al arco', 'Pases', 'Faltas', 'Tarjetas amarillas', 'Tarjetas rojas', 'Tiros de esquina', 'goles_primera_mitad', 'goles_segunda_mitad', 'goles_totales']]
y = df_stats['gano']

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Escalar los datos (es importante hacerlo después de la división del conjunto de datos)
X_train_scaled = X_train
X_test_scaled = X_test

# Entrenar el modelo de regresión logística con más iteraciones
modelo = LogisticRegression(solver='lbfgs', max_iter=20)  # Incrementa el valor de max_iter a 1000
modelo.fit(X_train_scaled, y_train)

# Hacer predicciones
y_pred = modelo.predict(X_test_scaled)

# 5. Evaluar el modelo
precision = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {precision * 100:.2f}%")

# Mostrar las predicciones
print("Predicciones:", y_pred)

#--------------------------------------Predecir si ganara con datos de un partido que ya ocurrio
# Predecir si ganará el próximo partido (usando nuevas estadísticas)
# Inicializar diccionarios para almacenar las estadísticas agregadas
estadisticas_equipo1 = {
    'Remates': 0,
    'Remates al arco': 0,
    'Pases': 0,
    'Faltas': 0,
    'Tarjetas amarillas': 0,
    'Tarjetas rojas': 0,
    'Tiros de esquina': 0,
    'goles_primera_mitad': 0,
    'goles_segunda_mitad': 0,
    'goles_totales': 0
}

estadisticas_equipo2 = {
    'Remates': 0,
    'Remates al arco': 0,
    'Pases': 0,
    'Faltas': 0,
    'Tarjetas amarillas': 0,
    'Tarjetas rojas': 0,
    'Tiros de esquina': 0,
    'goles_primera_mitad': 0,
    'goles_segunda_mitad': 0,
    'goles_totales': 0
}

equipo1, equipo2 = list(stats.keys())
# Calcular estadísticas para el equipo 1
for partido, stats_partido in stats[equipo1].items():
    estadisticas_equipo1['Remates'] += stats_partido['Remates']
    estadisticas_equipo1['Remates al arco'] += stats_partido['Remates al arco']
    estadisticas_equipo1['Pases'] += stats_partido['Pases']
    estadisticas_equipo1['Faltas'] += stats_partido['Faltas']
    estadisticas_equipo1['Tarjetas amarillas'] += stats_partido['Tarjetas amarillas']
    estadisticas_equipo1['Tarjetas rojas'] += stats_partido['Tarjetas rojas']
    estadisticas_equipo1['Tiros de esquina'] += stats_partido['Tiros de esquina']
    estadisticas_equipo1['goles_primera_mitad'] += stats_partido['goles_primera_mitad']
    estadisticas_equipo1['goles_segunda_mitad'] += stats_partido['goles_segunda_mitad']
    estadisticas_equipo1['goles_totales'] += stats_partido['goles_totales']

# Calcular estadísticas para el equipo 2
for partido, stats_partido in stats[equipo2].items():
    estadisticas_equipo2['Remates'] += stats_partido['Remates']
    estadisticas_equipo2['Remates al arco'] += stats_partido['Remates al arco']
    estadisticas_equipo2['Pases'] += stats_partido['Pases']
    estadisticas_equipo2['Faltas'] += stats_partido['Faltas']
    estadisticas_equipo2['Tarjetas amarillas'] += stats_partido['Tarjetas amarillas']
    estadisticas_equipo2['Tarjetas rojas'] += stats_partido['Tarjetas rojas']
    estadisticas_equipo2['Tiros de esquina'] += stats_partido['Tiros de esquina']
    estadisticas_equipo2['goles_primera_mitad'] += stats_partido['goles_primera_mitad']
    estadisticas_equipo2['goles_segunda_mitad'] += stats_partido['goles_segunda_mitad']
    estadisticas_equipo2['goles_totales'] += stats_partido['goles_totales']

#Imprime probabilidad estadisticas de solo los primeros 6 partidos
calcular_desviacion_estandar_y_datos(stats)

# Función para calcular promedio ponderado
def weighted_average(values, weights):
    return sum(v * w for v, w in zip(values, weights)) / sum(weights)

# Asignar pesos más altos a partidos recientes
pesos = [1.5, 1.3, 1.1, 0.9, 0.7, 0.5]  # Puedes ajustar según cuántos partidos quieras considerar

# Promedios ponderados para las estadísticas
estadisticas_equipo1['Remates'] = weighted_average(
    [stats_partido['Remates'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Remates al arco'] = weighted_average(
    [stats_partido['Remates al arco'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Pases'] = weighted_average(
    [stats_partido['Pases'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Faltas'] = weighted_average(
    [stats_partido['Faltas'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Tarjetas amarillas'] = weighted_average(
    [stats_partido['Tarjetas amarillas'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Tarjetas rojas'] = weighted_average(
    [stats_partido['Tarjetas rojas'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['Tiros de esquina'] = weighted_average(
    [stats_partido['Tiros de esquina'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['goles_primera_mitad'] = weighted_average(
    [stats_partido['goles_primera_mitad'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['goles_segunda_mitad'] = weighted_average(
    [stats_partido['goles_segunda_mitad'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo1['goles_totales'] = weighted_average(
    [stats_partido['goles_totales'] for stats_partido in stats[equipo1].values()],
    pesos
)

# Repetir para el equipo 2
estadisticas_equipo2['Remates'] = weighted_average(
    [stats_partido['Remates'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Remates al arco'] = weighted_average(
    [stats_partido['Remates al arco'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Pases'] = weighted_average(
    [stats_partido['Pases'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Faltas'] = weighted_average(
    [stats_partido['Faltas'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Tarjetas amarillas'] = weighted_average(
    [stats_partido['Tarjetas amarillas'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Tarjetas rojas'] = weighted_average(
    [stats_partido['Tarjetas rojas'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['Tiros de esquina'] = weighted_average(
    [stats_partido['Tiros de esquina'] for stats_partido in stats[equipo2].values()],
    pesos
)
estadisticas_equipo2['goles_primera_mitad'] = weighted_average(
    [stats_partido['goles_primera_mitad'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo2['goles_segunda_mitad'] = weighted_average(
    [stats_partido['goles_segunda_mitad'] for stats_partido in stats[equipo1].values()],
    pesos
)
estadisticas_equipo2['goles_totales'] = weighted_average(
    [stats_partido['goles_totales'] for stats_partido in stats[equipo1].values()],
    pesos
)

#COMIENZO DEL DATAFRAME
estadisticas_equipo1_df = pd.DataFrame([estadisticas_equipo1])
estadisticas_equipo2_df = pd.DataFrame([estadisticas_equipo2])

print("\n-----------------PREDICCIONES-----------------")
# Obtener probabilidades de la predicción para el equipo 1
probabilidades = modelo.predict_proba(estadisticas_equipo1_df)[0]

# Obtener probabilidades de la predicción para el equipo 2
probabilidades2 = modelo.predict_proba(estadisticas_equipo2_df)[0]

# Imprimir las probabilidades de ganar y perder para el equipo 1
print(f"Probabilidades para {equipo1}:")
print(f"  Ganar: {probabilidades[1] * 100:.2f}%")
print(f"  Perder: {probabilidades[0] * 100:.2f}%")

# Imprimir las probabilidades de ganar y perder para el equipo 2
print(f"Probabilidades para {equipo2}:")
print(f"  Ganar: {probabilidades2[1] * 100:.2f}%")
print(f"  Perder: {probabilidades2[0] * 100:.2f}%")
#--------------------------------------Predecir si ganara con datos de un partido que ya ocurrio