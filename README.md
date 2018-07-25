# hacktech2018

 Our project aims to make the receipt splitting more efficient through utilizing the Google Cloud Vision API. A problem we've encountered as college students specifically is splitting large receipts after a big shopping run, such as getting groceries at Costco. Instead of manually keeping track of what your friends or roommates want to split, Receipt It! takes the hassle out of this process by automating it through cloud computing services. Take a picture of your receipt, and our program will process an itemized list of products and prices. Then, you and your friends or roommates choose which items they want to split, and each individual's total will be sent automatically. 

To Run
1. `> git clone https://github.com/RussellCaletena/hacktech2018.git`
2. `> cd \hacktech2018\receiptRecognition`
3. Make sure you have a valid Google service account JSON file
3. Run `> gcloud auth login` in the Google Cloud SDK
4. Run `> cloud_sql_proxy.exe -instances=<INSTANCE_CONNECTION_NAME>=tcp:5432`. Make sure you have the cloud sql proxy installed on your computer. The instance name may be something similar to: `slohacks:us-west1:receipt`.
5. To run: `> python manage.py runserver`
6. This will by default run the server at `127.0.0.1:8000`
7. Visit `127.0.0.1:8000/shopperHelper` in your browser for the client side and `127.0.0.1:8000/admin` for the admin side.
  1. Default password for admin is USERNAME: `root`, PASSWORD: `superpassword`
