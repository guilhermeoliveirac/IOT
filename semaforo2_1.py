import RPi.GPIO as GPIO
from time import sleep
from threading import Thread 
from sr55 import discoVoador

# Defina os números dos pinos GPIO para os LEDs e botões
VERMELHO_SEMAFORO = 17
AMARELO_SEMAFORO = 18
VERDE_SEMAFORO = 27
VERMELHO_PEDESTRE = 23
VERDE_PEDESTRE = 24
BOTAO_PEDESTRE = 22

# Configurar a numeração dos pinos GPIO
GPIO.setmode(GPIO.BCM)

# Configurar os pinos como saída para os LEDs do semáforo e da faixa de pedestres
GPIO.setup(VERMELHO_SEMAFORO, GPIO.OUT)
GPIO.setup(AMARELO_SEMAFORO, GPIO.OUT)
GPIO.setup(VERDE_SEMAFORO, GPIO.OUT)
GPIO.setup(VERMELHO_PEDESTRE, GPIO.OUT)
GPIO.setup(VERDE_PEDESTRE, GPIO.OUT)

# Configurar o pino do botão de pedestre como entrada com pull-up interno
GPIO.setup(BOTAO_PEDESTRE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class Tempo_semaforo:
    geladeira = "verde"

def semaforo_verde():
    GPIO.output(VERMELHO_SEMAFORO, GPIO.LOW)
    GPIO.output(AMARELO_SEMAFORO, GPIO.LOW)
    GPIO.output(VERDE_SEMAFORO, GPIO.HIGH)

def semaforo_amarelo():
    GPIO.output(VERMELHO_SEMAFORO, GPIO.LOW)
    GPIO.output(AMARELO_SEMAFORO, GPIO.HIGH)
    GPIO.output(VERDE_SEMAFORO, GPIO.LOW)
    
def semaforo_vermelho():
    GPIO.output(VERMELHO_SEMAFORO, GPIO.HIGH)
    GPIO.output(AMARELO_SEMAFORO, GPIO.LOW)
    GPIO.output(VERDE_SEMAFORO, GPIO.LOW)

def pedestre_verde():
    GPIO.output(VERMELHO_PEDESTRE, GPIO.LOW)
    GPIO.output(VERDE_PEDESTRE, GPIO.HIGH)
    
def pedestre_vermelho():
    GPIO.output(VERMELHO_PEDESTRE, GPIO.HIGH)
    GPIO.output(VERDE_PEDESTRE, GPIO.LOW)
    
tempo = Tempo_semaforo()

def muda_estado():
    while True:
        tempo.geladeira = "verde"
        print("verde")
        sleep(10)
        tempo.geladeira = "amarelo"
        print("ämarelo")
        sleep(1)
        tempo.geladeira = "vermelho"
        print("vermelho")
        sleep(10)



def semaforo():
    tread = Thread(target=muda_estado)
    estado_pedestre = "ESPERANDO"
    try:
        tread.start()
        while True:
            print(tempo.geladeira)
            distancia = discoVoador()
            print(distancia)
            if GPIO.input(BOTAO_PEDESTRE) == GPIO.LOW or distancia >= 10:
            
                if(tempo.geladeira == "vermelho"):
                    pedestre_verde()
                    sleep(10)
                    pedestre_vermelho()
                else:
                    semaforo_amarelo()
                    sleep(2)
                    semaforo_vermelho()
                    pedestre_verde()
                    sleep(10)
                    pedestre_vermelho()
                    semaforo_verde()
                # Verificar se o botão de pedestre foi pressionado
                
            if tempo.geladeira == "verde":
                semaforo_verde()
                pedestre_vermelho()
            elif tempo.geladeira == "amarelo":
                semaforo_amarelo()
                
            elif tempo.geladeira == "vermelho":
                semaforo_vermelho()
                pedestre_verde()

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    semaforo()
