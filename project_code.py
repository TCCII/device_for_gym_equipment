import speech_recognition as sr
import wiringpi
from wiringpi import GPIO
from time import sleep

flag = True

wiringpi.wiringPiSetup()

class Tr():
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
    
    def faster(self):
        if self.frequency == 0:
            self.start()
        
        else:
            self.frequency += self.delta_freq
            self.frequency = min(self.frequency, self.max_frequency)
            wiringpi.softToneWrite(self.faster_gpio, self.frequency)
    
    def slower(self):
        if self.frequency > 0:
            self.frequency -= self.delta_freq
            self.frequency = max(self.frequency, 0) 
            wiringpi.softToneWrite(self.faster_gpio, self.frequency)
    
    def start(self):
        wiringpi.digitalWrite(self.start_gpio, GPIO.HIGH)
        sleep(1)
        wiringpi.digitalWrite(self.start_gpio, GPIO.LOW)
        if self.frequency == 0:
            self.frequency = self.delta_freq
            wiringpi.softToneWrite(self.faster_gpio, self.frequency)
    
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
    r = sr.Recognizer()
    speech = sr.Microphone(2)
    with speech as source:
        # Speech recognition using Google Speech Recognition
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit = 10)
        
        try:
            print("Diga o comando para a 'esteira': \n")
            ans = r.recognize_google(audio, language = 'en-US')
        
        except sr.UnknownValueError:
            print("O Google Speech Recognition não conseguiu entender o áudio")
        
        except sr.RequestError as e:
            print("Não foi possível solicitar resultados do serviço Google Speech Recognition; {0}".format(e))

        if audio:
            if ans == 'start':
                print("Você disse: ", ans)
                tr.start()

            elif ans == 'faster':
                print("Você disse: ", ans)
                tr.faster()

            elif ans == 'slower':
                print("Você disse: ", ans)
                tr.slower()

            elif ans == 'stop':
                print("Você disse: ", ans)
                tr.stop()
                break