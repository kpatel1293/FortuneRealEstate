# FortuneRealEstate

<hr>
SET UP FOR WINDOWS</br>
<b>Installing Python 2.7</b></br>
  Use the link to download: 
    https://www.python.org/downloads/release/python-2715/
</br>
  Check if it is downloaded by python -V and should output: python 2.7.11
</br>
To check if pip is downloaded: python -m pip -V </br>
if it doesnt show pip is downloaded than look at this for furthur help: https://pip.pypa.io/en/stable/installing/</br>

SET UP FOR MAC</br>

1) Install GCC : http://www.mkyong.com/mac/how-to-install-gcc-compiler-on-mac-os-x/
</br>
2) Install Homebrew</br>

run:</br>ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"</br>

after run: </br>
cd ~</br>
nano .bash_profile</br>

it will open the hidden file where you paste at the bottom of the code:</br> 
export PATH=/usr/local/bin:/usr/local/sbin:$PATH</br>
once done press ctrl+x, when prompted to accept changes made, hit 'y' key and enter
</br>
to see if it worked, restart terminal and run: brew , this will output info
</br>
3) Install python
</br>
brew update
</br>
brew install python@2
</br>
<hr>
SET UP DJANGO ON YOUR SYSTEM TO RUN THE PROJECT
</br>
STEP 1: Create virtual environment in your virtual environment folder (seperate folder on your computer)
</br>MAC: 
 </br> install virtualenv with the command: pip install virtualenv
</br>WINDOW: 
 </br> install virtualenv with the command: python -m pip install virtualenv </br>
 
Create virtual env in your floder by :  </br>
 MAC: virtualenv djangoEnv</br>
 WINDOW: python -m virtualenv djangoEnv</br>
 
Activate your virtual env by: </br>
Mac/Linux: source flaskEnv/bin/activate   </br>
Windows command prompt : call flaskEnv/Scripts/activate </br>
Windows 10 command prompt : . flaskEnv/Scripts/activate </br>
------------------------------------------------------------------</br>
Windows git bash : source flaskEnv/Scripts/activate    </br>
 
STEP 2: Download Django in your virtual env</br>
MAC: pip install Django==1.10</br>
WINDOW:pip install django</br>
 
OTHER THINGS TO DOWNLOAD IN ENV:</br>
pip install bcrypt</br>

STEP 3: Running the project (make sure your in terminal in the same location as the manage.py file)</br>
run: python manage.py runserver



