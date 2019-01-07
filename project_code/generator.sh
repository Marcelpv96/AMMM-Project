nServices=48
nBuses=20
nDrivers=20
maxBuses=20

for i in `seq 30` ; do

  python3 gen_instances.py --num_buses $(($nServices)) --num_drivers $(($nServices)) --num_services $(($nServices)) --bmax $(($nServices)) --seed $i

done
