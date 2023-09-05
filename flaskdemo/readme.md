# Using the Flask Demo
First make sure that anaconda or miniconda is installed (which can be found here(https://docs.conda.io/en/latest/miniconda.html#windows-installers)). Then open up the miniconda terminal.

Test out the environment to make sure it's working (e.g. enter ```python``` and you should see the latest version of Python that you're running). After doing this, you can exit the view by typing ```exit()```. This will be used to also exit your session after you're finished working on your analysis.

Next, you'll want to set up a new workspace that stores all packages you download (good for running locally so you don't have to keep re-downloading); the command for this is ```conda create --name kwantum``` for workspace kwantum (since that makes the most sense in this context).

Download the necessary python scripts within this repo. Now in your kwantum workspace (miniconda environment) navigate to those files through the directory (use the command cd "folder name").

The following packages should be downloaded
- Flask ```conda install -c conda-forge flask```
- Requests ```conda install -c conda-forge requests ````
- nltk ```conda install -c conda-forge nltk ```



# Running the FLASK APP
If you are on windows navigate to the flask app directory and run the following commands:
- ```python home.py```


If you are on linux or mac use the following instead


If you are returning at a later date you will first have to type ```conda activate kwantum``` to re-enter the kwantum workspace that you have created. Then navigate to the flask app directory, and then once again run the commands above.
