/*********************************************
 * OPL 12.6.0.0 Model
 * Author: marcepv
 * Creation Date: Jan 5, 2019 at 12:31:24 AM
 *********************************************/

main {
	
	 for(var i=1;i<=700;i++){
	 	 
	 	var src = new IloOplModelSource("project_model.mod");
	 	var def = new IloOplModelDefinition(src);
	 	var cplex = new IloCplex();
	 	cplex.tilim = 600;
	 	writeln("instance_seed_"+i+".dat");
	 	var model = new IloOplModel(def,cplex);	
	 	var data = new IloOplDataSource("../project_code/instances/instance_seed_"+i+".dat");

	 	model.addDataSource(data);
	 	model.generate();
		 if (cplex.solve()) {
		 		var total_cost = 0;
				for(var s=1;s<=model.nServices;s++){
					for(var b=1;b<=model.nBuses;b++){
						total_cost += model.SB[s][b]*(model.duration_s_min[s]*model.euros_min_B[b] + model.duration_s_km[s]*model.euros_km_B[b]);	
					}	
				}
				for(var d=1;d<=model.nDrivers;d++){
					total_cost += model.driver_cost[d];
				}
				var after = new Date();
				var solving_time= (after.getTime()-model.temp)*0.001;
				
				if (solving_time > 60){
					writeln("<--- INSTANCE --->");
					writeln("instance_seed_"+i+".dat");
					writeln("> total cost : "+total_cost);	
					writeln("> solving time ~= ",(after.getTime()-model.temp)*0.001);
					writeln("<---------------->");										
				}else{
									
				}
					
		 }
		 else {
		 	writeln("<--- INSTANCE --->");
			writeln("instance_seed_"+i+".dat");		 
		 	writeln("Not solution found");
		 	writeln("<---------------->");
		 }
		 writeln("Finish");
		 model.end();
		 data.end();
		 def.end();
		 cplex.end();
		 src.end();
	}	
	
};