# Install axios for sending requests
# Create src/api.js in frontend/src/
# Create src/constants.js in frontend/src for refresh and access tokens for auth

# Create .env and add the following command
VITE_API_URL = "http://localhost:8000" 
<!-- the url of the backend server no trailing '/' -->

# Define the following constant in api.js
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL ?
  });

# Implement src/components/ProtectedRoute.jsx for specific user access
//pass refreshToken as the payload in ProtectedRoute.jsx and wait for response from beackend

# Create pages as required

# Run the following command to test the site
npm run dev

# Include respective routes in pages from backend
# run both backend and frontend separately and test

# In src/pages/Home.jsx, get the correct routes for each API defined in the backend for the frontend 
const getNotes = () => {
        api
            .get("/api/notes/")
            .then((res) => res.data)
            .then((data) => {
                setNotes(data);
                console.log(data);
            })
            .catch((err) => alert(err));
    };

# After finsihing work on the frontend, time to deploy
# Create a database
# choreo allows for mySQL consider that going forward
# Create environment variable file database I am hosting on 

