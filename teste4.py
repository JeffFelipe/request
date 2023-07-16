import requests
import json
from pprint import pprint

produtos = ['KIKA ARROZ PARBOLIZADO KG', 'ACUCAR TRITURADO ALEGRE 1KG', 'LEITE EM PO TGUINHO INTEGRAL',
            'CAFE SAO BRAZ 250GR FAMILIA ALMOFADA', 'ÓLEO DE SOJA LIZA 900ML', 'CAFÉ NODESTINO 250G',
            'FLOCAO SAO BRAZ 500G']

dados = []


def adicionar_dados(novos_dados):
    dados.extend(novos_dados)


caminho_arquivo = "dados.json"

def salvar_arquivo():
    with open(caminho_arquivo, "w") as arquivo:
        json.dump(dados, arquivo)


def verificar_paginas(produto):
    cookies = {
        '_gid': 'GA1.4.1431529164.1689459720',
        'cXwtVJnh0Hy': 'FECVGxe0e94vhoN',
        'session': 'eyJjc3JmX3Rva2VuIjoiZDlmZDRjY2M5ZmRlZGE3MWFjODFmYTJkYzQ3Yzc2NmJkMjk5N2U5ZCJ9.ZLMeeA.97lregbt-B1UC5EU-0mXpdOL_wE',
        '_gat_gtag_UA_139589857_1': '1',
        '_ga': 'GA1.1.1308585336.1689459720',
        'token': 'Q-udvXMhVfLl59UyWT0ZkdKIMhXoOqi9apfXHGBB6BfQ79afodwNVXEkZZ6GgAwAl4oK8WSUeVDpTFmCqovCDI_QdH8',
        '_ga_DZ91BBFHNC': 'GS1.1.1689467242.2.1.1689467267.0.0.0',
        '_ga_1S6B2LVB1Z': 'GS1.1.1689467242.2.1.1689467267.0.0.0',
    }

    headers = {
        'authority': 'precodahora.pb.gov.br',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_gid=GA1.4.1431529164.1689459720; cXwtVJnh0Hy=FECVGxe0e94vhoN; session=eyJjc3JmX3Rva2VuIjoiZDlmZDRjY2M5ZmRlZGE3MWFjODFmYTJkYzQ3Yzc2NmJkMjk5N2U5ZCJ9.ZLMeeA.97lregbt-B1UC5EU-0mXpdOL_wE; _gat_gtag_UA_139589857_1=1; _ga=GA1.1.1308585336.1689459720; token=Q-udvXMhVfLl59UyWT0ZkdKIMhXoOqi9apfXHGBB6BfQ79afodwNVXEkZZ6GgAwAl4oK8WSUeVDpTFmCqovCDI_QdH8; _ga_DZ91BBFHNC=GS1.1.1689467242.2.1.1689467267.0.0.0; _ga_1S6B2LVB1Z=GS1.1.1689467242.2.1.1689467267.0.0.0',
        'origin': 'https://precodahora.pb.gov.br',
        'referer': 'https://precodahora.pb.gov.br/produtos/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-authorization': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjE0ZWI4YTNiNjgzN2Y2MTU4ZWViNjA3NmU2YThjNDI4YTVmNjJhN2IiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9wcmVjb2RhaG9yYS01ZjllNSIsImF1ZCI6InByZWNvZGFob3JhLTVmOWU1IiwiYXV0aF90aW1lIjoxNjg5NDU5NzE5LCJ1c2VyX2lkIjoib3c0aWg4SmRpSWJFOE1WcWV4ZWdLdkVVTkJpMSIsInN1YiI6Im93NGloOEpkaUliRThNVnFleGVnS3ZFVU5CaTEiLCJpYXQiOjE2ODk0NjcyNDMsImV4cCI6MTY4OTQ3MDg0MywiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6e30sInNpZ25faW5fcHJvdmlkZXIiOiJhbm9ueW1vdXMifX0.TrfBpN9KLjnRf92nGrI0Ize3Ru0kJM_s2jndcvR6ktuuCdPSN5ofuvZmNVg2SGfI4gZUtqA4MwL-eUKBCCqP-twVYpI7T_no0sY7AMJiuGhc5QfmonPl7Miwib_a3SRJ0Euxzd3rm06H0QLgAEH_0CmmWQOS0LNSpW9krNjmsEqW1eW1YBSkCadoOGPGgXyCfGNJJynxpkNiOd_eLQYdVyKadQd4_2Xkjwj7W2BTEm7LXAT8hPbsbnc-4uir-TMH0UYDL0d0Pk2NBFsTDGEf5seMrfhsraIwGWdh3USku4cwFzn46WHXVm_dX12HteDjkeXR6XEegiAN_4KgXM6f1g',
        'x-csrftoken': 'ImQ5ZmQ0Y2NjOWZkZWRhNzFhYzgxZmEyZGM0N2M3NjZiZDI5OTdlOWQi.ZLM5gw.zUAM7Hfv6Qcg2FceC6WbnPJv_Bg',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'termo': produto,
        'gtin': '',
        'cnpj': '',
        'horas': '72',
        'anp': '',
        'municipio': '',
        'latitude': '-7.137405',
        'longitude': '-34.8484777',
        'raio': '15',
        'localizacao': 'Centro de JOÃO PESSOA',
        'precomax': '0',
        'precomin': '0',
        'pagina': '1',
        'ordenar': 'preco.asc',
        'categorias': '',
        'processo': 'carregar',
        'totalCategorias': '',
        'totalRegistros': '0',
        'totalPaginas': '1',
        'pageview': 'lista',
    }

    response = requests.post('https://precodahora.pb.gov.br/produtos/', cookies=cookies, headers=headers, data=data)
    print(response.status_code)
    response = json.loads(response.content)

    print(response.keys())
    try:
        total_paginas = response['totalPaginas']
        for i in range(1, total_paginas + 1):
            extrair_listas_de_produtos(produto, i)
    except KeyError:
        pprint(response)


def extrair_listas_de_produtos(produto, pagina):
    cookies = {
        '_gid': 'GA1.4.1431529164.1689459720',
        'cXwtVJnh0Hy': 'FECVGxe0e94vhoN',
        'session': 'eyJjc3JmX3Rva2VuIjoiZDlmZDRjY2M5ZmRlZGE3MWFjODFmYTJkYzQ3Yzc2NmJkMjk5N2U5ZCJ9.ZLMeeA.97lregbt-B1UC5EU-0mXpdOL_wE',
        '_gat_gtag_UA_139589857_1': '1',
        '_ga': 'GA1.1.1308585336.1689459720',
        'token': 'Ct4uXOgVeDbYWe-LP9ZZd_ug06vGx2sEGznFPKhT2nn6N0Y79XkUlZCNIJ7mcEY7twTdUtBSDLj7dk4fMg3Uwez65Zc',
        '_ga_DZ91BBFHNC': 'GS1.1.1689459719.1.1.1689463437.0.0.0',
        '_ga_1S6B2LVB1Z': 'GS1.1.1689459719.1.1.1689463437.0.0.0',
    }

    headers = {
        'authority': 'precodahora.pb.gov.br',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://precodahora.pb.gov.br',
        'referer': 'https://precodahora.pb.gov.br/produtos/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-authorization': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjE0ZWI4YTNiNjgzN2Y2MTU4ZWViNjA3NmU2YThjNDI4YTVmNjJhN2IiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9wcmVjb2RhaG9yYS01ZjllNSIsImF1ZCI6InByZWNvZGFob3JhLTVmOWU1IiwiYXV0aF90aW1lIjoxNjg5NDU5NzE5LCJ1c2VyX2lkIjoib3c0aWg4SmRpSWJFOE1WcWV4ZWdLdkVVTkJpMSIsInN1YiI6Im93NGloOEpkaUliRThNVnFleGVnS3ZFVU5CaTEiLCJpYXQiOjE2ODk0NjM0MDAsImV4cCI6MTY4OTQ2NzAwMCwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6e30sInNpZ25faW5fcHJvdmlkZXIiOiJhbm9ueW1vdXMifX0.ZysM1MyaQXfO1dmnkqfO3tZmHXioqYamtq5QnEXhya35HST051vTJHypUdtMdH00jcc3r1R7hNzI9AviTMjZ-idfHRJnuXeUHNmqcUlpRKJuc3-emPfyplNBoNZDn7ukgQA1-qeSRD9OpdH3K4Ts9FO82YOxm8nPvpQgmLBqUR3ShsAaLpBkV5hAfSgj5LPlvuoUpFuvndzXu8o9peZ7VHtJea2c4RdFf4mrtkHRA2XFr9JBq1WM5LlHaT19zLSD8QvTSj0qauFm70mfqAdCjcT8a05H8yJ35ov0NPzrfMZpb_WXU_OYRAh9q31sX2ZZEvVUfPPUdioArSYjFhvctQ',
        'x-csrftoken': 'ImQ5ZmQ0Y2NjOWZkZWRhNzFhYzgxZmEyZGM0N2M3NjZiZDI5OTdlOWQi.ZLMqjQ.k38JEGJqLGazh3b1lDMnlWaCcTk',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'termo': produto,
        'gtin': '',
        'cnpj': '',
        'horas': '72',
        'anp': '',
        'municipio': '',
        'latitude': '-7.137405',
        'longitude': '-34.8484777',
        'raio': '15',
        'localizacao': 'Centro de JOÃO PESSOA',
        'precomax': '0',
        'precomin': '0',
        'pagina': pagina,
        'ordenar': 'preco.asc',
        'categorias': '',
        'processo': 'carregar',
        'totalCategorias': '',
        'totalRegistros': '0',
        'totalPaginas': '1',
        'pageview': 'lista',
    }

    response = requests.post('https://precodahora.pb.gov.br/produtos/', cookies=cookies, headers=headers, data=data)
    response = json.loads(response.content)

    pprint(response)

    adicionar_dados(response)
    salvar_arquivo()


for item in produtos:
    verificar_paginas(item)