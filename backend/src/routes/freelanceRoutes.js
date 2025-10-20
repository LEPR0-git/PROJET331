const express = require("express");
const router = express.Router();
const freelanceController = require("../controllers/freelanceController");

// Routes pour la gestion des profils freelances
router.get('/profiles', freelanceController.getAllProfiles);
router.get('/profiles/:id', freelanceController.getProfileById);
router.post('/profiles', freelanceController.createProfile);
router.put('/profiles/:id', freelanceController.updateProfile);
router.delete('/profiles/:id', freelanceController.deleteProfile);

// Routes pour le portfolio 
router.post('/profiles/:id/portfolio', freelanceController.addPortfolioItem);
router.delete('/portfolio/:itemId', freelanceController.removePortfolioItem);

module.exports = router;