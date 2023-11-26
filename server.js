
const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');



const app = express();
const port = process.env.PORT || 3000;
const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://dbBerkay:berkay123@cluster0.wybtlyo.mongodb.net/";

// Connect to MongoDB (replace 'your_database_name' with your actual database name)
mongoose.connect('mongodb+srv://dbBerkay:berkay123@cluster0.wybtlyo.mongodb.net/?retryWrites=true&w=majority', { useNewUrlParser: true, useUnifiedTopology: true });

// Define a User model
const User = mongoose.model('User', {
  username: String,
  password: String,
});

// Middleware
app.use(bodyParser.json());


// Route for user login
app.post('/api/login', async (req, res) => {
  const { username, password } = req.body;

  try {
    // Find the user in the database
    const user = await User.findOne({ username, password });

    if (user) {
      res.json({ success: true, message: 'Login successful' });
    } else {
      res.json({ success: false, message: 'Invalid username or password' });
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

app.post("/api/register", async (req, res) => {
  const {username, password} = req.body;
  try {
  const user = await User.create({username, password});
  if (user) {
      res.json({success: true, message: "User successfully created"});
  } else {
      res.json({success:false, message: "Couldn't create user"});
  }
}
  catch (error) {
  console.error(error);
  res.status(500).json({success:false, message:"Internal server error"})
}
});

const Day = mongoose.model('Day', {
  day: String,
});

// Add this route to your server-side code
app.post('/api/save_day', async (req, res) => {
  const { day } = req.body;

  try {
    // Perform the necessary logic to save the day to MongoDB
    // Ensure you have the appropriate Mongoose model and schema set up

    const savedDay = await Day.create({ day });

    if (savedDay) {
      res.json({ success: true, message: 'Day saved successfully' });
    } else {
      res.json({ success: false, message: 'Failed to save the day' });
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});




// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});