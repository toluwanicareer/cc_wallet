from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from web3.auto import w3, Web3
from .models import Wallet, Transaction
from django.conf import settings
import pdb



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    username=request.data.get("username")
    password=request.data.get("password")
    email=request.data.get("email")
    firstname=request.data.get("firstname")
    lastname=request.data.get("lastname")
    status=chk_email(email)
    if status:  # email does not exist
        try:
            user = User.objects.get(username=username)
            return Response({'message': 'Username Already Exist. Please try another'})
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, is_active=True, password=password,
                                            first_name=firstname, last_name=lastname, email=email)
            user.save()
            address=create_wallet(user)
            return Response({'message:Successful'}, status=HTTP_200_OK)

    else:
        return Response({'message':'Email already exist'})


def get_eth_balance(user):
    ether_balance=w3.eth.getBalance(user.wallet.address)
    return w3.fromWei(ether_balance,'ether')

def get_contract():
    web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:9545'))#TODO: change this to the settings configuration in production
    add = web3.toChecksumAddress(settings.CONTRACT_ADDRESS)
    contract = web3.eth.contract(address=add, abi=settings.ABI)
    return contract

def get_contract_balance(user):
    contract=get_contract()
    cc_bal=contract.functions.balanceOf(user.wallet.address).call()
    return cc_bal

def unlock_account(add, passphrase):
    web3 = Web3(Web3.HTTPProvider(settings.PROVIDER))
    status=web3.personal.unlockAccount(add,passphrase=passphrase)
    return status



@csrf_exempt
@api_view(["POST"])
def send_ether(request):
    address=request.data.get('address')

    amount=request.data.get('amount')
    web3=Web3(Web3.HTTPProvider(settings.PROVIDER))
    value=web3.toWei(float(amount), 'ether')
    #TODO: set_default_account to bear the cost of gas
    tx_hash=web3.eth.sendTransaction( {'to': address,'from': request.user.wallet.address,'value': value})
    tx=Transaction(from_addr=request.user.wallet.address, to_addr=address,tx_hash=tx_hash.hex(), amount_in_wei=value)
    tx.save()
    data={'message':'Successful', 'tx_hash':tx_hash.hex()}
    #pdb.set_trace()
    return Response(data, status=HTTP_200_OK)

#TODO: remember to write a cron job to update the status of the transacrtion

@csrf_exempt
@api_view(["POST"])
def get_address(request):
    response=dict()
    try:
        address=Wallet.objects.get(user=request.user)
        data={'address':address,'message':'Successful'}
        return Response(data, status=HTTP_200_OK)
    except Wallet.DoesNotExist:
        #it means user was not set up properly, this should never happen
        response['message']='Address not found'
        return Response(response, status=HTTP_404_NOT_FOUND)



@csrf_exempt
@api_view(["POST"])
def send_token(request):
    _amount=request.data.get('amount')
    _address=request.data.get('address')
    contract=get_contract()
    tx_hash=contract.functions.transfer(_address,_amount).send({
        'from':request.user.wallet.address,
    })
    tx = Transaction(from_addr=request.user.wallet.address, to_addr=_address, tx_hash=tx_hash.hex(), currency='cc', amount_in_wei=_amount)
    tx.save()
    data = {'message': 'Successful', 'tx_hash': tx_hash.hex()}
    # pdb.set_trace()
    return Response(data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def get_account_detail(request):
    ether_balance=get_eth_balance(request.user)
    cc_balance=get_contract_balance(request.user)
    data={'eth_balance': ether_balance, 'cc_balance':cc_balance}
    return Response(data, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
def get_transactions(request):
    transactions=Transaction.objects.filter(user=request.user)
    txs = [{'to':tx.to_addr, 'tx_hash':tx.tx_hash, 'amount':Web3.fromWei(int(tx.amount_in_wei),'ether')} for tx in transactions]
    data={'transaction_lists':txs}
    return Response(data, status=HTTP_200_OK)

def chk_email(email):
    user=User.objects.filter(email=email)
    if user.exists():
        return False
    else:
        return True

def create_wallet(user):

    #cannot create more than a particualr number of account
    user_wallets_count=Wallet.objects.filter(user=user)
    if user_wallets_count.exists():
        return False

    # create the wallet on the localhost node, so the node can manage it
    address=w3.personal.newAccount(user.username)
    wallet=Wallet(address=address, user=user)#create the wallet instance to store in database for future reference
    #unlock account for use
    w3.personal.unlockAccount(address,passphrase=user.username)
    #TODO: handle error, if unlock account is not successful
    wallet.save()
    return address



@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    #pdb.set_trace()
    return Response(data, status=HTTP_200_OK)


