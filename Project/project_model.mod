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

int cap_B[b in B]=...;
int euros_min_B[b in B]=...;
int euros_km_B[b in B]=...;

int BM=...;
int max_D[d in D]=...;


int S_starting_time[s in S]=...;
int duration_s_min[s in S]=...;
int duration_s_km[s in S]=...;
int num_passangers[s in S]=...;
int overlap_time[1..nServices][1..nServices];

float CBM=...;
float CEM=...;
int test[1..nDrivers];

dvar boolean SD [s in S, d in D];
dvar boolean SB [s in S, b in B];

dvar boolean is_used [b in B];

dvar int driver_cost[d in D];


execute{
	for (var s=1; s<=nServices; s++){
		for (var s2=1; s2<=nServices; s2++){
			if(s==s2){
				overlap_time[s][s2] = 1;					
			}else if (S_starting_time[s2] <= (S_starting_time[s]+duration_s_min[s]) ){
				overlap_time[s][s2] = 1;
			}else if(S_starting_time[s] <= (S_starting_time[s2]+duration_s_min[s2]) ){
				overlap_time[s2][s] = 1;		
			}else{
				overlap_time[S][s2] = 0;									
			}
		}
	}
	
	
}

minimize sum(s in S)sum(b in B)(SB[s,b]*(duration_s_min[s]*euros_min_B[b] + duration_s_km[s]*euros_km_B[b])) + sum(d in D)driver_cost[d];

subject to{
	//All services must be serviced only once.
	forall(s in S){
		sum(b in B)(SB[s,b]) == 1;
	};	
	forall(s in S){
		sum(d in D)(SD[s,d]) == 1;	
	};
	
	//Which cost will have each driver.
	forall(d in D){
		driver_cost[d] >=  BM*CBM + (CEM*(sum(s in S)SD[s,d]*duration_s_min[s])-BM);	
	}
	forall(d in D){
		driver_cost[d] >= CBM*(sum(s in S)SD[s,d]*duration_s_min[s]);		
	}

	//One driver or bus, cannot do two overlap services.
	forall (s1 in S, s2 in S: s1 < s2 && overlap_time[s1][s2] == 1) {
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
	for(var d=1;d<=nDrivers;d++){
		test[d] = 0;
	}
	for(var d=1;d<=nDrivers;d++){
		for (var s=1; s<=nServices; s++){
			for (var s2=1; s2<=nServices; s2++){
				test[d] = overlap_time[s][s2]*SD[s][d]*SD[s2][d]+test[d] ;
			}
		}
	}
	
	for(var d=1;d<=nDrivers;d++){
		writeln("-> Driver number : " + d +" i result :"+test[d]);
	}
	
	var total_cost = 0;
	for(var s=1;s<=nServices;s++){
		for(var b=1;b<=nBuses;b++){
			total_cost += SB[s][b]*(duration_s_min[s]*euros_min_B[b] + duration_s_km[s]*euros_km_B[b]);	
		}	
	}
	for(var d=1;d<=nDrivers;d++){
		total_cost += driver_cost[d];
	}
	writeln("> total cost : "+total_cost);

	
}

 
