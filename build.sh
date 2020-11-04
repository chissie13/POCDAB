mkdir build
cd build

printf "Installing external libraries..."
sudo apt-get install librtlsdr-dev fftw3 cmake g++ pkg-config autoconf libtins-dev libboost-dev git gnuradio-dev libasio-dev 
sudo apt-get update
printf "Done installing external libraries. Building..."
cmake ..
cmake --build .

printf "Done installing, file can be found at <install_directory>/build/products/bin\n" 
