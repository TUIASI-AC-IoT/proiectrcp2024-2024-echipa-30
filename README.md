# Documentație Proiect 
## Aplicație pentru Descoperirea unei Topologii de Rețea - Implementare RIPv2

#### Studenți: Sărăteanu Alexandru, Gurău Dragoș-Sergiu


### 1. Introducere
Descoperirea topologiei unei rețele ajută echipele IT să înțeleagă structura rețelei, facilitând depanarea, diagnosticarea problemelor și optimizarea performanței și a securității. De aceea ne propunem sa dezvoltăm o astfel de aplicație, demonstrându-i funcționarea pe baza unei topologii de rețea de mașini virtuale configurate în VirtualBox.
### 2. Cerințe Tehnice
#### 2.1 Configurația VM-urilor în VirtualBox: 
- Pregătește mai multe mașini virtuale, fiecare configurată cu două interfețe de rețea:
    - Interfață NAT pentru acces la gazdă (prin SSH).
    - Interfață internă pentru comunicare cu celelalte VM-uri, utilizată pentru mesajele RIP v2.
- Adrese IP alocate static.
#### 2.2 Utilizarea modulului socket pentru comunicarea între mașini virtuale, fără alte module pentru lucrul cu stiva de rețea.
#### 2.3 Implementarea protocolului RIPv2 conform RFC: 
- Formatul de mesaj specific RIPv2
- Logica de schimb de mesaje specifică RIPv2
- Mecanismul de actualizare a informațiilor diseminate specific RIPv2
#### 2.4 Implementarea structurii de date internă pentru stocarea structurii topologiei
![image](https://github.com/user-attachments/assets/2e5a02ef-2af7-44d9-9fd0-038092c63761)

#### 2.5 Parametrii configurabili
Implementarea trebuie să permită setarea unor parametri specifici pentru configurarea funcționării protocolului, cum ar fi:
- Timpul de actualizare pentru mesaje (update timer).
- Limita maximă de distanță pentru rute (de exemplu, 15 hop-uri).
- Timeout pentru expunerea rutelor inactive.

### 3. Protocolul RIPv2
Protocolul de Rutare a Informației (RIP, Routing Information Protocol în engleză) este un protocol de rutare de tip distanță-vector ce implică utilizarea ca metrică de rutare a numărului de pași de rutat (hop count). Prin aceasta, RIP previne apariția buclelor de rutare, utilizând o valoare limită maximă ca număr de pași de rutare pe calea de la sursă la destinație. 

#### 3.1 Caracteristicile principale ale RIPv2 includ:
- Algoritm de rutare bazat pe distanță (Hop Count): Numărul de hop-uri (sărituri) reprezintă metricul principal pentru determinarea traseului optim.
- Actualizări periodice de rutare: Fiecare nod trimite periodic tabela sa de rutare vecinilor pentru a permite propagarea informațiilor în întreaga rețea.
- Limită de metrică: Distanta maximă este de 15 hop-uri, ceea ce face RIP potrivit pentru rețele mici și medii (o valoare fixată la 16 reprezintă o distanță de rutare infinită, inoperabilă, prin urmare de evitat în selecția procesului de rutare).
### 4. Funcționalități Principale
#### 4.1 Detectarea și adaptarea la modificări: 
- Detectarea schimbărilor în topologie (de exemplu, adăugarea/eliminarea unui nod) și actualizarea in timp real a tabelelor de rutare corespunzătoare.

![image](https://github.com/user-attachments/assets/d0998697-9bde-4b48-8254-8902f3fa6f91)

#### 4.2 Vizualizarea topologiei de rețea: 
- Afișarea grafică a topologiei rezultate în urma algoritmului RIP, pentru a vizualiza traseele și distanțele dintre noduri.
