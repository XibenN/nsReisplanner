Uninstall your current Python  
Download the latest Python here: https://www.python.org/downloads/   
In the setup make sure you tick the "Add Python 3.7 to PATH"  
  
Pycharm:  
Start Pycharm  
Click on VCS > Checkout from Version Control > Git > Paste this Github URL: https://github.com/XibenN/nsReisplanner and click on Clone
  
Windows:  
Go into Powershell as administrator and type in:  
cd C:  
Set-ExecutionPolicy Unrestricted  
  
^^ This makes it so you can use your Django commands everywhere.  
  
  
Use a project interpreter, file > settings > project > project interpreter  
If the interpreter "Python" is not selected, click on the dropdown and click "Show all"  
Click the + button and click on "System Interpreter" and on OK. Make sure PIP is in the list.  
  
Clone this code and go to the directory in Powershell.  
type 'pip install virtualenv'  
(Make sure Powershell is opened as Administrator.)  
  
Windows:   
virtualenv .   
./Scripts/activate   
pip install django   
pip install xmltodict  
pip install request  
  
Mac:  
virtualenv .  
source ./bin/activate  
pip install django  
pip install xmltodict  
pip install request  
