if [ $# -lt 2 ] || [ $# -gt 3 ]; then
    echo "Usage: ./benchmark.sh <data_dir> <solver> (<time_limit>)"
    echo "Where <solver> can be one of these: OR, LS"
    echo "<time_limit> is the time limit in seconds (default 600 sec)."
    exit 1
fi

if [ $# -eq 3 ]; then
    time_limit=$3
else
    time_limit=600
fi

echo "Experimental Campaign:"
echo "Data directory: $1"
echo "Output directory: log/"
echo "Solver: $2"
echo "Time limit: $time_limit"

mkdir -p log
cd log && mkdir -p $2
echo `date` > $2/date.txt
cd ..

for instance in `ls $1` ; do
    echo Resolution of $instance
    python3 src/main.py $1/$instance $2 $time_limit >> log/$2/log_${instance}
done

grep "obj:" log/$2/*.txt >> log/$2/results.csv

exit 0