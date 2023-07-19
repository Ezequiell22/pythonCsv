import csv
import chardet
import re

caminho_arquivo = 'relatorio.csv'
caminho_arquivo_salvar = 'relatorio_processado.csv'

with open(caminho_arquivo, 'rb') as f:
    result = chardet.detect(f.read())
    encoding = result['encoding']

print(encoding)


def reset_values():
    quantidade = ''
    taxa = ''
    nro_lcto = ''
    vlrAquisicao = 0
    vlrResidual = 0
    vlrEncargos = 0
    vlrQuotaMensal = 0
    encargo = ''


quantidade = ''
taxa = ''
nro_lcto = ''
vlrAquisicao = 0
vlrResidual = 0
vlrEncargos = 0
vlrQuotaMensal = 0
encargo = ''
conta_contabil = ''
filial = ''

vlrTotAquisicao = 0
vlrTotResidual = 0
vlrTotEncargos = 0
vlrTotQuotaMensal = 0

total = False
newArray = []
newLine = ['filial', 'conta_contabil', 'nro_lcto', 'quantidade', 'taxa',
           'vlrAquisicao', 'vlrEncargos', 'vlrQuotaMensal', 'vlrResidual',  'encargo']
newArray.append(newLine)


def isTotal(text):
    return text.find("Total") != -1


def getFilal(text):
    return re.findall(r'\d+', text.split('-')[0])[0]


def getIndex(splitLine, columnSearch):
    valueInd = -1

    for index, coluna in enumerate(splitLine):
        if columnSearch in coluna:
            valueInd = index
            break

    return valueInd


def strToFloat(text):
    value = text.replace(".", "").replace(",", ".")
    return float(value)


# Lê o arquivo CSV e armazena as linhas na lista
with open(caminho_arquivo, newline='', encoding=encoding) as arquivo:

    for linha in arquivo:
        linha = linha.replace('"', '').replace('\r\n', '')
        if linha.strip() != '':
            if linha.find("Total") != -1:
                total = True

            # atribui filial
            if "Filial 00" in linha and not "*** Total Filial" in linha:
                filial = getFilal(linha)

            if "Conta Contábil" in linha and not linha.find("Total") != -1:
                conta_contabil = linha

            splitLine = linha.split(';')
            indexQuantidade = getIndex(splitLine, "Quantidade....")
            indexTaxa = getIndex(splitLine, "Taxa......")

            if indexQuantidade != -1:
                quantidade = splitLine[indexQuantidade+1]

            if indexTaxa != -1:
                taxa = splitLine[indexTaxa+1]

            if not total:
                indexVlrAquisicao = getIndex(splitLine, "Valor Aquisi")
                indexVlrEncargos = getIndex(splitLine, "Encargo Acumul")
                indexQuotaMensal = getIndex(splitLine, "Quota Mensal.")
                indexVlrResidual = getIndex(splitLine, "Valor Residual")
                indexEncargo = getIndex(splitLine, "Encargo.")

                if indexVlrAquisicao != -1:
                    vlrAquisicao = strToFloat(splitLine[indexVlrAquisicao +
                                                        1])

                    vlrTotAquisicao = float(
                        vlrTotAquisicao) + vlrAquisicao

                if indexVlrEncargos != -1:
                    vlrEncargos = strToFloat(splitLine[indexVlrEncargos +
                                                       1])
                    vlrTotEncargos = float(
                        vlrTotEncargos) + vlrEncargos

                if indexQuotaMensal != -1:
                    vlrQuotaMensal = strToFloat(splitLine[indexQuotaMensal +
                                                          1])

                    vlrTotQuotaMensal = float(
                        vlrTotQuotaMensal) + vlrQuotaMensal

                if indexVlrResidual != -1:
                    vlrResidual = strToFloat(splitLine[indexVlrResidual +
                                                       1])

                    vlrTotResidual = float(
                        vlrTotResidual) + vlrResidual

                if indexEncargo != -1:
                    encargo = splitLine[indexEncargo+1]

            if " PAULO ROBERTO" not in linha and linha.split(';')[0].isdigit():

                if nro_lcto != '':
                    newArray.append(
                        [filial, conta_contabil, nro_lcto, quantidade, taxa, vlrAquisicao, vlrEncargos, vlrQuotaMensal, vlrResidual, encargo])
                    reset_values()
                    total = False

                nro_lcto = re.findall(r'\d+', linha.split(';')[0])[0]

# para ultima linha
newArray.append(
    [filial, conta_contabil, nro_lcto, quantidade, taxa, vlrAquisicao, vlrEncargos, vlrQuotaMensal, vlrResidual, encargo])

# totais
newArray.append(
    ['', '', '', '', '', vlrTotAquisicao, vlrTotEncargos, vlrTotQuotaMensal, vlrTotResidual, ''])


# # Salva o array em um arquivo CSV
with open(caminho_arquivo_salvar, 'w', newline='') as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv)
    escritor_csv.writerows(newArray)
