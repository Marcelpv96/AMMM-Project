nServices=10
nBuses=7
nDrivers=7
maxBuses=8

for i in `seq 20` ; do
  nServices=$(($nServices+1))
  nBuses=$(($nBuses+1))
  nDrivers=$(($nDrivers+1))
  maxBuses=$(($maxBuses+1))
  python3 gen_instances.py -b $nBuses -d $nDrivers -s $nServices --bmax 25 --seed $i

done
