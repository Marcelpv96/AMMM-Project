nServices=9
nBuses=7
nDrivers=7
maxBuses=5

for i in `seq 1000` ; do
  value=$(((RANDOM % 120)+10))
  max=$(((RANDOM % 15)+1))
  bus=$(((RANDOM % 7)+1))
  driver=$(((RANDOM % 7)+1))

  python3 gen_instances.py --num_buses $(($nServices+value-bus)) --num_drivers $(($nServices+value-driver)) --num_services $(($nServices+value)) --bmax $(($nServices+value-max)) --seed $i

done
