const express = require('express'); 
const cors = require('cors');
require('dotenv').config()

const {testConnection} = require("./config/databases");
const freelanceRoutes = require('./src/routes/freelanceRoutes')

const app = express()

const PORT = process.env.PORT || 3000;

// middleware

app.use(cors());
app.use(express.json())

// teste de connection au demarage

testConnection();


// Routes
app.use('/api/freelance', freelanceRoutes);

// Route de santé
app.get('/health', async (req, res) => {
  try {
    const { prisma } = require("./config/database");
    await prisma.$queryRaw`SELECT 1`;
    res.json({ 
      status: 'OK', 
      database: 'Connected',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ 
      status: 'ERROR', 
      database: 'Disconnected',
      error: error.message 
    });
  }
});

// Route par défaut
app.get('/', (req, res) => {
  res.json({
    message: ' API Freelance Platform - Module 1: Gestion Freelances',
    status: 'OK',
    timestamp: new Date().toISOString(),
    endpoints: {
      freelances: '/api/freelance/profiles',
      health: '/health'
    }
  });
});

// Demarage du serveur 

app.listen(PORT, ()=>{
    console.log("serveur demarer ! http://localhost:",PORT);
    console.log("sante de la BD! http://localhost:",PORT,"/health");
    console.log("prisma studion : npx prisma studio");
})