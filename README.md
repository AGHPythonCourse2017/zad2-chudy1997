# Programowanie w jezyku Python 2016/2017 zadanie 2

Żeby zainstalować wpisz : pip install git+https://github.com/AGHPythonCourse2017/zad2-chudy1997.git

Dostępne moduły z przykładowym użyciem:
  main - plik z przykładowym wywołaniem (funkcja main) 
  
  
  from complexity_estimate import main
    
  main.main()


  ComplexCalc
  

from complexity_estimate import *

tab = [10000 * random.random() for _ in range(int(pow(2, 16)))]

def example(a):

  i = 0
  
  j = 0
  
  while i < len(a):
  
      i = 2 * i + 1
      
      for j in range(1, 100):
      
          j = (2 * j + 1 - 1) / 2
          
  return j
  
 
c1 = ComplexCalc(example, tab, 2, 1, 16, 30)

c1.calculate_complexity()

tmp = c1.get_time_foreseer()(100000)

c1.get_size_foreseer()(tmp)


nazwa package'u complexity_estimate


https://pypi.python.org/pypi/complexity-estimate#downloads
