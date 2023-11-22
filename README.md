# How to run the project

## Install the required dependencies
1) `git clone https://github.com/StockerMC/Eloquence`
2) `cd Eloquence`
3) `cd alice-hacks-backend`
4) `(python) -m venv venv`
5) LINUX ONLY: `chmod +x venv/bin/activate` (if this command fails, try a different activate file)
6)` venv/scripts/activate` (Windows) or `venv/bin/activate` (Linux)
7) `(python) -m pip install -r requirements.txt` - NOTE: It will take quite a while to download all the models, but this only needs to be done once.
8) `cd ../alice-hacks-frontend`
9) `npm i`

## Running the backend
1. `cd` into the `alice-hacks-backend` folder
2. Copy `env.example.py` into `env.py` and set your `OPENAI_API_KEY`
3. Run `uvicorn server:app --port 3000` to start the backend server. Keep note of the ip address that is outputted.

# Running the frontend
1. `cd` into the `alice-hacks-frontend` folder
2. Create a file named `.env`
3. Copy the contents of `.env.example` into `.env`
4. Change the value of `SECRET_BACKEND_SERVER_ADDRESS` to the address of the backend 
5. Run `npm run preview` to run the website
