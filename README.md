Requirements:  
Basic knowledge of the CMD/Powershell  
Walk through this guide STEP BY STEP  
  
Uninstall your current Python 
Open Control Panel  
Click "Uninstall a Program"  
Scroll down to Python and click uninstall for all versions you have.  
Download the latest Python here: https://www.python.org/downloads/  
In the setup make sure you click CUSTOM and tick the "Add Python 3.7 to PATH"  
  
Pycharm:  
Start Pycharm  
Click on VCS > Checkout from Version Control > Git > Paste this Github URL: https://github.com/XibenN/nsReisplanner  
and click on Clone  
Make sure you have git installed, if you get an error in the bottom-right, click on download and restart your PC and try again.
  
Windows:  
Go into Powershell as administrator and type in:  
cd C:\  
Set-ExecutionPolicy Unrestricted  
  
^^ This makes it so you can use your Django commands everywhere.  
  
Go to the directory in Powershell.  
cd C:\Users(YOUR_USER)\PycharmProjects\nsReisplanner  
type 'pip install virtualenv'  
(Make sure Powershell is opened as Administrator.)  
  
** If there is already an project interpreter selected, skip this step **  
Use a project interpreter, file > settings > project > project interpreter  
If the interpreter "Python" is not selected, click on the dropdown and click "Show all"  
Click the + button and click on "System Interpreter" and on OK. Make sure PIP is in the list.  
  
Windows:  
virtualenv .  
./Scripts/activate  
pip install django  
pip install xmltodict  
pip install request  
pip install requests  
cd src  
python manage.py runserver  
  
** If you still get errors regarding xmltodict and requests, do this. Otherwise skip this **
file > settings > project > project interpreter > + button > install xmltodict, requests, django
  
Mac:  
virtualenv .  
source ./bin/activate  
pip install django  
pip install xmltodict  
pip install request  
pip install requests  
cd src  
python manage.py runserver  
  
  
Your server should be running now, go to your webbrowser and go to localhost:8000  
  
  
When you want to start up the server again from the start you'd have to do this:
  
Go to the project folder in powershell with admin rights  
Type './Scripts/Activate' to activate the virtual environment  
**On MAC: 'source ./bin/activate'**  
Then cd to the src folder  
Type 'python manage.py runserver'  
