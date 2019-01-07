/*********************************************
 * OPL  Model
 * Author: marcel-windows
 * Creation Date: Dec 5, 2018 at 3:05:01 PM
 *********************************************/
int nBuses=...;
int nDrivers=...;	
int nServices=...;
int max_busses=...;

range B=1..nBuses;
range D=1..nDrivers;
range S=1..nServices;			
float temp;
int cap_B[b in B]=...;
float euros_min_B[b in B]=...;
float euros_km_B[b in B]=...;

int BM=...;
int max_D[d in D]=...;


int S_starting_time[s in S]=...;
int duration_s_min[s in S]=...;
float duration_s_km[s in S]=...;
int num_passangers[s in S]=...;
int overlap_time[1..nServices][1..nServices];

float CBM=...;
float CEM=...;

dvar boolean SD [s in S, d in D];
dvar boolean SB [s in S, b in B];

dvar boolean is_used [b in B];

dvar float+ numBaseMinutes[d in D];
dvar float+ numExtraMinutes[d in D];
 

execute{
	var before = new Date();
	temp = before.getTime();

	for (var s=1; s<=nServices; s++){
		for (var s2=1; s2<=nServices; s2++){
			overlap_time[s][s2] = 0;									
		}
	}
	for (var s=1; s<=nServices; s++){
		for (var s2=1; s2<=nServices; s2++){
			if(S_starting_time[s] <= S_starting_time[s2] && (S_starting_time[s]+duration_s_min[s]) >= S_starting_time[s2]){
				overlap_time[s2][s] = 1;	
				overlap_time[s][s2] = 1;			
			}
		}
	}
	
	
}

minimize sum(s in S)sum(b in B)(SB[s,b]*(duration_s_min[s]*euros_min_B[b] + duration_s_km[s]*euros_km_B[b])) + sum(d in D) numBaseMinutes[d]*CBM + sum(d in D) numExtraMinutes[d]*CEM;

subject to{
	//All services must be serviced only once.
	forall(s in S){
		sum(b in B)(SB[s,b]) == 1;
	};	
	forall(s in S){
		sum(d in D)(SD[s,d]) == 1;	
	};
	

	//One driver or bus, cannot do two overlap services.
	forall (s1 in S, s2 in S: s1 != s2 && overlap_time[s1][s2] == 1) {
			forall (d in D) SD[s1][d] + SD[s2][d] <= 1;
			forall (b in B) SB[s1][b] + SB[s2][b] <= 1;
	}
	
	//Maxim passangers.
	forall (b in B){
		forall(s in S){
			cap_B[b] >= SB[s,b]*num_passangers[s];				
		}
	}
	
	//Maxim num of minutes.
	forall (d in D){
		max_D[d] >= sum(s in S)SD[s,d]*duration_s_min[s];	
	}

	forall (d in D) {
		numBaseMinutes[d] + numExtraMinutes[d] == sum(s in S) duration_s_min[s]*SD[s][d];
		numBaseMinutes[d] <= BM;			 
 	}		
	//Defining is used.
	forall (b in B){
		is_used[b]*nServices >= sum(s in S)(SB[s,b]);
	}
	forall (b in B){
		is_used[b] <= sum(s in S)(SB[s,b]);
	}
	max_busses >= sum(b in B)(is_used[b]);

}

execute{
	
	var total_cost = 0;
	for(var s=1;s<=nServices;s++){
		for(var b=1;b<=nBuses;b++){
			total_cost += SB[s][b]*(duration_s_min[s]*euros_min_B[b] + duration_s_km[s]*euros_km_B[b]);	
		}	
	}
	for(var d=1;d<=nDrivers;d++){
		total_cost += numBaseMinutes[d]*CBM + numExtraMinutes[d]*CEM;
	}
	writeln("> total cost : "+total_cost);

}

 

