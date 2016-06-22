##Upgrade your packages
sudo apt-get upgrade
<br>
##Install Compilers (Fortran & GCC)
sudo apt-get install -y gfortran gcc-multilib g++-multilib libffi-dev libffi6 libffi6-dbg python-crypto python-mox3 python-pil python-ply libssl-dev zlib1g-dev libbz2-dev libexpat1-dev libbluetooth-dev libgdbm-dev dpkg-dev quilt autotools-dev libreadline-dev libtinfo-dev libncursesw5-dev tk-dev blt-dev libssl-dev zlib1g-dev libbz2-dev libexpat1-dev libbluetooth-dev libsqlite3-dev libgpm2 mime-support netbase net-tools bzip2
<br>
##Install other dependencies
sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev
<br>
<br>
sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev python-pip
<br>
<br>
sudo pip install greenlet
<br>
<br>
sudo pip install gevent
<br>
##Build Numpy, Scipy & Scikit
<br>
sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran
<br>
sudo pip install numpy scipy scikit-learn

##Install language dependencies
sudo pip install unidecode redis gensim nltk
