#librerias 'pip3 install nombre_libreria'
from tkinter import *
from tkinter import ttk
import datetime
from datetime import date
import time
from time import sleep
import pandas as pd
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import pyudev



#Aqui se crea la interfaz grafica
ventana = Tk()
frame = Frame()
frameL = Frame()
frameH = Frame()
ventana.title("INTERFAZ GRAFICA THERMO 42C")
#ventana.iconbitmap("logo.ico")
#ventana.wm_attributes("-fullscreen", True)
ventana.resizable(True,True)
ventana.geometry("2000x2000")
ventana.configure(bg="#9AECD5")

#-------------------------COMANDOS-----------------------------

#-----------------------SENSOR DTH21---------------------------
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4 #PIN DIGITAL DE LECTURA
def Sensor_DHT21():
	humedad, temperatura = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
	if humedad is not None and temperatura is not None:
		if humedad<100:
			global temperaturaF
			global humedadF
			temperaturaF= float('{:.3f}'.format(temperatura))
			temperaturaS=str(temperaturaF)+'°C'
			humedadF=float('{:.3f}'.format(humedad))
			humedadS=str(humedadF)+'%'
			temperaturaLabel.config(text=temperaturaS)
			humedadLabel.config(text=humedadS)
		else:
			print("Sensor failure. Check wiring.")
	ventana.after(60000,Sensor_DHT21)

#FUNCION PARA LEER DATOS ANALOGICOS DEL MCP3008
# Configuracion del Hardware SPI:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
#Variables iniciales de
NO=[1023,1023,1023,1023,1023]
NO2=[1023,1023,1023,1023,1023]
NOx=[1023,1023,1023,1023,1023]
estado=[1023,1023,1023,1023,1023]
fecha = [0,0,0,0,0]
hora=['00:00:00','00:00:00','00:00:00','00:00:00','00:00:00']
i=0
def lecturaAnalogica():
    global wb
    print('leyendo valores del MCP3008')
    #se establecen las variables para cada canal
    CH1= mcp.read_adc(0)
    CH2= mcp.read_adc(1)
    CH3= mcp.read_adc(2)
    CH4= mcp.read_adc(3)
    CH5= mcp.read_adc(4)
    CH6= mcp.read_adc(5)
    CH7= mcp.read_adc(6)
    CH8= mcp.read_adc(7)
    #Se guardan las variables en el archivo Excel
    today = date.today()
    now = time.strftime("%H:%M:%S")
    d1 = today.strftime("%d-%m-%Y")
    d1S=str(d1)
    nombre = str('./Datos'+d1+'.xlsx')
    writer = pd.ExcelWriter(nombre,engine='openpyxl')
    wb = writer.book
    fecha.append(d1S)
    hora.append(now)
    NO.append(str(CH1)+'-ppm')
    NO2.append(str(CH2)+'-ppm')
    NOx.append(str(CH3)+'-ppm')
    if CH4 > 700:
        CH4 = 'Alto'
    else:
        CH4 = 'Bajo'
    estado.append(CH4) 
    df = pd.DataFrame({'Fecha': fecha,'Hora': hora,'NO': NO,'NO2':NO2,'NOx': NOx,'ESTADO':estado})
    df.to_excel(writer,index=False)
    wb.save(nombre)
    #Se envian las variables a los labels
    NOW = [hora[-1],hora[-2],hora[-3],hora[-4],hora[-5]] 
    no = [NO[-1],NO[-2],NO[-3],NO[-4],NO[-5]]
    no2 = [NO2[-1],NO2[-2],NO2[-3],NO2[-4],NO2[-5]]
    nox = [NOx[-1],NOx[-2],NOx[-3],NOx[-4],NOx[-5]]
    es = [estado[-1],estado[-2],estado[-3],estado[-4],estado[-5]]
    NOLabel.config(text=no,wraplength=150)
    NO2Label.config(text=no2,wraplength=150)
    NOxLabel.config(text=nox,wraplength=150)
    ESTADOLabel.config(text=es, wraplength=150)
    horamuestraLabel.config(text=NOW,wraplength=200)

    ventana.after(60000,lecturaAnalogica)

#FUNCION PARA CREAR EL ARCHIVO EXCEL
def crearExcel():
    df = pd.DataFrame({'Fecha': [],
                       'Hora': [],
                       'NO': [],
                       'NO2': [],
                       'NOx': []})
    df = df[['Fecha', 'Hora', 'NO', 'NO2', 'NOx']]
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    nombre = str('./Datos'+d1+'.xlsx')
    df.to_excel(nombre, 'Hoja de datos', index=False)
    print('El archivo excel se creo')

#FUNCION PARA DETECTAR USB Y GUARDAR DATOS 
def guardarUSB():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')
    Led = 32
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Led,GPIO.OUT)
    GPIO.output(Led, GPIO.LOW) #poner la señal de salida en alto (High) o bajo (low)
    time.sleep(3)
    GPIO.cleanup() #limpiar el pin

    if devide.action == 'add':
        print('dispositivo usb conectado')
        wb.save(monitor)
        print('los datos se guardaron en la memoria USB')

def verExcel():
    print("abrir")

def leerExcel():
    df1 = pd.read_excel('example.xlsx',
                       skiprows=1,
                       names=['UID', 'First Name', 'Last Name', 'Age', 'Sales #1', 'Sales #2'])

#FUNCION PARA CERRAR LA VENTANA DE TKINTER
def cerrarVentana():
    pi_pwm.stop()
    ventana.destroy()

#FUNCION PARA ENVIAR Y RECIBIR DATOS POR MEDIO DE LA CONEXION RS232
def conexionRS232():
    print('dato enviado')
    señaltx.delete(0,'end')

#FUNCION PARA CALCULAR LAS VARIABLES ESTADISTICAS
def calcularEstadistica():
    print('se calcularon las variables estadisticas')
    

#-------------------PID Y SALIDA PWM---------------------------

#FUNCION PARA OBTENER LA SEÑAL DE CONTROL Y REALIZAR EL PID
PWMpin = 12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PWMpin,GPIO.OUT)
pi_pwm = GPIO.PWM(PWMpin,500)
pi_pwm.start(0)

def Señal_control():
    print('se toma la señal de control')
    global SCF
    SCF = SC.get()
    SCFS = str(SCF)+' °C'
    Setpoint_Label.configure(text=SCFS)
    duty=90 #no se cambia
    #u = SCF - temperaturaF
    frecuencia = 450 
    voltaje = ((frecuencia + 62)* 24)/1024
    voltajeS = str(int(voltaje))+' v'
    pi_pwm.ChangeDutyCycle(duty)
    pi_pwm.ChangeFrequency(frecuencia)
    Señal_control_Label.configure(text=voltajeS)
    señal_de_control.delete(0,'end')
    

# FUNCION DE ACTUALIZAR LA HORA Y LA FECHA
def update_clock():
    now = time.strftime("%H:%M:%S")
    current_time_label.configure(text=now)
    ventana.after(500, update_clock)

def get_date():
    #OBTENER DIA DE LA SEMANA
    datetime_object = datetime.datetime.now()
    week_day = datetime_object.strftime("%A")

    #OBTENER FECHA
    global d1
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    week_day_label.configure(text=d1 + ' | ' + week_day)
    

# -----------------FRAMES DE LA APLICACION ---------------------------------------------------

#FRAME DE LA HORA Y FECHA
frameHora = frameH.pack(side="left", anchor="n")
frameH.configure(bg="#9AECD5", width=650 , height=200, bd=5 ,relief="groove")
Label(frameHora, text= "HORA Y FECHA ACTUAL", fg= "#005B52",bg="#9AECD5", font=("Times New Roman",18, "bold")).place(x=325, y=10)
current_time_label = Label(frameHora, text="", font=('Times New Roman', 40), fg='#ffffff', bg='#449a66', pady=10, padx=10)
week_day_label = Label(frameHora, text="", font=('Times New Roman', 12), fg='#ffffff', bg='#449a66', pady=10, padx=10)
current_time_label.place(x=360, y=40)
week_day_label.place(x=380, y=130)
update_clock()
get_date()


#IMAGEN DEL LOGO DE LA EMPRESA
imagenLogo = PhotoImage(file = "logo.png")
Label(frameHora, text="LOGO", image=imagenLogo, bg="#9AECD5").place(x=12,y=12)


#FRAME DEL SENSOR DHT21
frameDHT21 = frame.pack(side="right", anchor="n")
frame.config(bg="#61FF00", width=1000 , height=200, bd=5 ,relief="groove")
Label(frameDHT21, text= "SENSOR DE TEMPERATURA Y HUMEDAD (DTH21)", fg= "#225105", bg="#61FF00", font=("Times New Roman",18,"bold")).place(x=850, y=10)
Label(frameDHT21, text= "TEMPERATURA: ", fg= "#225105", bg="#61FF00", font=("Times New Roman",15,"bold")).place(x=675, y=80)
Label(frameDHT21, text= "HUMEDAD: ", fg= "#225105", bg="#61FF00", font=("Times New Roman",15,"bold")).place(x=1175, y=80)
temperaturaLabel = Label(frameDHT21, text="wait", font=('Times New Roman', 70), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
humedadLabel = Label(frameDHT21, text="wait", font=('Times New Roman', 70), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
humedadLabel.place(x=1310, y=45)
temperaturaLabel.place(x=850,y=45)
Sensor_DHT21()

#FRAME DE LA LECTURA ANALOGICA
frameLectura = frameL.place(x=0,y=200)
frameL.config(bg="#A9F5A9", width=1300 , height=675, bd=5 ,relief="groove")
Label(frameLectura, text= "LECTURA DEL ANALIZADOR THERMO 42C", fg= "#225105", bg="#61FF00", font=("Times New Roman",30,"bold")).place(x=240, y=250)
Label(frameLectura, text= "HORA DE MUESTRA", fg= "#225105", bg="#61FF00", font=("Times New Roman",15,"bold")).place(x=40, y=320)
Label(frameLectura, text= "MUESTRA DE NO ", fg= "#225105", bg="#61FF00", font=("Times New Roman",15,"bold")).place(x=320, y=320)
Label(frameLectura, text= "MUESTRA DE NO2 ", fg= "#225105", bg="#61FF00", font=("Times New Roman",15,"bold")).place(x=555, y=320)
Label(frameLectura, text= "MUESTRA DE NOx ", fg= "#225105", bg="#61FF00", font=("Times New Roman",15,"bold")).place(x=800, y=320)
Label(frameLectura, text= "ESTADO DE LA MUESTRA", fg= "#225105", bg="#61FF00", font=("Times New Roman",15,"bold")).place(x=1030, y=320)
NOLabel = Label(frameLectura, text="wait", font=('Times New Roman', 30), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
NO2Label = Label(frameLectura, text="wait", font=('Times New Roman', 30), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
NOxLabel = Label(frameLectura, text="wait", font=('Times New Roman', 30), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
ESTADOLabel = Label(frameLectura, text="wait", font=('Times New Roman', 30), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
horamuestraLabel = Label(frameLectura, text="wait", font=('Times New Roman', 30), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
horamuestraLabel.place(x=30, y=352)
NOLabel.place(x=330, y=352)
NO2Label.place(x=570, y=352)
NOxLabel.place(x=820, y=352)
ESTADOLabel.place(x=1070, y=352)
lecturaAnalogica()

#FRAME PARA EL CONTROLADOR PID
framePID= Frame()
frameCONTROLADOR = framePID.place(x=1300,y=200)
framePID.config(bg="#81F7F3", width=300 , height=460, bd=5 ,relief="groove")
Label(frameCONTROLADOR, text= "Señal de Control (PWM)", fg= "#225105", bg="#61FF00", font=("Times New Roman",18,"bold")).place(x=1315, y=225)
Label(frameCONTROLADOR, text= "SetPoint", fg= "#225105", bg="#61FF00", font=("Times New Roman",18,"bold")).place(x=1400, y=350)
SC = StringVar()
señal_de_control= ttk.Entry(ventana, textvariable=SC)
señal_de_control.place(x=1370, y=480)
señal_de_control.config(justify=CENTER)
Señal_control_Label = Label(frameCONTROLADOR, text="wait", font=('Times New Roman', 25), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
Setpoint_Label = Label(frameCONTROLADOR, text="wait", font=('Times New Roman', 25), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
Señal_control_Label.place(x=1400, y=265)
Setpoint_Label.place(x=1400, y=400)
bottonControl = Button(frameCONTROLADOR,text="ACEPTAR", width=10, height=1, font=("Times New Roman", 10), command=Señal_control, bg="#2ADA0A", fg="white")
bottonControl.place(x=1400, y=510)
global SCF
SCF = SC.get()

#FRAME PARA LA CONEXION RS-232
frameRS= Frame()
frameConexionRS = frameRS.place(x=0,y=875)
frameRS.config(bg="#81F7F3", width=600 , height=260, bd=5 ,relief="groove")
Label(frameConexionRS, text= "Señal a enviar (Tx): ", fg= "#225105", bg="#61FF00", font=("Times New Roman",18,"bold")).place(x=195, y=900)
Label(frameConexionRS, text= "Señal recibida (Rx): ", fg= "#225105", bg="#61FF00", font=("Times New Roman",18,"bold")).place(x=35, y=980)
Label(frameConexionRS, text= "CONEXION RS-232", wraplength=400,fg= "#225105", bg="#61FF00", font=("Times New Roman",40,"bold")).place(x=290, y=980)
tx= StringVar()
señaltx= ttk.Entry(ventana, textvariable=SC)
señaltx.place(x=140, y=950)
señaltx.config(justify=CENTER)
señalrxLabel = Label(frameConexionRS, text="wait", font=('Times New Roman', 50), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
señalrxLabel.place(x=50, y=1020)
bottonConexion = Button(frameConexionRS,text="ACEPTAR", width=10, height=1, font=("Times New Roman", 10), command=conexionRS232, bg="#2ADA0A", fg="white")
bottonConexion.place(x=340, y=945)

#FRAME PARA HALLAR VARIABLES ESTADISTICAS
frameVE=Frame()
frameEstadistica = frameVE.place(x=600,y=875)
frameVE.config(bg="#A9F5A9", width=700 , height=260, bd=5 ,relief="groove")
Label(frameEstadistica, text= "Variables Estadisticas", fg= "#225105", bg="#61FF00", font=("Times New Roman",30,"bold")).place(x=725, y=890)
Label(frameEstadistica, text= "PROMEDIO", fg= "#225105", bg="#61FF00", font=("Times New Roman",15,"bold")).place(x=625, y=960)
Label(frameEstadistica, text= "MEDIANA", fg= "#225105", bg="#61FF00", font=("Times New Roman",15,"bold")).place(x=777, y=960)
Label(frameEstadistica, text= "MODA", fg= "#225105", bg="#61FF00", font=("Times New Roman",15,"bold")).place(x=940, y=960)
promedioLabel = Label(frameEstadistica, text="wait", font=('Times New Roman', 40), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
medianaLabel = Label(frameEstadistica, text="wait", font=('Times New Roman', 40), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
modaLabel = Label(frameEstadistica, text="wait", font=('Times New Roman', 40), fg='#ffffff',bg="#A4A4A4", pady=10, padx=10)
promedioLabel.place(x=625, y=1000)
medianaLabel.place(x=775, y=1000)
modaLabel.place(x=915, y=1000)
bottonCalcular = Button(frameConexionRS,text="CALCULAR", width=10, height=2, font=("Times New Roman", 30), command=calcularEstadistica, bg="#2ADA0A", fg="white")
bottonCalcular.place(x=1050, y=990)


#---------------------------------BOTONES EXCEL Y OTROS -----------------------------------------------------
#BOTON PARA ABRIR Y CREAR EL ARCHIVO EXCEL
frameB = Frame()
frameButton = frameB.pack()
boton1 = Button(frameButton,text="To Excel", width=10, height=2, font=("Times New Roman", 20), command=verExcel, bg="#2ADA0A", fg="white")
boton1.place(x=1375, y=700)
boton2 = Button(frameButton,text="Crear Excel", width=10, height=2, font=("Times New Roman", 20), command=crearExcel, bg="#2ADA0A", fg="white")
boton2.place(x=1375, y=800)


#BOTON PARA HACER QUE EL PROGRAMA FINALICE
botton3 = Button(frameButton,text="Apagado", width=10, height=2, font=("Times New Roman", 20),command=cerrarVentana ,bg="#FF0000", fg="white")
botton3.place(x=1375, y=1000)


#ESTO ES LO QUE MANTIENE EL BUCLE DE LA VENTANA
ventana.mainloop()
