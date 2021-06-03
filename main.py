from tkinter import *
from PIL import ImageTk,Image
import numpy as np
import pandas as pd
from heapq import nsmallest
import warnings
import sys
warnings.filterwarnings('ignore')
# Funciones anteriores

##Introducion
##Peliculas vistas
def vistas(lista):
  """
  entradas: una lista de calificaciones
  salida: las calificaciones que no son cero
  funcion: quitar de la lista las peliculas no vistas
  """
  rate_knn = []
  for element in lista:
    if element != 0:
      rate_knn.append(element)
  return rate_knn

##Quitar peliculas no vistas
def sinver(lista):
  """
  entradas: una lista de calificaciones
  salida: las posisiones de las peliculas no vistas
  funcion: tener los indices de las peliculas no vistas
  """

  novistas = []
  for i in range(0,len(lista)):
    if lista[i] == 0:
      novistas.append(i+1)
  return novistas

def modifyDf(dataframe,novistas):
  """
  entradas: dataframe de peliculas,lista de indices de peliculas no vistas
  salida: dataframe solo de peliculas vistas
  funcion: hacer un dataframe de solo peliculas vistas
  """
  df_solovistas = dataframe
  df_solovistas = df_solovistas.drop(df_solovistas.columns[novistas], axis=1)
  df_solovistas = df_solovistas.drop(df_solovistas.columns[0], axis=1)
  return df_solovistas

#Entrega Pasada
def dist(coords1,coords2):
  """
  entradas: lista de coordenadas, lista de coordenadas
  salida: distancia entre coordenadas
  funcion: sacar la distancia entre las coordenadas
  """
  suma = 0
  for i in range(0,len(coords1)):
      resta = (coords1[i]-coords2[i])**2
      suma = suma + resta
  suma = (suma)**(1/2)
  return suma

def putInd(lista):
  """
  entradas: una lista
  salida: lista de listas con indice
  funcion: poner indices a los elementos
  """
  nueva =[]
  for i in range(0,len(lista)):
    nuevo_elemento = [lista[i],i]
    nueva.append(nuevo_elemento)
  return nueva

def kmin(k,lista):
  """
  entradas: numero de numeros minimos,lista de listas de calificaciones con indices
  salida: los elementos con los valores mas chicos
  funcion: sacar los vecinos mas cercanos
  """
  return nsmallest(k, lista)


def KNN(k,listaPuntos,puntos):
  """
  entradas: lista de vecinos, dataframe de peliculas, calificacion de usuario
  salida: los indices de los alumnos mas cercanos
  funcion: sacar los indices de los alumnos con gustos mas parecidos
  """
  lista_dis = []
  for element in listaPuntos:
    dis = dist(element,puntos)
    lista_dis.append(dis)
  lista_indices = putInd(lista_dis)
  minimos = kmin(k,lista_indices)
  indices = []
  for element in minimos:
    indices.append(element[1])
  return indices

##Promedio de peliculas no vistas
def promedios_peliculas(sinver,dataframe):
  """
  entradas: lista de indices de peliculas no vistas, dataframe solo con los vecinos cercanos
  salida: promedio por culmna de las peliculas sinv ver
  funcion: sacar los promedios de las peliculas de los vecinos cercanos que no ha visto el usuario
  """
  promedios = []
  for pelicula in sinver:
    data = []
    prom_p = dataframe.iloc[:, pelicula].mean()
    data.append(prom_p)
    data.append(pelicula)
    promedios.append(data)
  return promedios

def getmax(lista):
  """
  entradas: lista de promedios de peliculas no vistas
  salida: indice de la pelicula no vista con el promedio mas grande
  funcion: sacar el indice de la pelicula a recomendar
  """
  max = 0
  indice = 0
  for element in lista:
    if element[0]>max:
      max = element[0]
      indice = element[1]
  return indice

def recomendar(k,dataframe,cal):
  """
  entradas: vecinos, nombre del archivo sin extencion
  salida: pelicula recomendada
  funcion: recomendar pelicula basada en knn
  """
  if type(dataframe) == str:
    try:
      df = pd.read_csv(dataframe + ".csv")
      print("Se abrio el archivo correctamente")
    except FileNotFoundError:
      print('No se encontro el archivo')
      sys.exit(1)
  else:
    df = dataframe
  ##quitar na
  df = df.drop(["Y"], axis=1)
  df = df.dropna(axis="rows")
  #calificaciones = [5.0,0,5.0,0,4.0,4.5]##Solo son de prueba mientras
  print(df.head())
  calificaciones = cal
  peliculas_vistas = vistas(calificaciones)
  peliculas_sinver = sinver(calificaciones)
  df_sinver = modifyDf(df,peliculas_sinver)
  np_df = np.array(df_sinver)
  indices = KNN(k,np_df,peliculas_vistas)
  df_cercanos = df.iloc[indices]
  print(df_cercanos)
  p = promedios_peliculas(peliculas_sinver,df_cercanos)
  recomendada = getmax(p)
  print(f"Se te recomienda ver la pelicula de : {df.iloc[:, recomendada].name}")
  return df.iloc[:, recomendada].name

window=Tk()
##Cargar pelis
i21 = Image.open('Images/21.jpeg')
i21 = i21.resize((100, 200), Image.ANTIALIAS)
img_2001 = ImageTk.PhotoImage(i21)

iai = Image.open('Images/ai.jpg')
iai = iai.resize((100, 200), Image.ANTIALIAS)
img_ai  = ImageTk.PhotoImage(iai)

ibr = Image.open('Images/br.jpg')
ibr = ibr.resize((100, 200), Image.ANTIALIAS)
img_br = ImageTk.PhotoImage(ibr)

iex = Image.open('Images/ex.jpg')
iex = iex.resize((100, 200), Image.ANTIALIAS)
img_ex = ImageTk.PhotoImage(iex)

ima = Image.open('Images/ma.jpg')
ima = ima.resize((100, 200), Image.ANTIALIAS)
img_ma = ImageTk.PhotoImage(ima)

iyr = Image.open('Images/yr.jpg')
iyr = iyr.resize((100, 200), Image.ANTIALIAS)
img_yr = ImageTk.PhotoImage(iyr)

dict_pelis = {"Exmachina":img_ex,"Yo, Robot": img_yr,"AI":img_ai,"2001":img_2001,"Matrix":img_ma,"Blade Runner":img_br}
window.title('Fakeflix')
window.geometry("800x650+100+50")
window.config(bg="black")
fake = Image.open('Images/fake.png')
fake = fake.resize((150, 150), Image.ANTIALIAS)
my_img = ImageTk.PhotoImage(fake)

Button(text="Ingresar", height="150", width="150", command=(), bg="white", image=my_img, border="0").place(x=280, y=30)
label = Label(text="Hola, bienvenido a Fakeflix. Ponga las calficaciones del 1 al 5 y ponga 0 en las peliculas que no ha visto")
label.place(x=50,y=200)
p1 = Entry(window)
p1.place(x=20, y=550)
p2 = Entry(window)
p2.place(x=150, y=550)
p3 = Entry(window)
p3.place(x=280, y=550)
p4 = Entry(window)
p4.place(x=410, y=550)
p5 = Entry(window)
p5.place(x=540, y=550)
p6 = Entry(window)
p6.place(x=670, y=550)
Button( height="200", width="100", command=(), bg="white", image=img_ex, border="0").place(x=30, y=300)
Button( height="200", width="100", command=(), bg="white", image=img_yr, border="0").place(x=160, y=300)
Button( height="200", width="100", command=(), bg="white", image=img_ai, border="0").place(x=290, y=300)
Button( height="200", width="100", command=(), bg="white", image=img_2001, border="0").place(x=420, y=300)
Button( height="200", width="100", command=(), bg="white", image=img_ma, border="0").place(x=550, y=300)
Button( height="200", width="100", command=(), bg="white", image=img_br, border="0").place(x=680, y=300)
def aplicar():
    window.withdraw()
    c1 = p1.get()
    c2 = p2.get()
    c3 = p3.get()
    c4 = p4.get()
    c5 = p5.get()
    c6 = p6.get()
    c1 = float(c1)
    c2 = float(c2)
    c3 = float(c3)
    c4 = float(c4)
    c5 = float(c5)
    c6 = float(c6)
    calificaciones = [c1]
    calificaciones.append(c2)
    calificaciones.append(c3)
    calificaciones.append(c4)
    calificaciones.append(c5)
    calificaciones.append(c6)
    recomendada = recomendar(5,"peliculas",calificaciones)
    extra = Toplevel(window)
    Label(extra, text=f"Recomendada").place(x=160, y=50)
    Button(extra,height="200", width="100", command=(), bg="white", image=dict_pelis[recomendada], border="0").place(x=120, y=100)
    Label(extra,text=f"Se te recominda ver la pelicula {recomendada}").place(x=70,y=300)
    extra.geometry("400x400+100+50")
    extra.config(bg="black")
    def salir():
        window.deiconify()
        extra.destroy()
    Button(extra,text="Regresar",command=salir).place(x=150,y=350)


Button(text="Recomendar",command=aplicar).place(x=350,y=600)

window.mainloop()