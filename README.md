## Portfolio Monitor
### What is it?
#### It is a simple portfolio monitoring simulator
### How to use it?
#### Get portfolio statistic
   1. Download the project
   2. Open the project by PyCharm
   3. Run the application
   4. Invoke the price publishing task:  
      POST http://127.0.0.1/position/start-publishing/
   5. Get portfolio statistic by this API:  
      GET http://127.0.0.1/position/statistic/
#### Manage the stock, option, position defination
   1. Invoke the viewSet of the model  
      Example: GET http://127.0.0.1/stock/  
               GET http://127.0.0.1/stock/1/  
               DELETE http://127.0.0.1/stock/1/
