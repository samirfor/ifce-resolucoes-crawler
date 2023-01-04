# ifce-resolucoes-crawler
Robô para fazer download das resoluções do site https://ifce.edu.br/instituto/documentos-institucionais/resolucoes/

# Como rodar
```bash
# instale o scrapy
python -m venv .venv
source ./venv/bin/activate
pip install scrapy
cd ifce_resolucoes
scrapy crawl resolucoes
```
