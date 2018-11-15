# https://oefbo.taglivros.com/admin/django_oef_models/assinaturaendereco/?q=&id=&endereco_recebedor__uf=SP&status_assinatura__exact=ATIVO&data_assinatura_start=&data_assinatura_end=&data_cancelamento_start=&data_cancelamento_end=
import io
import time

ARQUIVO_TRANSPORTADORA_CSV = 'abrangencia.csv'
ARQUIVO_CEP_CSV = 'ceps_para_analise.csv'
ARQUIO_RESULTADO = 'cep_por_transportadora.txt'
ARQUIVO_LOG = 'cep_por_transportadora_log.txt'


def _log(texto):
    log_text = open(ARQUIVO_LOG, 'w+')
    log_text.write('{}\n'.format(texto))
    log_text.close()
    print('{}\n'.format(texto))


def _gerar_arquivo_de_ceps(cep_por_transportadora):
    retorno = open(ARQUIO_RESULTADO, "a")
    retorno.write('{}\n'.format(cep_por_transportadora))
    retorno.close()


def _comparar_cep_transportadora(ceps):
    textfile = io.open(ARQUIVO_TRANSPORTADORA_CSV, 'rt', newline='', encoding='utf-8')
    linhas_transportadora = textfile.readlines()
    for indice_cep in range(1, len(ceps)):
        cep = ceps[indice_cep]
        cep_por_transportadora = cep.zfill(8)
        for indice_linha_transportadora in range(1, len(linhas_transportadora)):
            try:
                cep_transportadora = linhas_transportadora[indice_linha_transportadora].split(';')
                tokens = [token for token in cep_transportadora]
                metodo_envio = tokens[0]
                regiao = tokens[1]
                uf = tokens[2]
                cidade = tokens[3]
                praca = tokens[4]
                cep_inicial = tokens[5]
                cep_final = tokens[6]
                prazo = tokens[7]
                custo = tokens[8]
                if int(cep_inicial) <= int(ceps[indice_cep]) <= int(
                        cep_final) and metodo_envio not in cep_por_transportadora:
                    cep_por_transportadora += ("; {}".format(metodo_envio)
                                               + "; {}".format(regiao)
                                               + "; {}".format(uf)
                                               + "; {}".format(cidade)
                                               + "; {}".format(praca)
                                               + "; {}".format(prazo)
                                               + "; {}".format(custo)
                                               )
            except Exception as e:
                mensagem_erro = "Erro na linha {}; {}".format(indice_linha_transportadora, e)
                _log(mensagem_erro)
        _gerar_arquivo_de_ceps(cep_por_transportadora.replace('\n', '').replace('\r', ''))


def gerar():
    start_time = time.time()
    _log('Tag Livros - Ouro & Fino - Iniciando verificação de CEP por transportadora ')
    textfile = io.open(ARQUIVO_CEP_CSV, 'rt', newline='', encoding='utf-8')
    linhas_cep = textfile.readlines()
    _comparar_cep_transportadora(linhas_cep)
    elapsed_time = int(time.time() - start_time)
    minutos = elapsed_time // 60
    segundos = elapsed_time % 60
    _log("Tag Livros - Ouro & Fino - Finalizado")
    _log("timer:{}min{}seg".format(minutos, segundos))
    textfile.close()


return gerar()
