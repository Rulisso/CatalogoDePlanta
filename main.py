import datetime
import subprocess
import banco_de_dados
import telepot
import time
from telepot.loop import MessageLoop
from gtts import gTTS
import speech_recognition as sr
import threading as tr

def handle(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)
    nome = msg['from']['first_name']
    banco_de_dados.carrega_id(str(chat_id), nome)
    banco_de_dados.adicionar_table_foto(str(chat_id))
    banco_de_dados.adicionar_table_audio(str(chat_id))
    banco_de_dados.adicionar_table_planta(str(chat_id))

    print(msg)
    print(content_type, chat_type, chat_id)
    r = sr.Recognizer()
    if content_type == 'text':
        mensagem = msg['text']
        if mensagem == "/start":
            bot.sendMessage(chat_id, "  Olá, {}, serei seu catalogo de planta.\nComigo, você poderá: \n1- catalogar suas plantas por seus nomes; \n2- informar quanto de agua precisa na semana; \n3- tempo de sol por dia; \n4- seu vigor; \n5- se possui floração;  \n6 - adicionar varias observações sobre cada uma.\n Além disso, é possível acompanhar, por meio das fotos, o crescimento e desenvolvimento de cada planta registrada.".format(nome))
        if mensagem == '/audio':
            audio = gTTS('Eu amo voce', lang='pt')
            audio.save(str(chat_id) + ".mp3")
            bot.sendAudio(chat_id, audio=open(str(chat_id) + ".mp3", 'rb'))
        if mensagem == '/adicionarcatalogo':
            bot.sendMessage(chat_id, 'Envie a foto de sua planta e um nome junto')
        if mensagem == "/comandos":
            bot.sendMessage(chat_id, "/MandaFoto + (nome da planta cadastrada por você). Por exemplo se a planta foi cadastrada como violeta: /MandaFotoVioleta. "
                                     "\n\n /MandaNome: lista todas duas plantas catalogadas"
                                     "\n\n /DefBrilho + (nome da planta cadastrada por você)+ um número de 0 a 10. Por exemplo se a planta foi cadastrada como violeta: \n'/DefBrilhoVioleta 10', ou seja, seu brilho ou vigor está em seu máximo"
                                     "\n\n /DefAgua + (nome da planta cadastrada por você)+ um número de 0 a 10. Por exemplo se a planta foi cadastrada como violeta: \n'/DefAguaVioleta 3', ou seja, precisa de pouca água"
                                     "\n\n /DefSol + (nome da planta cadastrada por você)+ um número de 0 a 10. Por exemplo se a planta foi cadastrada como violeta: \n'/DefSolVioleta 6', ou seja, de uma quantidade mediana de sol por dia"
                                     "\n\n /DefFlor + (nome da planta cadastrada por você)+ sim ou nao. Por exemplo se a planta foi cadastrada como violeta: \n'/DefFlorVioleta sim', ou seja, essa planta possui floração"
                                     "\n\n /DefObs + (nome da planta cadastrada por você)+ sua observação. Por exemplo se a planta foi cadastrada como violeta: \n'/DefObsVioleta Sua flor é de cor violeta', ou seja, será definido para a violeta a observação de ter flor cor violeta, porém pode-se adicionar quantas observações for preciso"
                                     "\n\n /Info + (nome da planta cadastrada por você). Por exemplo se a planta foi cadastrada como violeta: \n'/InfoVioleta', será enviada as fotos cadastradas com o nome violeta e suas definições e observações")

        if "/MandaFoto" in mensagem:
            planta = str(mensagem)
            planta = planta.replace("/MandaFoto", "")
            planta = planta.replace(" ", "")
            fotos = banco_de_dados.verifica_foto(str(chat_id), planta)
            for planta in fotos:
                bot.sendPhoto(chat_id, planta)

        if mensagem == "/MandaNome":
            lista_nome = banco_de_dados.carrega_foto_nome(str(chat_id))
            id_da_foto = banco_de_dados.carrega_foto_id(str(chat_id))
            for i in range(len(lista_nome)):
                bot.sendMessage(chat_id, str(id_da_foto[i]) + " " + str(lista_nome[i]))
        lista_nome = banco_de_dados.carrega_foto_nome(str(chat_id))
        cont = 0
        for i in lista_nome:
            cont += 1
            if ("/DefBrilho" + str(i)) in mensagem:
                brilho = str(mensagem)
                brilho = brilho.replace("/DefBrilho" + str(i), "")
                brilho = brilho.replace(" ", "")
                banco_de_dados.adicionar_brilho_plantas(str(chat_id), brilho, i)

            if ("/DefAgua" + str(i)) in mensagem:
                agua = str(mensagem)
                agua = agua.replace("/DefAgua" + str(i), "")
                agua = agua.replace(" ", "")
                banco_de_dados.adicionar_agua_plantas(str(chat_id), agua, i)

            if ("/DefSol" + str(i)) in mensagem:
                sol = str(mensagem)
                sol = sol.replace("/DefSol" + str(i), "")
                sol = sol.replace(" ", "")
                banco_de_dados.adicionar_sol_plantas(str(chat_id), sol, i)

            if ("/DefFlor" + str(i)) in mensagem:
                flor = str(mensagem)
                flor = flor.replace("/DefFlor" + str(i), "")
                flor = flor.replace(" ", "")
                print(flor)
                banco_de_dados.adicionar_flor_plantas(str(chat_id), flor, i)

            if ("/DefObs" + str(i)) in mensagem:
                obs = str(mensagem)
                obs = obs.replace("/DefObs" + str(i), "")
                print(obs)

                observ_ = str(banco_de_dados.verifica_obs(str(chat_id), str(i)))
                observ_ = observ_.replace("[", "")
                observ_ = observ_.replace("]", "")
                observ_ = observ_.replace("'", "")
                banco_de_dados.adicionar_Mais_Obs_plantas(str(chat_id), obs + "; " + str(observ_), i)


            if ("/Info" + str(i)) in mensagem:
                info = str(mensagem)
                info = info.replace("/Info", "")
                info = info.replace(" ", "")
                infos = banco_de_dados.verifica_info_planta(str(chat_id), info)
                print(infos)

                nome_ = troca_variavel(str(infos[0]))
                brilho_ = troca_variavel(str(infos[1]))
                agua_ = troca_variavel(str(infos[2]))
                sol_ = troca_variavel(str(infos[3]))
                flor_ = troca_variavel(str(infos[4]))

                obs_ = str(infos[5])
                obs_ = obs_.replace("None", "")
                obs_ = obs_.replace("[", "")
                obs_ = obs_.replace("]", "")
                obs_ = obs_.replace("'", "")

                data_ = troca_variavel(str(infos[6]))
                ano = data_[0:4]
                mes = data_[5:7]
                dia = data_[8:10]
                fotos = banco_de_dados.verifica_foto(str(chat_id), i)
                print(fotos)
                id_no_banco = banco_de_dados.carrega_foto_id(str(chat_id))
                c = 0
                for fotos in id_no_banco:
                    print(fotos)
                    carrega = str(banco_de_dados.carrega_foto_pelo_id(str(chat_id), fotos, info))
                    carrega = carrega.replace("[", "")
                    carrega = carrega.replace("]", "")
                    carrega = carrega.replace("'", "")
                    carrega = carrega.replace(" ", "")
                    print(carrega)
                    if carrega != "":
                        print(c)
                        bot.sendPhoto(chat_id, carrega,
                                      "Planta: {} \nBrilho: {} \nÁgua: {} \nSol: {} \nFlor: {} \n\nObservações: \n {} \n\nData de Adição: {}/{}/{}"
                                      .format(nome_, brilho_, agua_, sol_, flor_, obs_, dia, mes, ano))
                if cont >= 1:
                    break
                print(ano)
                print(mes)
                print(dia)
    if content_type == 'photo':
        foto = msg['photo'][1]['file_id']
        legenda = msg['caption']
        banco_de_dados.adicionar_foto(str(chat_id), foto, legenda)
        banco_de_dados.adicionar_info_plantas(str(chat_id), legenda, str(datetime.datetime.now()))

    if content_type == 'voice':
        file_id = msg['voice']['file_id']
        banco_de_dados.adicionar_audio(str(chat_id), file_id)
        arquivo = open("./" + str(chat_id) + ".mp3", 'wb')
        bot.download_file(file_id, arquivo)
        time.sleep(3)
        subprocess.call(['ffmpeg', '-i', ("./" + str(chat_id) + ".mp3"), ("./" + str(chat_id) + ".wav")])
        with sr.AudioFile("./" + str(chat_id) + ".wav") as source:
            audio = r.record(source)
            transcrito = r.recognize_google(audio, language="pt-BR")
            print(transcrito)


def troca_variavel(dados):
    variavel = str(dados)
    variavel = variavel.replace("[", "")
    variavel = variavel.replace("]", "")
    variavel = variavel.replace("'", "")
    variavel = variavel.replace(" ", "")
    return variavel

#bot = telepot.Bot("1004906066:AAGaB9AOgstBB2hN8R-nfK4uLJxpsOawR4o")

TOKEN = "1004906066:AAGaB9AOgstBB2hN8R-nfK4uLJxpsOawR4o"
bot = telepot.Bot(TOKEN)
MessageLoop(bot,handle).run_as_thread()

while True:
    time.sleep(10)
print('Listening ...')

