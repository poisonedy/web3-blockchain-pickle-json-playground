from pickleshare import *
from web3 import Web3
import os
import json
import concurrent.futures
import time
import threading
import copy

AbiDict ={'default':'[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"minTokensBeforeSwap","type":"uint256"}],"name":"MinTokensBeforeSwapUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"tokensSwapped","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"ethReceived","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"tokensIntoLiqudity","type":"uint256"}],"name":"SwapAndLiquify","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"enabled","type":"bool"}],"name":"SwapAndLiquifyEnabledUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_liquidityFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxTxAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_taxFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"}],"name":"deliver","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"geUnlockTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromFee","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromReward","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"time","type":"uint256"}],"name":"lock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"},{"internalType":"bool","name":"deductTransferFee","type":"bool"}],"name":"reflectionFromToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"liquidityFee","type":"uint256"}],"name":"setLiquidityFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxTxPercent","type":"uint256"}],"name":"setMaxTxPercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_enabled","type":"bool"}],"name":"setSwapAndLiquifyEnabled","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"taxFee","type":"uint256"}],"name":"setTaxFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"swapAndLiquifyEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"rAmount","type":"uint256"}],"name":"tokenFromReflection","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"uniswapV2Pair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"uniswapV2Router","outputs":[{"internalType":"contract IUniswapV2Router02","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
}

class dataBase:

    def __init__(self, ownDirectory, pathTofileDB):

        self.rootDataDirectory = os.getcwd() + "/dataDB"
        self.ownDirectory = ownDirectory
        self.pathToFileDB = pathTofileDB
        if not os.path.isdir(self.rootDataDirectory):
            os.mkdir(self.rootDataDirectory)
        if not os.path.isdir(self.rootDataDirectory + "/" + self.ownDirectory):
            os.mkdir(self.rootDataDirectory + "/" + self.ownDirectory)


        self.completePath = self.rootDataDirectory + "/" +  self.ownDirectory + "/" + self.pathToFileDB

        try:

            self.objDB = PickleShareDB(self.completePath)

        except:

            return False

    def _emptyDB(self):
        
        try:

            self.objDB.clear()

        except:

            return False

    def _insertKeyValue(self, key, value):

        self.key = key
        self. value = value

        try:
            self.objDB[self.key] = self.value

        except:

            return False

    def _DBItems (self):

        return self.objDB.items()



class blockchainConnector:
    def __init__(self, urlWeb3):
        self.urlWeb3 = urlWeb3
        self.web3 = Web3(Web3.HTTPProvider(urlWeb3))
        from web3.middleware import geth_poa_middleware
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def isValidConnection (self):
        return self.web3.isConnected()



class BlockchainClass (dataBase, blockchainConnector):

    class ContractsExplorer (dataBase, blockchainConnector):

        def __init__(self, blockchainName, blockchainAPI):
            self.blockchainName = blockchainName
            self.blockchainAPI = blockchainAPI
            dataBase.__init__(self, self.blockchainName, "contracts")
            blockchainConnector.__init__(self, self.blockchainAPI)


            

        def exploreAndSet(self, address, blocknumber):

            self.address = address
            self.blocknumber = blocknumber
            try:

                tokenAddress = str(self.web3.toChecksumAddress(self.address))
                tokenRouter = self.web3.eth.contract(tokenAddress, abi=json.loads(AbiDict['default']))

                self.nameTokenContract = tokenRouter.functions.name().call()
                print (self.nameTokenContract)
                
                

                #return self.nameTokenContract
            except:
                print ("no contract found")
            else:
                try:

                    self._insertKeyValue(tokenAddress, {"Found_on_BLOCK":self.blocknumber, "Token_NAME": self.nameTokenContract, "Token_SYMBOL": tokenRouter.functions.symbol().call(),"Contract_ADDRESS" : tokenAddress})
                    print ("Tokens Found:")
                    for item in self.objDB.keys():
                        print(self.objDB[item])

                except:
                    print ("There was a problem running contract functions.")



    class TransactionsViewer (blockchainConnector):

        def __init__(self, blockchainName, blockchainAPI, block):

            self.blockchainAPI = blockchainAPI
            self.blockchainName = blockchainName
            self.block = block
            blockchainConnector.__init__(self, self.blockchainAPI)
            self.ContractExplorer = BlockchainClass.ContractsExplorer(self.blockchainName, self.blockchainAPI)
            self.get_Transactions(self.block)
            

        
  
        def get_Transactions (self, blocknumber):
  
                self.blocknumber = blocknumber
                print ("checking block " + str(self.blocknumber))
                self.data = self.web3.eth.get_block(self.blocknumber)
                self.transactions = self.data['transactions']
                if self.transactions != []:
                    for item in self.transactions:
                        self.get_addresses_and_run_contract_explorer(item.hex(), self.blocknumber)
                else:
                    print ("No transactions Found in block number " + str(self.blocknumber))


        def get_addresses_and_run_contract_explorer (self, transactionID, blocknumber):

            self.transactionID = transactionID
            self.blocknumber = blocknumber
            self.transactionData = self.web3.eth.get_transaction(self.transactionID)
            self.fromAddress = self.transactionData['from']
            self.toAddress = self.transactionData['to']
            self.ContractExplorer.exploreAndSet(self.fromAddress, self.blocknumber)
            self.ContractExplorer.exploreAndSet(self.toAddress, self.blocknumber)



    def __init__(self, blockchainName, blockchainAPI_URL):

        self.blockchainName = blockchainName
        self.blockchainAPI_URL = blockchainAPI_URL

        dataBase.__init__(self, self.blockchainName, "blockchain")
        blockchainConnector.__init__(self, self.blockchainAPI_URL)




        self.dataBlockchain = "blockchainInfo.dat"
        self.dataLastBlockCount = "blockchainLastBlock.dat"
        self.dataLastParsedBlock = "blockchainLastParsedBlock.dat"
        self.operableBlockchain = False
        self.lastBlock = 0
        self.setupBlockChainVars()

        if self.isValidConnection() is True:

            self.operableBlockchain = True

            self._insertKeyValue(self.dataBlockchain, {"blockchain_NAME": self.blockchainName, "blockchainAPI_URL" : self.blockchainAPI_URL})
        
        else:

            return False

    def setupBlockChainVars(self):
        self.getLastBlock()
        self.getLastParsedBlock()

    
    def getLastBlock(self):
        self.lastBlock = int(self.web3.eth.block_number)

        self._insertKeyValue(self.dataLastBlockCount, self.lastBlock)

    
    
    def getLastParsedBlock(self):

        try:
            self.lastParsedBlock = self.objDB[self.dataLastParsedBlock]

        
        except:

            
            self.lastParsedBlock = 0
            self._insertKeyValue(self.dataLastBlockCount, self.lastParsedBlock)



    def runTransactionViewer (self,blockchainName, blockchainAPI, block):
        self.blockchainAPI = blockchainAPI
        self.blockchainName = blockchainName
        self.block = block
        self.connector = blockchainConnector(self.blockchainAPI)
        self.ContractExplorer = BlockchainClass.ContractsExplorer(self.blockchainName, self.blockchainAPI)
        print ("checking block " + str(self.block))
        self.data = self.connector.web3.eth.get_block(block)
        self.transactions = self.data['transactions']
        print (self.transactions)
        if not self.transactions:
            for item in self.transactions:

                self.transactionData = self.connector.web3.eth.get_transaction(item)
                self.fromAddress = self.transactionData['from']
                self.toAddress = self.transactionData['to']
                self.ContractExplorer.exploreAndSet(self.fromAddress, self.block)
                self.ContractExplorer.exploreAndSet(self.toAddress, self.block)

            else:
                print ("No transactions Found in block number " + str(self.block))


    def parseBlock(self):

        
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:

            for lastblock in range(self.lastBlock):
  
                future_to_cc = {executor.submit(self.runTransactionViewer, self.blockchainName, self.blockchainAPI_URL, copy.copy(lastblock))}
    
                self.lastParsedBlock = self.lastParsedBlock + 1
            #self.TransactionViewer.get_Transactions(self.lastParsedBlock, self.data)
            

        for future in concurrent.futures.as_completed(future_to_cc):
            try:
                lastblock = future_to_cc[future]
                
                
            except:
                print ("Job Finished")


            try:
                data = future.result()
                


            except Exception as exc:

                print('%r generated an exception: %s' % (lastblock, exc))
            else:
                print('%r page is %d bytes' % (lastblock, len(data)))




    


blDB = BlockchainClass("Polygon", "https://polygon-mainnet.infura.io/v3/e209d7d77e934b32a98ab3fb700513e3")
print (blDB.lastBlock)
print (blDB.lastParsedBlock)




blDB.parseBlock()

