"# cc_wallet Api Server"


Documentation for Wallet
Prequisite:
Django 2.0
Python 3.7 or older

Step to install the api server on localhost
Git clone source
run this in your console, preferably in a virtual environment
pip install -r requirements.txt – this will install all the depencies like web3 etc

You are done with that:
Download ganache , install and run it – Ganache is a standalone blockchain that developers can use for testing their dapps, it comes with 10 default account on the network

Once ganache is running:
Copy one the address and copy it to the Mathew wallet, so that u can use it for testing

After this you will steup the contract blockchain too, but most of the api should be working

Endpoints
Login api/account/login
Parameters {username, password}
Returns - token

Use this to test, the rest can be provided on request
