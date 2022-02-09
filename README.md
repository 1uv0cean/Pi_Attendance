# Pi_Attendance
얼굴 인식 출석부 프로그램

라즈베이파이 업데이트를 진행합니다.

    ```
    sudo apt-get update && sudo apt-get upgrade   
    ```
    
필요한 모듈들을 설치해줍니다.

```
 #OpenCV설치를 위한 의존성 설치   
    sudo apt-get install build-essential cmake git unzip pkg-config    
    sudo apt-get install libjpeg-dev libpng-dev libtiff-dev   
    sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev   
    sudo apt-get install libgtk2.0-dev libcanberra-gtk*   
    sudo apt-get install libxvidcore-dev libx264-dev libgtk-3-dev   
    sudo apt-get install python3-dev python3-numpy   
    sudo apt-get install libtbb2 libtbb-dev libdc1394-22-dev   
    sudo apt-get install libv4l-dev v4l-utils   
    sudo apt-get install libjasper-dev libopenblas-dev libatlas-base-dev   
    sudo apt-get install libblas-dev liblapack-dev gfortran   
    sudo apt-get install gcc-arm*   
    sudo apt-get install protobuf-compiler   
    sudo apt-get install python-dev python-numpy   
    
  #OpenCV 설치
    cd ~
    wget -O opencv.zip https://github.com/opencv/opencv/archive/4.1.2.zip
    wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.1.2.zip
    unzip opencv.zip
    unzip opencv_contrib.zip
    mv opencv-4.1.2 opencv
    mv opencv_contrib-4.1.2 opencv_contrib
    cd ~/opencv/
    mkdir build
    cd build
    
   #Build하기
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
        -D ENABLE_NEON=ON \
        -D ENABLE_VFPV3=ON \
        -D WITH_OPENMP=ON \
        -D BUILD_TIFF=ON \
        -D WITH_FFMPEG=ON \
        -D WITH_TBB=ON \
        -D BUILD_TBB=ON \
        -D BUILD_TESTS=OFF \
        -D WITH_EIGEN=OFF \
        -D WITH_GSTREAMER=OFF \
        -D WITH_V4L=ON \
        -D WITH_LIBV4L=ON \
        -D WITH_VTK=OFF \
        -D OPENCV_EXTRA_EXE_LINKER_FLAGS=-latomic \
        -D OPENCV_ENABLE_NONFREE=ON \
        -D INSTALL_C_EXAMPLES=OFF \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D BUILD_NEW_PYTHON_SUPPORT=ON \
        -D BUILD_opencv_python3=TRUE \
        -D OPENCV_GENERATE_PKGCONFIG=ON \
        -D BUILD_EXAMPLES=OFF ..
        
   #Build를 위한 메모리 설정
    sudo nano /etc/dphys-swapfile
    Nano text editor진입 후 CONF_SWAPSIZE=100 -> CONF_SWAPSIZE=2048 로 변경
    
   #dphys-swapfile 재시작
    sudo /etc/init.d/dphys-swapfile stop
    sudo /etc/init.d/dphys-swapfile start
    
   #make
    make -j4
    
   #Opencv 설치 마무리
    sudo make install
    sudo ldconfig
    make clean
    sudo apt-get updat
    sudo nano /etc/dphys-swapfile
    #Nano text editor진입 후 CONF_SWAPSIZE=2048 -> CONF_SWAPSIZE=100 로 변경
    sudo reboot
```
