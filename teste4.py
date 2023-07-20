import requests
import json
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import sqlite3

lista_id_cadernos, lista_quantidade_questao = list(), list()
urls = list()
questoes = []


def puxar_thread_caderno():
    global urls
    for i in puxar_dados_pasta():
        urls.append(i)

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(puxar_id_caderno, urls)


def puxar_thread_questoes():
    global lista_id_cadernos, lista_quantidade_questao

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(puxar_questoes, lista_id_cadernos, lista_quantidade_questao)


# Puxa id das pastas
def puxar_dados_pasta():
    lista_id = list()
    cookies = {
        'TecPermanecerLogado': 'MzM0NzAsYWZyYW5pb191bmlmZWlAeWFob28uY29tLmJyLCQyYSQxMiRxbWtBQUU3clVabm9xbzJkZkNqWFUud1J4SlRpVTU1MVN3UjZTSVdzM21XWHMvL1RSa1NibQ==',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Logado': 'true',
        'Connection': 'keep-alive',
        'Referer': 'https://www.tecconcursos.com.br/questoes/pastas'
    }
    while True:
        response = requests.get('https://www.tecconcursos.com.br/api/pastas-cadernos/', cookies=cookies,
                                headers=headers)
        if response.status_code != 200:
            print(f'Erro: {response.status_code}\n{response.text}')
            sleep(180)
        else:
            break

    response = json.loads(response.content)
    for i in response['pastas']:  # percorre por cada pasta extraindo as informações
        lista_id.append(i['id'])
    return lista_id


# Puxa o id de cada caderno
def puxar_id_caderno(id):
    global lista_id_cadernos, lista_quantidade_questao
    cookies = {
        '_fbp': 'fb.2.1689422657801.55388152',
        '_gcl_au': '1.1.1995680729.1689422658',
        '_gid': 'GA1.3.2080611932.1689594068',
        'TecPermanecerLogado': 'MzM0NzAsYWZyYW5pb191bmlmZWlAeWFob28uY29tLmJyLCQyYSQxMiRxbWtBQUU3clVabm9xbzJkZkNqWFUud1J4SlRpVTU1MVN3UjZTSVdzM21XWHMvL1RSa1NibQ==',
        'JSESSIONID': 'CE657E57A5093298CFADE4750A3E02F6',
        'aws-waf-token': 'e5d6f015-ba09-4cc5-a682-629c3bda067f:EAoAi9wJJJQJAAAA:ujyP+s+nNpyVJR9C7Tf9K8fWAhCv+RPBmYUjN4vfUxwgkJBLfBUg4k1RFwVmcHrzXpokSCfsHtHr5g8K8HEkS3rb061Nss5mtn63toOIe8ilM70JNMDFOZpHwTo/H+nPLobCzh/FWFaGakL4DXTY0f5h7CC8G9zXMIPnPWeBD5I6VNB9btuhwghFxnb6q4mKKxwioNpyR5yEIpRLGyryFGFYlGDnY3s3kWPARrfr5VuAELTbhsyxp9//ExTeqKfMcv//wPQuWqY0',
        '_gat_UA-32462178-1': '1',
        '_uetsid': 'd1c3c760249611ee9240ab93a9b4b672',
        '_uetvid': 'b9ba4db0230711ee8d0a9b95a1e8f42f',
        'AWSALB': 'dpBBci7hK/mmx514WryyJyXlx2AklaDkHVgtPsyh1UTGrLvkKzhaTdqM1WcJtsVhhxLwotGKm4nKtGEQmis15CH4x7IOtwaPS3fJA8HL1Lb3T2DHq3nvp+JjOolk360usa4uZBH/PvhMQVHCRrvOyj+q8HCH3sTJTb+0mp8Ih5dKTxyCGMe7VwMalENe5w==',
        'AWSALBCORS': 'dpBBci7hK/mmx514WryyJyXlx2AklaDkHVgtPsyh1UTGrLvkKzhaTdqM1WcJtsVhhxLwotGKm4nKtGEQmis15CH4x7IOtwaPS3fJA8HL1Lb3T2DHq3nvp+JjOolk360usa4uZBH/PvhMQVHCRrvOyj+q8HCH3sTJTb+0mp8Ih5dKTxyCGMe7VwMalENe5w==',
        '_ga': 'GA1.1.796737532.1689422658',
        '_ga_1LNYCM2MLB': 'GS1.1.1689815566.18.1.1689816958.8.0.0',
        '_ga_X9T694QY0S': 'GS1.3.1689815584.17.1.1689816958.0.0.0',
    }

    headers = {
        'authority': 'www.tecconcursos.com.br',
        'accept': 'application/json, text/plain, * / *',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'if-modified-since': 'Mon, 26 Jul 1997 05:00:00 GMT',
        'logado': 'true',
        'pragma': 'no-cache',
        'Referer': f'https://www.tecconcursos.com.br/questoes/pastas/{id}',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    while True:
        response = requests.get(
            f'https://www.tecconcursos.com.br/api/pastas-cadernos/{id}/itens', cookies=cookies, headers=headers
        )
        if response.status_code != 200:
            print(f'Erro: {response.status_code}\n{response.text}')
            sleep(180)
        else:
            break

    response = json.loads(response.content)
    for i in response['itens']:
        lista_id_cadernos.append(i['id'])
        lista_quantidade_questao.append(i['quantidadeItens'])


# Puxa as questões
def puxar_questoes(id, quantidade_questoes):
    global lista_id_cadernos, questoes
    n = quantidade_questoes
    # Divido os numeros, para obter as questões iniciais e finais
    tamanho = 200
    num_listas, resto = divmod(n, tamanho)
    listas = []
    for i in range(num_listas):
        inicio = i * tamanho + 1
        fim = inicio + tamanho - 1
        lista = list(range(inicio, fim + 1))
        listas.append(lista)
    if resto > 0:
        inicio = num_listas * tamanho + 1
        fim = inicio + resto - 1
        lista = list(range(inicio, fim + 1))
        listas.append(lista)
    # dentro do for percorro as requisições usando os numeros de questões
    for i in listas:
        cookies = {
            '_fbp': 'fb.2.1689422657801.55388152',
            '_gcl_au': '1.1.1995680729.1689422658',
            '_gid': 'GA1.3.2080611932.1689594068',
            'TecPermanecerLogado': 'MzM0NzAsYWZyYW5pb191bmlmZWlAeWFob28uY29tLmJyLCQyYSQxMiRxbWtBQUU3clVabm9xbzJkZkNqWFUud1J4SlRpVTU1MVN3UjZTSVdzM21XWHMvL1RSa1NibQ==',
            'JSESSIONID': 'CE657E57A5093298CFADE4750A3E02F6',
            'aws-waf-token': 'e5d6f015-ba09-4cc5-a682-629c3bda067f:EAoAto8JHIEAAAAA:c9vZfwL9dOaTrbpRY/FaGX5IPgkY3xklXa2v1PCJeYVtKgffDJum/Ue7Vfg1GCEbnZBOmF5tpZXnE/Ua1lPxACIs2i/GWb6FilQUq9tjKaj9kxTwX89vGL8QLaP2tt0wmFJSe1xCotzNklxoTMnkLyXdUui5k6hDccALEMnw+09Wm/zo7aa7+Ajv2yS4pMT8vjV5c/p+YCSv9eNz6cqYn8/2vAfn9tPiWGxNl/htTEIarB3+ZypnYgri1WRrGyfCO107Z7QiIv+C',
            '_gat_UA-32462178-1': '1',
            '_uetsid': 'd1c3c760249611ee9240ab93a9b4b672',
            '_uetvid': 'b9ba4db0230711ee8d0a9b95a1e8f42f',
            '_ga_X9T694QY0S': 'GS1.3.1689815584.17.1.1689815978.0.0.0',
            'AWSALB': 'FQ721DoAi5/MR/iJF9OrDvEbqhcEqWzTy3MMO5yzU6CbaMs86ul3g0bXdn2lj8rhckz7ORU/vj72naiqMbUSDaBc+Mfele1RDCMAHXf65nxZ3CTK6bPqn5WvnMprSTIAx06j+lGQnRdkod75JCdJTg5H5zBMwP7CM1b+vK9Ka2raRSD3MVL3VqGj6YSuXA==',
            'AWSALBCORS': 'FQ721DoAi5/MR/iJF9OrDvEbqhcEqWzTy3MMO5yzU6CbaMs86ul3g0bXdn2lj8rhckz7ORU/vj72naiqMbUSDaBc+Mfele1RDCMAHXf65nxZ3CTK6bPqn5WvnMprSTIAx06j+lGQnRdkod75JCdJTg5H5zBMwP7CM1b+vK9Ka2raRSD3MVL3VqGj6YSuXA==',
            '_ga': 'GA1.1.796737532.1689422658',
            '_ga_1LNYCM2MLB': 'GS1.1.1689815566.18.1.1689815988.45.0.0',
        }

        headers = {
            'authority': 'www.tecconcursos.com.br', 'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.tecconcursos.com.br',
            'referer': 'https://www.tecconcursos.com.br/questoes/cadernos/experimental/32374710/imprimir',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"', 'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest', }

        data = {
            'configuracoes.idCadernoQuestoes': f'{id}', 'configuracoes.idTeoriaModulo': '',
            'configuracoes.idTeoriaAssunto': '',
            'configuracoes.questaoInicial': f'{i[0]}', 'configuracoes.numeroQuestoes': f'{i[-1]}',
            'configuracoes.removerQuestoes': 'NENHUMA', }
        while True:
            response = requests.post(
                f'https://www.tecconcursos.com.br/questoes/cadernos/experimental/{id}/ajaxCarregarQuestoesImpressao',
                cookies=cookies, headers=headers, data=data)
            if response.status_code != 200:
                print(f'Erro: {response.status_code}\n{response.text}')
                sleep(180)
            else:
                break
        response = json.loads(response.content)
        for i in response['list']:
            questoes.append(i)

        sleep(180)


puxar_thread_caderno()
sleep(180)  # aguarda 180 segundo, zerando o tempo dos works
print('aguardando 180 segundos iniciais!')
puxar_thread_questoes()


def inserir_dados(questoes):
    # Cria uma conexão com o banco de dados SQLite
    conn = sqlite3.connect('dados.db')

    # Cria um cursor
    cursor = conn.cursor()

    # Insere os registros da lista `questoes` na tabela `banco_de_dados`, mesmo se o ID já existir
    cursor.executemany('''
        INSERT OR IGNORE INTO banco_de_dados (id, questao_completa)
        VALUES (?, ?)
        ''', [(item['idQuestao'], json.dumps(item)) for item in questoes])

    # Salva as alterações no banco de dados
    conn.commit()

    # Fecha a conexão com o banco de dados
    conn.close()


print('inserindo questoes')
inserir_dados(questoes)
print(f'Questoes inseridas: {len(questoes)}')