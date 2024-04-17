/*********************************************
 * OPL 22.1.1.0 Model
 * Author: Tomas Ramirez Morales
 * Creation Date: 18 jul. 2023 at 17:26:14
 *********************************************/

// Parametros de entrada
int n = ...; // Numero de drones
int m = ...; // Numero se sensores

int limite_x = ...; // Limite de la coordenada x del sensor
int limite_y = ...; // limite de la coordenada y del sensor

int minimo_recarga = ...; // Valor minimo que tendra la bateria del dron dedicada a la recarga de sensores
int maximo_bonus_recarga = ...; // Valor maximo que puede alcanzar un extra sumado al mínimo de la bateria del dron dedicada a la recarga de sensores

int minimo_distancia = ...; // Valor minimo que tendra la bateria del dron dedicada al desplazamiento del mismo
int maximo_bonus_distancia = ...; // Valor maximo que puede alcanzar un extra sumado al mínimo de la bateria del dron dedicada al desplazamiento del mismo

int maximo_bateria_restante_sensor = ...; // Valor maximo que puede alcanzar la bateria del sensor restante para cargarse al 100%
int maximo_prioridad = ...; // Valor maximo que puede tener la prioridad de un sensor

float peso_distancia = ...; // Valor que multiplica al sumatorio de las distancias para asignarle un peso en la funcion objetivo. Si es muy alto, puede no funcionar (con los parametros actuales, 0.001 funciona)
 
// Sets
range K = 1..n; // Drones
range S = 1..m; // Sensores

// Parametros
float D[S][S]; // Distancia entre cada pareja de sensores
float F[S]; // Carga necesaria para recargar el sensor i
float P[S]; // Prioridad del sensor i

float B[K]; // Capacidad de recarga de sensores del dron k
float C[K]; // Maxima distancia que puede recorrer el dron k

// Parametros para la generacion de escenarios iniciales
tuple coordenadas {
  float x;
  float y;
}

coordenadas coordSensor[S];

// Generacion de escenarios iniciales
execute{
  
  function getDistancia(i,j){
    return Opl.sqrt(Opl.pow(coordSensor[i].x - coordSensor[j].x, 2) + Opl.pow(coordSensor[i].y - coordSensor[j].y, 2));
  }
  
  for (var i in S) {
    coordSensor[i].x = Opl.rand(limite_x); // Coordenada x aleatoria entre 0 y limite_x
    coordSensor[i].y = Opl.rand(limite_y); // coordenada y aleatoria entre 0 y limite_y
  }
  
  for (var i in K) {
    B[i] = Opl.rand(maximo_bonus_recarga) + minimo_recarga; // Bateria para recargas con carga entre minimo_recarga y minimo_recarga + maximo_bonus_recarga
    C[i] = Opl.rand(maximo_bonus_distancia) + minimo_distancia; // Bateria para desplazarse con carga entre minimo_distancia y minimo_distancia + maximo_bonus_distancia
  }
  
  for (var i in S) {
    
	F[i] = Opl.rand(maximo_bateria_restante_sensor); // Bateria restante para recargar el sensor con valor entre 0 y maximo_bateria_restante_sensor
    P[i] = Opl.rand(maximo_prioridad); // Prioridad del sensor con valor entre 0 y maximo_prioridad
    
    for (var j in S) {
      D[i][j] = getDistancia(i,j) // Asignamos las distancias entre cada par de sensores i y j
    }
  }
  
  // Ajustes para el punto inicial
  F[1] = 0;
  P[1] = 0;
  
}



// Variables de decision
dvar boolean x[S][S][K]; // Variable binaria: 1 si el dron k viaja del sensor i al j
dvar int u[S]; // Variable entera para eliminacion de subtours. Guarda el orden de visita de los sensores



// Funcion Objetivo
maximize (sum(i in S, j in S, k in K) x[i][j][k] * P[j]) - (peso_distancia * (sum(i in S, j in S, k in K) x[i][j][k] * D[i][j]));



// Restricciones
subject to {
  
  	// ############# Restricciones del estilo TSP #############
  	
  	// El destino debe ser distinto al origen, excepto para el inicial
  	forall(i in S: i > 1, k in K)
  	  destino_distinto_sensor:
  	  x[i][i][k] == 0;
  	
  	// Todos los drones deben partir y regresar al origen
  	forall(k in K)
  	  parte_regresa_inicio:
  	  sum(i in S) x[i][1][k] == 1 && sum(i in S) x[1][i][k] == 1;
  	  
  	// Cada sensor es visitado por 0 o 1 drones, excepto el inicial
  	forall(i in S: i > 1, j in S)
  	  sensor_visitado_por_un_dron:
  	  sum(k in K) x[i][j][k] <= 1;
  	  
  	// Desde cada sensor solo puede partir un dron, excepto desde el inicial
  	forall(i in S: i > 1)
  	  solo_sale_uno:
  	  sum(j in S, k in K) x[i][j][k] <= 1;
  	
  	// A un sensor solo puede llegar un dron, excepto para el inicial
  	forall(j in S: j > 1)
  	  solo_llega_uno:
  	  sum(i in S, k in K) x[i][j][k] <= 1;
  	
  	// Si un dron va de i a j, debe existir un sensor i2 desde el que se parte hasta i
  	forall(i in S: i > 1, j in S, k in K)
  	  debe_ser_visitado_previamente:
  	  x[i][j][k] <= sum(i2 in S) x[i2][i][k];
  	  
  	// Eliminacion de subrutas utilizando MTZ (orden de visita de sensores)
  	forall(i in S, j in S: i != j && j != 1, k in K)
  	  elimina_subrutas:
  	  u[i] + 1 <= u[j] + m * (1 - x[i][j][k]);
  	
  	// Restricciones para que los valores del vector de orden de subrutas estén dentro de unos límites
  	forall(i in S: i > 1)
  	  limites_vector_orden_subrutas:
  	  2 <= u[i] && u[i] <= m - 1;
  	  
  	// El sensor inicial siempre se visita primero
  	u[1] == 1;
  	  
  	// Nos aseguramos que el orden de los valores del vector de visita sea secuencial.
  	forall(i in S, j in S: j > 1, k in K)
  	  orden_de_visita_es_secuencial:
  	  x[i][j][k] == 1 => u[i] + 1 == u[j];
  	  
  	  
  	// ############# Restricciones del estilo KP #############
  	
  	// La distancia recorrida por un dron debe ser menor o igual a la distancia máxima que puede recorrer
  	forall(k in K)
  	  distancia:
  	  sum(i in S, j in S) x[i][j][k] * D[i][j] <= C[k];
  	
  	// La bateria recargada por un dron debe ser menor o igual a la bateria máxima que puede recargar
  	forall(k in K)
  	  recarga:
  	  sum(i in S, j in S) x[i][j][k] * F[j] <= B[k];
  	
}




// #### Imprimir solución ####

// Variables para la impresión
float totalRecorrido = 0;
int totalRecargado = 0;
int totalPrioridad = 0;

float sumaDistancias = 0;
int sumaRecargas = 0;
int sumaPrioridades = 0;

int maxDistancia = 0;
int maxRecarga = 0;
int maxRecargaDrones = 0;
int maxPrioridad = 0;

// Imprimimos
execute{
  writeln("\nSENSORES (m) = ", m, "\n");
  
  // Para cada sensor imprimimos sus coordenadas, bateria y prioridad
  //for (var i in S)
  //{
  //  writeln("\nSensor ", i, " (F = ", F[i], ", P = ", P[i], ")");
  //  writeln("x: ", coordSensor[i].x, " y: ", coordSensor[i].y);
  //  
  //  maxRecarga += F[i];
  //  maxPrioridad += P[i];
  //}
  
  // Para cada sensor imprimimos sus coordenadas, bateria y prioridad
  // Usamos este formato para poder comparar resultados con el alg genetico
  for (var i in S)
  {
    writeln("X: ", coordSensor[i].x, "\tY: ", coordSensor[i].y, "\tP: ", P[i], "\tB: ", F[i]);
    
    maxRecarga += F[i];
    maxPrioridad += P[i];
  }

  
  writeln("\n\nDRONES (n) = ", n, "\n");
  
  
  // Imprimimos los drones para poder comparar resultados con el alg genetico
  for (var k in K)
  {
    writeln("{'distance_capacity': ", C[k], ", 'battery_capacity': ", B[k], "}");
  }
  
  // Para cada dron
  for (var k in K) {
    
    maxDistancia += C[k];
    maxRecargaDrones += B[k];
    
    writeln("\n\nDron ", k, " (C = ", C[k], ", B = ", B[k], "):");
    
    // Para cada sensor de origen
  	for (var i in S) {
  	  // Para cada sensor de destino
  	  for (var j in S) {
  	    if (x[i][j][k] == 1) {
  	      writeln("- Viaja de ", i, " a ", j, " (D = ", D[i][j], ", F = ", F[j], ", P = ", P[j], ", u = ", u[i], ")");
  	      totalRecorrido += D[i][j];
  	      totalRecargado += F[j];
  	      totalPrioridad += P[j];
  	    }
  	  }
    }
    writeln("");
    writeln("TOTAL RECORRIDO (sum D) = ", totalRecorrido);
    writeln("TOTAL RECARGADO (sum F) = ", totalRecargado);
    writeln("TOTAL PRIORIDAD (sum P) = ", totalPrioridad);
    
    sumaDistancias += totalRecorrido;
    totalRecorrido = 0;
    sumaRecargas += totalRecargado;
    totalRecargado = 0;
    sumaPrioridades += totalPrioridad;
    totalPrioridad = 0;
  } 
  
  // Resumen del resultado del problema
  writeln("\n\nSUMA DISTANCIAS (D) = ", sumaDistancias, " (max = ", maxDistancia, ")");
  writeln("SUMA RECARGAS (F) = ", sumaRecargas, " (max sensores = ", maxRecarga, ", max drones = ", maxRecargaDrones, ")");
  writeln("SUMA PRIORIDADES (P) = ", sumaPrioridades, " (max = ", maxPrioridad, ")");
}