# That's SO Fetch - takehome test

### Let's make Fetch a thing!

Fetch Rewards - Data Engineering Take Home: ETL off of a SQS Queue

### Questions

How would you deploy this application in production?
\*The obvious location for production would be on AWS. I would use SQS and setup a trigger to use Lambda whenever a new message is in the queue. Lambda will do the transform and loading it into a Postgres AWS RDS database.

What other components would you want to add to make this production ready?

- I would do a lot more testing for various performance metrics, system/connection failures and test for bugs.
- Tuning it for better proformance, like batch loading into the database instead of doing it one at a time.
- Add/setup more security around the system.
- Good quality documentation.
- Error handling and logging.
- Backup and recovery.

How can this application scale with a growing dataset.

- With RDS you can increase the storage when needed and also use auto scaling to scale horizonality.

How can PII be recovered later on?

- No, I hashed the values which is unrecoverable but it will have the same output for the same input (deterministic). We could encrpyt the values but most encrpytion is not deterministic, so you can not compare the ciphertext. I assumed that if we needed it, we load it into a different table or database with encryption set up.

What are the assumptions you made?

- I assumed the PII did not need to be recovered and was only needed for comparison by analysts.
- I'm assuming the person reading this will like my personality **MORE** than my code and will hire me. 😉

### Want to try it on your system?

Open a terminal and navigate to a location where you want to put the project
Run the following commands:

git clone https://github.com/mikewschmidt/fetch-takehome.git
cd fetch-takehome
docker compose up -d

Now lets create a virtual environment, so we can cleanly run the program and delete it when you're done.
python3 -m venv fetch-venv

Active the new virtual environment.
Run the one that matches your environment:

# Windows - CMD

fetch-venv\Scripts\activate.bat

# Linux/Mac

source fetch-venv/bin/activate

Lets install the dependent packages and run the program
pip install -r requirements.txt
python main.py

This prints out the unmasked messages from the SQS queue. There is 1 that does not fit the format and was NOT inserted into the database.

Run the test.py file to query the database and see the masked infomation for columns "masked_ip" and "masked_device_id"
python test.py

### Next Steps
