import speech_recognition as sr 
import pyttsx3, pywhatkit       #Libreria para configuracion del microfono y la voz
from datetime import datetime   #Libreria para consultar el tiempo, la fecha y la hora
import wikipedia        #Libreria para extraer informacion de wikpedia
import keyboard
from pygame import mixer     
import os 
import subprocess as sub    #Libreria para ejecutar subprocesos 
from pytube import YouTube #libreria para descargar videos de youtube
import tkinter as tk

name = "juan"
nombre = "Francisco"
#configuracion de la voz

listener = sr.Recognizer()
engine = pyttsx3.init()

voice = engine.getProperty('voice')
engine.setProperty('voice', voice[0])


#Diccionario para el reconocimiento de paginas web
sites={
    'google': 'google.com',
    'youtube': 'youtube.com',
    'facebook': 'facebook.com',
    'instagram': 'instagram.com',
    'x': 'twitter.com',
    'wikipedia': 'es.wikipedia.org'
    
}

#diccionario para el reconocimiento de archivos
archivo ={
    'carta': 'juan.pdf',    
    'video': 'sigueme.mp4',
    'audio': 'nombre_usuario.txt'

}   

def hablar(text):
    engine.say(text)
    engine.runAndWait()

hablar("Asistente activado, En qu puedo ayudar te el dia d hoy?")

#Configuracion del microfono
def listen():
    rec = ""  # Asignar un valor predeterminado a la variable rec
    try:
        with sr.Microphone() as source:
            print("Escucho...")            
            pc = listener.listen(source)
            rec = listener.recognize_google(pc)
            rec = rec.lower()

            if name is rec:
                rec = rec.replace(name, '')

    except:
        pass 
    return rec 


#comandos 
def run_juan():
    while True: 
        rec = listen()

        if 'hola' in rec:
            hablar(f'Hola {nombre} en que puedo ayudarte?')

        elif 'especificaciones' in rec:
            hablar("Soy un asistente virtual, programado en el codigo de programacion Pyton, por el estudiante de Ingenieria de sistemas, Francisco Silva")


        elif 'capacidades' in rec:
            hablar("A partir de comandos de voz puedo, decir la hora y fecha actual, abrir sitios wed, abrir archivos, reproducir musica y descargar videos de youtube...Aunque son todas mis capacidades, en el futuro se espera una mayor implementacion de herramientas")

        
        #reproducir musica en yutu
        elif 'reproduce' in rec:
            music = rec.replace('reproduce', '')    #Reemplazamos lo que decimos al microfono con solo el nombre del video
            hablar("Reproduciendo "+ music) 
            pywhatkit.playonyt(music)   #Extrae lo dicho en la variable "music" para buscar y reproducir


        #Comando para descargar videos de youtube
        elif 'descargar un video' in rec:

            hablar("Ingresa el Link del video")

            def cerrar():
                video_url = entrada.get()

                try:
                    yt = YouTube(video_url)
                    video = yt.streams.get_highest_resolution()
                    video.download()
                    print("Video Descargado")
                    hablar("El Video ha sido descargado con éxito")

                except Exception as e:
                    print("Error en descarga")
                    hablar("Error en la descarga...verifique que el video no tenga restricción de edad")

                ventana.destroy()

            ventana = tk.Tk()
            ventana.title("Descargar Video")
            
            # Establecer la ventana emergente como la principal
            ventana.attributes('-topmost', True)

            # Ajustar el tamaño de la ventana
            ventana.geometry("400x200")  # Anchura x Altura

            etiqueta = tk.Label(ventana, text="Ingrese el Link del Video:")
            etiqueta.pack()

            entrada = tk.Entry(ventana)
            entrada.pack()

            boton = tk.Button(ventana, text="Aceptar", command=cerrar)
            boton.pack()

            ventana.mainloop()


        #Comando para decir la hora actual
        elif 'hora' in rec:
            hora_actual = datetime.now().strftime('%H:%M')  #Extraemos la hora con la libreria datetime

           #Verificamos en que momento del dia estamos para geenerar el saludo 
            if hora_actual < datetime.strptime('12:00:00', '%H:%M:%S').strftime('%H:%M'):
                hablar(f'Buenos días...son las {hora_actual} de la mañana')
                        
            elif hora_actual < datetime.strptime('18:00:00', '%H:%M:%S').strftime('%H:%M'):                
                hablar(f'Buenas tardes...son las {hora_actual} de la tarde')

            else:
                hablar(f'Buenas noches...son las {hora_actual} de la noche')


        #Comando para decir la fecha actual
        elif 'fecha' in rec:
            fecha_actual = datetime.now()   #Extraemos la fecha actual con la libreria datetime

            # creamos un diccionario para verificar el nombre del mes en español
            nombres_meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
            nombre_mes = nombres_meses[fecha_actual.month - 1]

            print(f'Estamos en el mes de {nombre_mes}')
            hablar(f'la fecha actual es {fecha_actual.day} de {nombre_mes} del {fecha_actual.year}')


        #buscar alguna consulta en wikipedia
        elif 'busca' in rec:
            search = rec.replace('buscar', '')  #Toma lo dicho en para guardar lo en la variable
            wikipedia.set_lang("es")    #ingresamos en wikipedia en español
            try:
                wiki = wikipedia.summary(search, 1)     #tomamos el primer resultado junto con el primer parrafo
                print(search + ": " + wiki) 
                hablar(wiki)
            except wikipedia.exceptions.PageError:
                print("No se encontró un resultado para la búsqueda.")
                hablar("No se encontró un resultado para la búsqueda.")
            except wikipedia.exceptions.DisambiguationError:
                print("La búsqueda es ambigua. Por favor, proporciona más detalles.")
                hablar("La búsqueda es ambigua. Por favor, proporciona más detalles.")
                

        #cerrar programa
        elif 'apagar' in rec:
            hablar("Apagando")
            break   #Cerramos el buble cerrando asi el programa


        #Abrir un archivo
        elif 'archivo' in rec:
            for  files in archivo:     #A partir de decir el comando tendremos que decir que queremos abrir
                if files in rec:    
                    sub.Popen([archivo[files]], shell=True) #Se abre el archivo pedido
                    hablar(f'Abrindo {files}')


        #abrir paginas web
        elif 'open' or 'abrir' in rec:
            for site in sites:
                if site in rec:     #Luego de decir que queremos abrir un sitio, deberemos decir que pagina queremos abrir
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)     #Aqui se abre el sitio 
                    print(site)
                    hablar(f'Abriendo{site}')
        
        
        #Escribir notas
        elif 'escribe' in rec:
            hablar("Hola")
            for files in archivo:
                try:
                    with open ("nota.txt",'a') as f:
                        write(f)
                
                except FileNotFoundError as e:
                    files = open("nota.txt",'w')
                    write(files)



                    
def write(f):
    
    hablar("Que deseas que escriba?")
    rec_escribir = listen()
    f.write(rec_escribir + os.linesep)
    f.close()
    hablar("Documento finalizado")
    sub.Popen("nota.txt",shell=True)  


        
if __name__ == '__main__':
    run_juan()



        
        