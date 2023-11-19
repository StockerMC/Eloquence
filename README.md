# How to run the project
# NOTE: these commands are tested on Linux. It should probably work on other operating systems as well.
# Message `727_` on Discord if you have any issues

# Install the required dependencies
1) `git clone https://github.com/StockerMC/Eloquence`
2) `cd Eloquence`
3) `cd alice-hacks-backend`
4) `python -m venv venv`
5) `chmod +x venv/bin/activate` (run only on linux, if this command fails, try a different activate file)
6) venv/scripts/activate (Windows) or venv/bin/activate (Linux)`
7) python -m pip install -r requirements.txt` - NOTE: It will take quite a while to download all the models, but you only need to do this once
8) `cd ../alice-hacks-frontend`
9) `npm i`

# Running the backend
1. `cd` into `alice-hacks-backend` folder
2. Run `uvicorn` to start the backend server. Keep note of the ip address that is outputted.

# Running the frontend
1. `cd` into the `alice-hacks-frontend` folder
2. Create a file named `.env`
3. Copy the contents of `.env.example` into `.env`
4. Change the value of `SECRET_BACKEND_SERVER_ADDRESS` to the address of the backend 
5. Run `npm run preview` to run the website