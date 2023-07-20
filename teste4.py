import requests
import json
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import sqlite3

lista_id_cadernos, lista_quantidade_questao = list(), list()
urls = list()
contador = 0

questao_salva = 0
lista_com_questoes = []

# Verificação de erro
def verificar_request(response):
    """
    Verifica se o status code e diferente de 200 e aplica um time
    sleep || Contabiliza o total de requisições (variavel: contador),
    apos N requisições ele aplica um time sleep
    """

    global contador
    if response.status_code != 200:
        print(f'Erro: {response.status_code}\n{response.text}')
        print('Aguarde 3 minutos para restaurar!')
        save_responses_to_json(lista_com_questoes)
        sleep(180)
        lista_com_questoes.clear()
        return True
    else:
        contador += 1
        if contador >= 100:
            print(f'Requisições: {contador}, esperar 180s')
            contador = 0
            save_responses_to_json(lista_com_questoes)
            sleep(180)
            lista_com_questoes.clear()


# Restaurar questões
def restaurar(id, index_um, index_dois):
    global questao_salva
    """
    Refazer apenas os indices que deram erro na verificação (def verificar_request()),
    caso de erro, ele vai continuar a verificar e refazer até da certo
    """
    print('Restaurando')
    cookies = {
        'aws-waf-token': '2504a6ad-e97e-4e0f-909d-6f728e360d6a:EAoAvbamXUcJAAAA:1Wq5LP+kBCQk7LhFIPZNuLSCoaocIMwyJHnlLUl7FzEC/Ij+OmEs4LRiXWZvR8wwR036nycPbKqpjkOkldL4eKzlO6S89A1Wnuzo9VmlU9321RHvjNj/nt6k9N9fq1fHQ9bxOhLTZvBjmkcFFObbuyVvN0fFbE6w59/9Y1Tz9B2d6uw4GawBc5AhqWdlUCoPALoul2Mfn5wygIfQ7OO8NpRMzWSQNEjaUdb3YIwJMWwDybKwMAhlmrwGQKUbiFdMMWmuVyjZ+/Nu',
        'TecPermanecerLogado': 'MzM0NzAsYWZyYW5pb191bmlmZWlAeWFob28uY29tLmJyLCQyYSQxMiRxbWtBQUU3clVabm9xbzJkZkNqWFUud1J4SlRpVTU1MVN3UjZTSVdzM21XWHMvL1RSa1NibQ==',
        'JSESSIONID': 'B68BFFC8F356D577C1ACDD6FEC8709B6', '_gat_UA-32462178-1': '1',
        '_ga': 'GA1.1.796737532.1689422658',
        'AWSALB': 'eSooXXdc3pJay21ayhyOwocHdrHv+8TS/cz7Pc6kX0wy69ZbFnru6aKrrMSnJqV1q8pkus1/hWBNivv9AlDtfCboJoN7vL87Wna6O3QZMCsquU4JA6Ojo8DBkA6eKP2VnlWpixH9OVLNQ8xdx2voqp/5oqC0KWtWLjTF795oem4jkAVmMkTQcs7LvwCTbA==',
        'AWSALBCORS': 'eSooXXdc3pJay21ayhyOwocHdrHv+8TS/cz7Pc6kX0wy69ZbFnru6aKrrMSnJqV1q8pkus1/hWBNivv9AlDtfCboJoN7vL87Wna6O3QZMCsquU4JA6Ojo8DBkA6eKP2VnlWpixH9OVLNQ8xdx2voqp/5oqC0KWtWLjTF795oem4jkAVmMkTQcs7LvwCTbA==', }

    headers = {
        'authority': 'www.tecconcursos.com.br', 'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'origin': 'https://www.tecconcursos.com.br',
        'referer': 'https://www.tecconcursos.com.br/questoes/cadernos/experimental/32374710/imprimir',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"', 'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest', }

    data = {
        'configuracoes.idCadernoQuestoes': f'{id}', 'configuracoes.idTeoriaModulo': '',
        'configuracoes.idTeoriaAssunto': '',
        'configuracoes.questaoInicial': f'{index_um}', 'configuracoes.numeroQuestoes': f'{index_dois}',
        'configuracoes.removerQuestoes': 'NENHUMA', }
    response = requests.post(
        f'https://www.tecconcursos.com.br/questoes/cadernos/experimental/{id}/ajaxCarregarQuestoesImpressao',
        cookies=cookies, headers=headers, data=data, )
    if verificar_request(response):
        restaurar(id, index_um, index_dois)  # caso de erro novamente
    else:
        response = json.loads(response.content.decode())
        lista_com_questoes.append(response)


# Aplica Thread para puxar todos id de todos os cadernos
def puxar_thread_caderno():
    global urls
    for i in puxar_dados_pasta():  # percorro em cada id de pasta.
        urls.append(i)
    print(len(urls))

    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(puxar_id_caderno, urls)


# Puxa id das pastas
def puxar_dados_pasta():
    """
    puxo todos id de cada pasta
    """
    lista_id = list()
    cookies = {
        '_fbp': 'fb.2.1689422657801.55388152',
        '_gcl_au': '1.1.1995680729.1689422658',
        '_gid': 'GA1.3.2080611932.1689594068',
        'TecPermanecerLogado': 'MzM0NzAsYWZyYW5pb191bmlmZWlAeWFob28uY29tLmJyLCQyYSQxMiRxbWtBQUU3clVabm9xbzJkZkNqWFUud1J4SlRpVTU1MVN3UjZTSVdzM21XWHMvL1RSa1NibQ==',
        'JSESSIONID': '806AD3418CC314C5B1ED96A908E5D233',
        'aws-waf-token': 'e5d6f015-ba09-4cc5-a682-629c3bda067f:EAoAmyVkR04BAAAA:XBp5y9WzxIs3FLhy9R5npEuiNvZI54TxMfA0mqJp9wo8yqKYPkVzPzu8W+Mvnr2V9hOKt7ienuu56S3jJM4AV/H3VoCQvdSQnV/y+PCeYHJuKOiGtE1qVlLyMm2WeyEnt25RHwCggYtpPd1VKysJEXr1JEjSq6c+zVoam9aEI623KSv1F60NQjAS4f1cRHoIZh2CnTUPoBiMbRzmoYzXDb4y4rLelu+kZdu3+ilXjKDMHkQgR5D6V8fzCSQZzYZIgxA4DxkwlQVE',
        '_gat_UA-32462178-1': '1',
        '_uetsid': 'd1c3c760249611ee9240ab93a9b4b672',
        '_uetvid': 'b9ba4db0230711ee8d0a9b95a1e8f42f',
        'AWSALB': 'vztm6ByHU6W7H8Gt0FeZGXE8b8bsvepdkZSAi8DlSgkRs9A7yQL+h1alSdRzErKyaF0tGtK8hkolQIubTgUF+AsJWNeBorAtiqq5gP06ly60M476xxOeWwFZArJWhxad8GwnMftcE9FDBgDBz55Ukscjf0uNVWAacf/XxkEA4fMErHjO+BcdjJbbEmyo8w==',
        'AWSALBCORS': 'vztm6ByHU6W7H8Gt0FeZGXE8b8bsvepdkZSAi8DlSgkRs9A7yQL+h1alSdRzErKyaF0tGtK8hkolQIubTgUF+AsJWNeBorAtiqq5gP06ly60M476xxOeWwFZArJWhxad8GwnMftcE9FDBgDBz55Ukscjf0uNVWAacf/XxkEA4fMErHjO+BcdjJbbEmyo8w==',
        '_ga': 'GA1.1.796737532.1689422658',
        '_ga_1LNYCM2MLB': 'GS1.1.1689856593.20.1.1689862795.40.0.0',
        '_ga_X9T694QY0S': 'GS1.3.1689856610.19.1.1689862796.0.0.0',}

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Logado': 'true',
        'Connection': 'keep-alive',
        'Referer': 'https://www.tecconcursos.com.br/questoes/pastas'
    }
    response = requests.get('https://www.tecconcursos.com.br/api/pastas-cadernos/', cookies=cookies, headers=headers)
    verificar_request(response)
    response = json.loads(response.content)
    for i in response['pastas']:  # percorre por cada pasta extraindo as informações
        lista_id.append(i['id'])
    return lista_id


# Puxa o id de cada caderno
def puxar_id_caderno(id):
    """
    Puxa id do caderno, para puxar todos de uma vez, usamos threads (puxar_thread_caderno()),
    como e uma quantidade menor (<3k) não sobrecarrega o servidor,
    e sera feito apenas uma vez no script
    """
    global lista_id_cadernos, lista_quantidade_questao
    cookies = {
        'TecPermanecerLogado': 'MzM0NzAsYWZyYW5pb191bmlmZWlAeWFob28uY29tLmJyLCQyYSQxMiRxbWtBQUU3clVabm9xbzJkZkNqWFUud1J4SlRpVTU1MVN3UjZTSVdzM21XWHMvL1RSa1NibQ==',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Logado': 'true',
        'Referer': f'https://www.tecconcursos.com.br/questoes/pastas/{id}',
    }

    response = requests.get(
        f'https://www.tecconcursos.com.br/api/pastas-cadernos/{id}/itens', cookies=cookies, headers=headers
    )
    verificar_request(response)

    response = json.loads(response.content)
    for i in response['itens']:
        lista_id_cadernos.append(i['id'])
        lista_quantidade_questao.append(i['quantidadeItens'])


# Puxa as questões
def puxar_questoes(id, quantidade_questoes):
    global lista_id_cadernos, questao_salva
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
            'aws-waf-token': '2504a6ad-e97e-4e0f-909d-6f728e360d6a:EAoAvbamXUcJAAAA:1Wq5LP+kBCQk7LhFIPZNuLSCoaocIMwyJHnlLUl7FzEC/Ij+OmEs4LRiXWZvR8wwR036nycPbKqpjkOkldL4eKzlO6S89A1Wnuzo9VmlU9321RHvjNj/nt6k9N9fq1fHQ9bxOhLTZvBjmkcFFObbuyVvN0fFbE6w59/9Y1Tz9B2d6uw4GawBc5AhqWdlUCoPALoul2Mfn5wygIfQ7OO8NpRMzWSQNEjaUdb3YIwJMWwDybKwMAhlmrwGQKUbiFdMMWmuVyjZ+/Nu',
            'TecPermanecerLogado': 'MzM0NzAsYWZyYW5pb191bmlmZWlAeWFob28uY29tLmJyLCQyYSQxMiRxbWtBQUU3clVabm9xbzJkZkNqWFUud1J4SlRpVTU1MVN3UjZTSVdzM21XWHMvL1RSa1NibQ==',
            'JSESSIONID': 'B68BFFC8F356D577C1ACDD6FEC8709B6', '_gat_UA-32462178-1': '1',
            '_ga': 'GA1.1.796737532.1689422658',
            'AWSALB': 'eSooXXdc3pJay21ayhyOwocHdrHv+8TS/cz7Pc6kX0wy69ZbFnru6aKrrMSnJqV1q8pkus1/hWBNivv9AlDtfCboJoN7vL87Wna6O3QZMCsquU4JA6Ojo8DBkA6eKP2VnlWpixH9OVLNQ8xdx2voqp/5oqC0KWtWLjTF795oem4jkAVmMkTQcs7LvwCTbA==',
            'AWSALBCORS': 'eSooXXdc3pJay21ayhyOwocHdrHv+8TS/cz7Pc6kX0wy69ZbFnru6aKrrMSnJqV1q8pkus1/hWBNivv9AlDtfCboJoN7vL87Wna6O3QZMCsquU4JA6Ojo8DBkA6eKP2VnlWpixH9OVLNQ8xdx2voqp/5oqC0KWtWLjTF795oem4jkAVmMkTQcs7LvwCTbA==', }

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
        response = requests.post(
            f'https://www.tecconcursos.com.br/questoes/cadernos/experimental/{id}/ajaxCarregarQuestoesImpressao',
            cookies=cookies, headers=headers, data=data, )
        if verificar_request(response):
            restaurar(id, i[0], i[-1])
        else:
            response = json.loads(response.content.decode())
            lista_com_questoes.append(response)



def save_responses_to_json(response_list):
    for item in response_list:
        with open('questoes.json', 'w') as f:
            json.dump(item, f, indent=4)







puxar_thread_caderno()

"""
Com as duas listas montadas (id(caderno), quantidade_questão(numero de questão em cada caderno) )
percorremos os dois e puxamos as questões
"""
for id in lista_id_cadernos:
    for qtd in lista_quantidade_questao:
        puxar_questoes(id, int(qtd))