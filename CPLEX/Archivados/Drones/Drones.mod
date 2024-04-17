/*********************************************
 * OPL 22.1.1.0 Model
 * Author: tomit
 * Creation Date: 17 jul. 2023 at 21:01:34
 *********************************************/


int n = ...;
int m = ...;

// Sets
range T = 1..n;
range C = 1..m;

// Parameters
float D[C][C] = ...; // Distance between sensors
float L[C] = ...; // Load consumed (to recharge) at sensor i
float K[T] = ...; // Drone capacity
float R[T] = ...; // Maximum travel distance of drone i
float P[C] = ...; // Sensor priorities

// Decision Variables
dvar boolean x[C][C][T]; // Binary variable: 1 if drone t travels from sensor i to sensor j
dvar boolean y[C][T]; // Binary variable: 1 if drone t visits sensor i

// Objective Function
maximize sum(i in C, j in C, t in T)P[i] * L[i] * x[i][j][t];

// Constraints
subject to {
  
    // Each drone must visit at least one additional sensor besides the starting one
    forall(t in T)
      visit_one:
      sum(i in C) y[i][t] >= 2;

    // Each sensor, except the starting and returning sensor, must be visited by at most one drone
    forall(i in C: i != 1)
      visited_once:
      sum(t in T) y[i][t] <= 1;

    // The load of each drone cannot exceed its capacity
    forall(t in T)
      load:
      sum(i in C) L[i] * y[i][t] <= K[t];

    // The distance traveled by each drone cannot exceed its maximum travel distance
    forall(t in T)
      distance:
      sum(i in C, j in C) D[i][j] * x[i][j][t] <= R[t] + 1;

    // Constraints to ensure drones leave and return to the same sensor
    forall(i in C: i > 1, t in T) {
      	same_sensor:
        sum(j in C) x[i][j][t] == 1; // Se deben agregar restricciones para garantizar que los drones salgan y regresen al mismo sensor
        sum(j in C) x[j][i][t] == 1;
        x[i][i][t] == 0;
    }

    // Some sensors may be unreachable due to previous constraints
    forall(i in C, j in C, t in T)
      unreachable:
      D[i][j] >= R[t] => y[j][t] == 0;
	
	forall(i in C: i > 1, t in T)
	  unrechargachable:
      L[i] == 0 => y[i][t] == 0;
	
}


// Imprimir solución
execute{
  
  for(var t in T) {
    writeln("Dron ", t, ":");
    for(var i in C) {
        if(y[i][t] == 1) {
            writeln("Visita el sensor ", i);
      }
    }  	
  }
}

