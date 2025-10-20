const { prisma } = require("../../config/databases");

class FreelanceController {

    // GET /api/freelance/profiles
    async getAllProfiles(req, res) {
        try {
            const { skills, availability, minRate, maxRate } = req.query;
            const filters = {};
            
            if (skills) filters.skills = { hasSome: skills.split(',') };
            if (availability) filters.availability = availability;
            if (minRate || maxRate) {
                filters.hourlyRate = {};
                if (minRate) filters.hourlyRate.gte = parseFloat(minRate);
                if (maxRate) filters.hourlyRate.lte = parseFloat(maxRate);
            }

            const profiles = await prisma.freelanceProfile.findMany({
                where: filters,
                include: {
                    user: {
                        select: { email: true, createdAt: true }
                    },
                    portfolioItems: true
                },
                orderBy: { createdAt: 'desc' }
            });

            res.json({
                success: true,
                data: profiles,
                count: profiles.length
            });

        } catch (error) {
            console.error('Error fetching profiles: ', error);
            res.status(500).json({
                success: false,
                message: "Erreur serveur lors de la récupération des profils"
            });
        }
    }

    // GET /api/freelance/profiles/:id
    async getProfileById(req, res) {
        try {
            const { id } = req.params;

            const profile = await prisma.freelanceProfile.findUnique({
                where: { id: parseInt(id) },
                include: {
                    user: {
                        select: { email: true, createdAt: true }
                    },
                    portfolioItems: {
                        orderBy: { createdAt: 'desc' }
                    }
                }
            });

            if (!profile) {
                return res.status(404).json({
                    success: false,
                    message: "Profil freelance non trouvé"
                });
            }

            res.json({
                success: true,
                data: profile
            });

        } catch (error) {
            console.error('Erreur lors du fetching Profile:', error);
            res.status(500).json({
                success: false,
                message: "Erreur Serveur"
            });
        }
    }

    // POST /api/freelance/profiles
    async createProfile(req, res) {
        try {
            const { userId, firstName, lastName, title, description, skills, hourlyRate, availability } = req.body;

            // Validation des données requises 
            if (!userId || !firstName || !lastName) {
                return res.status(400).json({
                    success: false,
                    message: 'userId, firstName et lastName sont requis !'
                });
            }

            const profile = await prisma.freelanceProfile.create({
                data: {
                    userId: parseInt(userId),
                    firstName,
                    lastName,
                    title,
                    description,
                    skills: skills || [],
                    hourlyRate: hourlyRate ? parseFloat(hourlyRate) : null,
                    availability: availability || "AVAILABLE"
                },
                include: {
                    user: {
                        select: { email: true }
                    },
                    portfolioItems: true
                }
            });

            res.status(201).json({
                success: true,
                message: "Profil créé avec succès",
                data: profile
            });

        } catch (error) {
            console.error("Error creating profile:", error);

            if (error.code === 'P2002') {
                return res.status(400).json({
                    success: false,
                    message: "Profil existant déjà pour cet utilisateur"
                });
            }

            res.status(500).json({
                success: false,
                message: "Erreur lors de la création du profil"
            });
        }
    }

    // PUT /api/freelance/profiles/:id
    async updateProfile(req, res) {
        try {
            const { id } = req.params;
            const { firstName, lastName, title, description, skills, hourlyRate, availability } = req.body;

            const profile = await prisma.freelanceProfile.update({
                where: { id: parseInt(id) },
                data: {
                    firstName,
                    lastName,
                    title,
                    description,
                    skills,
                    hourlyRate: hourlyRate ? parseFloat(hourlyRate) : null,
                    availability
                },
                include: {
                    user: {
                        select: { email: true }
                    },
                    portfolioItems: true
                }
            });

            res.json({
                success: true,
                message: "Profil mis à jour avec succès",
                data: profile
            });

        } catch (error) {
            console.error('Error updating profile:', error);
            res.status(500).json({
                success: false,
                message: "Erreur lors de la mise à jour du profil"
            });
        }
    }

    // DELETE /api/freelance/profiles/:id
    async deleteProfile(req, res) {
        try {
            const { id } = req.params;

            await prisma.freelanceProfile.delete({
                where: { id: parseInt(id) }
            });

            res.json({
                success: true,
                message: "Profil supprimé avec succès"
            });

        } catch (error) {
            console.error('Error deleting profile:', error);
            res.status(500).json({
                success: false,
                message: "Erreur lors de la suppression du profil"
            });
        }
    }

    // POST /api/freelance/profiles/:id/portfolio
    async addPortfolioItem(req, res) {
        try {
            const { id } = req.params;
            const { title, description, imageUrl, projectUrl } = req.body;

            if (!title) {
                return res.status(400).json({
                    success: false,
                    message: "Le titre est requis"
                });
            }

            const portfolioItem = await prisma.portfolioItem.create({
                data: {
                    title,
                    description,
                    imageUrl,
                    projectUrl,
                    freelanceProfileId: parseInt(id)
                }
            });

            res.status(201).json({
                success: true,
                message: "Élément de portfolio ajouté avec succès !",
                data: portfolioItem
            });

        } catch (error) {
            console.error('Error adding portfolio item:', error);
            res.status(500).json({
                success: false,
                message: "Erreur lors de l'ajout au portfolio"
            });
        }
    }

    // DELETE /api/freelance/portfolio/:itemId
    async removePortfolioItem(req, res) {
        try {
            const { itemId } = req.params;

            await prisma.portfolioItem.delete({
                where: { id: parseInt(itemId) }
            });

            res.json({
                success: true,
                message: "Élément de portfolio supprimé avec succès"
            });

        } catch (error) {
            console.error('Error removing portfolio item:', error);
            res.status(500).json({
                success: false,
                message: "Erreur lors de la suppression du portfolio"
            });
        }
    }
}

module.exports = new FreelanceController();