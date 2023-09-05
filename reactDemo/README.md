# Running this Demo

This demo is based on a flask backend and a react frontend, both will have to be started at the same time for the demo to work. You will also need to have redis installed on your machine for the server to work. If you are on windows please install redis [here](https://github.com/microsoftarchive/redis/releases/tag/win-3.0.504), once installed you can check that it is working in powershell by using the command

```
$ redis-cli
```
if you get an IP address you are good. Use the command ```exit``` to leave.

## Flask Backend
### Python
Make sure that python is installed on the system. If it is not installed you can download and install it from [here](https://www.python.org/downloads/windows/). Alternative once can use Anaconda which may be downloaded [here](https://www.anaconda.com/)

Now navigate to the React Demo in Powershell (Windows) or the Terminal (Mac/Linux) and enter the Server folder using

```
cd server
```

### Setting up the virtual environment

#### Python
If you are using base python use the following command to create a virtual environment
```
python -m venv venv             #(windows)
python3 -m venv venv            #(mac/linux)
```

Then activate the virtual environment with the command

```
venv\Scripts\activate               #(windows)
source venv/bin/activate            #(mac/linux)
```

#### Anaconda 
If you are using anaconda on windows it may be helpful to get Anaconda to work in powershell for this open up the powershell console and type the following command
```
powershell -ExecutionPolicy ByPass -NoExit -Command 
```
and enter yes. Then open the Anaconda command prompt, which can be found by searching for it in windows search and use the following command
```
conda init powershell
```
You can now reopen powershell and see the (base) virtual environment present in powershell. This will auto activate every time you start powershell, to disable the auto activation use
```
conda config --set auto_activate_base false
```

Now navigate to the react demo and then the server folder and create a virtual environment by means of

```
conda update conda                          #updating conda to latest version
conda create -n NAME python=3.10 anaconda   # Replace NAME with your choice
conda activate NAME
```


### Intalling the packages
Now run the following command to install all of the relavant packages for this project
```
pip install -r requirements.txt     #windows
pip3 install -r requirements.txt    #max/linux 
```


### Staring the Flask server
Now run the following command to start the server
```
python server.py        #windows
python3 server.py       #max/linux 
```

The flask server will now be running at localhost:5000.

## React Frontend
Start another powershell or terminal console and nagivate to the react demo and then the client folder. Make sure that npm is installed, you can download it [here](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

We now install yarn by means of the following command

```
npx install --global yarn
```

We will now use yarn to install the relevant packages for the react server.
```
yarn install
```
We can now start the react server by means of 

```
yarn start
```
The react server should now be running on localhost:3000



# Deployment
Make sure that you have docker installed in your system as well as the azure command line. Then run the following commands, in this directory

```
az login                #log into azure
docker login azure      #log into azure for docker
az acr login --name containersvtutor        #log into the azure container registry for this project
```

Then run the following
```
docker-compose build        #Build the current project
docker-compose push         #Pusht the project to azure
az webapp update --name virtualtutor --resource-group rg-vtutor         # Update the containers used on azure
```


Then navigate to the portal.azure.com for the webapp vtutor and restart the app there.