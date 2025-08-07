mkdir lots_of_files
for i in {1..10000}; do
  head -c 1024 </dev/urandom >lots_of_files/file_$i.bin
done