import datetime
import subprocess
import banco_de_dados
import telepot
import time
from telepot.loop import MessageLoop
from gtts import gTTS
import speech_recognition as sr


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
        if mensagem == '/audio':
            audio = gTTS('Eu amo voce', lang='pt')
            audio.save(str(chat_id) + ".mp3")
            bot.sendAudio(chat_id, audio=open(str(chat_id) + ".mp3", 'rb'))
        if mensagem == '/adicionarcatalogo':
            bot.sendMessage(chat_id, 'Envie uma foto e um nome juntos')

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

        for i in lista_nome:

            if ("/SetBrilho" + str(i)) in mensagem:
                brilho = str(mensagem)
                brilho = brilho.replace("/SetBrilho" + str(i), "")
                brilho = brilho.replace(" ", "")
                banco_de_dados.adicionar_brilho_plantas(str(chat_id), brilho, i)

            if ("/SetAgua" + str(i)) in mensagem:
                agua = str(mensagem)
                agua = agua.replace("/SetAgua" + str(i), "")
                agua = agua.replace(" ", "")
                banco_de_dados.adicionar_agua_plantas(str(chat_id), agua, i)

            if ("/SetSol" + str(i)) in mensagem:
                sol = str(mensagem)
                sol = sol.replace("/SetSol" + str(i), "")
                sol = sol.replace(" ", "")
                banco_de_dados.adicionar_sol_plantas(str(chat_id), sol, i)

            if ("/SetFlor" + str(i)) in mensagem:
                flor = str(mensagem)
                flor = flor.replace("/SetFlor" + str(i), "")
                flor = flor.replace(" ", "")
                banco_de_dados.adicionar_flor_plantas(str(chat_id), flor, i)

            if ("/SetObs" + str(i)) in mensagem:
                obs = str(mensagem)
                obs = obs.replace("/SetObs" + str(i), "")
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
                e = 0
                a = 0
                for planta in fotos:
                    for o in obs_:
                        e += 1
                        if o == ";":
                            print(e)
                            print(a)
                            if a < e:
                                print(" A " + obs_[a:e])
                            else:
                                print(" A " + obs_[e:a])
                            a = e
                            e = 0


                    bot.sendPhoto(chat_id, planta,
                                  "Planta: {} \n Brilho: {} \n Água: {} \n Sol: {} \n Flor: {} \n\n Observações: \n {} \n\n Data de Modificação: {}/{}/{}"
                                  .format(nome_, brilho_, agua_, sol_, flor_, obs_, dia, mes, ano))
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
        bot.sendMessage(chat_id, transcrito)


bot = telepot.Bot("1004906066:AAGaB9AOgstBB2hN8R-nfK4uLJxpsOawR4o")
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')


def troca_variavel(dados):
    variavel = str(dados)
    variavel = variavel.replace("[", "")
    variavel = variavel.replace("]", "")
    variavel = variavel.replace("'", "")
    variavel = variavel.replace(" ", "")
    return variavel


while 1:
    time.sleep(10)
