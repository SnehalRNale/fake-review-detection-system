const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

// Initialize the app
const app = express();

// Body-parser middleware to handle POST data
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// MongoDB connection
const mongoose = require('mongoose');

// Connect to MongoDB Local instance
mongoose.connect('mongodb://localhost:27017/mydatabase', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
}).then(() => {
    console.log('Connected to MongoDB locally');
}).catch((err) => {
    console.error('Error connecting to MongoDB:', err);
});

// Create a schema for storing contact form data
const contactSchema = new mongoose.Schema({
    name: String,
    email: String,
    message: String
});

// Create a model from the schema
const Contact = mongoose.model('Contact', contactSchema);

// Route to serve the HTML form (for testing)
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/contact.html'); // Ensure contact.html is present in your root directory
});

// Route to handle form submission
app.post('/submit-form', (req, res) => {
    // Get data from the form submission
    const { name, email, message } = req.body;

    // Create a new instance of the model with the submitted data
    const newContact = new Contact({
        name,
        email,
        message
    });

    // Save the new data to MongoDB
    newContact.save()
        .then(() => {
            res.send('Thank you for contacting us! Your message has been received.');
        })
        .catch((err) => {
            console.error('Error saving data:', err);
            res.send('Something went wrong. Please try again later.');
        });
});

// Start the server
const port = 3000;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
