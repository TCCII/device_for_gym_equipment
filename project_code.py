import speech_recognition as sr # biblioteca que faz o reocnhecimento de fala
import wiringpi # biblioteca que possibilita o uso dos pinos GPIO
from wiringpi import GPIO
from time import sleep # biblioteca de variáveis de tempo

flag = True

wiringpi.wiringPiSetup()

class Tr():
    # variáveis para frequência,frequência máxima, pinos de GPIO para o LED 
    frequency = 1
    delta_freq = 1
    max_frequency = 5
    faster_gpio = 5
    start_gpio = 10
    stop_gpio = 9
    

    def __init__(self):
        wiringpi.pinMode(self.start_gpio, GPIO.OUTPUT)
        wiringpi.pinMode(self.stop_gpio, GPIO.OUTPUT)
        wiringpi.softToneCreate(self.faster_gpio)
    
    # função para acelerar a simulação do equipamento de ginástica
    def faster(self):
        if self.frequency == 0:
            self.start()
        
        else:
            self.frequency += self.delta_freq
            self.frequency = min(self.frequency, self.max_frequency)
            wiringpi.softToneWrite(self.faster_gpio, self.frequency)
    
    # função para desacelerar a simulação do equipamento de ginástica
    def slower(self):
        if self.frequency > 0:
            self.frequency -= self.delta_freq
            self.frequency = max(self.frequency, 0) 
            wiringpi.softToneWrite(self.faster_gpio, self.frequency)
    
    # função para iniciar a simulação do equipamento de ginástica
    def start(self):
        wiringpi.digitalWrite(self.start_gpio, GPIO.HIGH)
        sleep(1)
        wiringpi.digitalWrite(self.start_gpio, GPIO.LOW)
        if self.frequency == 0:
            self.frequency = self.delta_freq
            wiringpi.softToneWrite(self.faster_gpio, self.frequency)
    
    # função para parar a simulação do equipamento de ginástica
    def stop(self):
        while (self.frequency > self.delta_freq):
            self.frequency -= self.delta_freq
            self.frequency = max(self.frequency, 0)
            wiringpi.softToneWrite(self.stop_gpio, self.frequency)
            sleep(1)
        wiringpi.softToneStop(self.faster_gpio)
        wiringpi.digitalWrite(self.stop_gpio, GPIO.HIGH)
        sleep(1)
        wiringpi.digitalWrite(self.stop_gpio, GPIO.LOW)

    def exit(self):
        self.stop()
        

tr = Tr()

while(flag):
    '''
    O objetivo principal de uma instância do Recognizer é, 
    obviamente, reconhecer a fala. Cada instância vem com 
    uma variedade de configurações e funcionalidades para 
    reconhecer a fala de uma fonte de áudio.
    '''
    r = sr.Recognizer()

    # Usa o microfone padrão como fonte de áudio
    speech = sr.Microphone(2)
    with speech as source:
        '''
        O método adjust_for_ambient_noise() lê o primeiro
        segundo do fluxo de arquivo e calibra o reconhecedor 
        para o nível de ruído do áudio.
        '''
        r.adjust_for_ambient_noise(source)

        '''
        Ouve a primeira frase e extraia-a em dados de áudio, 
        phrase_time_limit define quanto tempo de fala par os 
        comandos
        '''
        audio = r.listen(source, phrase_time_limit = 10)
        
        try:
            print("Diga o comando para a 'esteira': \n")
            
            # reconhecer a fala usando o Google Speech Recognition
            ans = r.recognize_google(audio, language = 'en-US')
        
        # a fala é ininteligível
        except sr.UnknownValueError:
            print("O Google Speech Recognition não conseguiu entender o áudio")
        
        except sr.RequestError as e:
            print("Não foi possível solicitar resultados do serviço Google Speech Recognition; {0}".format(e))

        if audio:
            if ans == 'start':
                print("Você disse: ", ans)
                # comando GPIO
                tr.start()

            elif ans == 'faster':
                print("Você disse: ", ans)
                # comando GPIO
                tr.faster()

            elif ans == 'slower':
                print("Você disse: ", ans)
                # comando GPIO
                tr.slower()

            elif ans == 'stop':
                print("Você disse: ", ans)
                # comando GPIO
                tr.stop()
                break
