const {PrismaClient} = require("@prisma/client")


const prisma = new PrismaClient()


// test de connection 
async function testConnection() {
    try{
        await prisma.$connect();
        console.log("Connecter a postgreSQL avec prisma")
        return true
    } catch(error){
        console.log("erreur de connection a la BD avec prisma: ",error)
        return false
    }
}


module.exports = { prisma , testConnection};

