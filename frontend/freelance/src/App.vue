<template>
  <section class="header">
    <div class="logo">
      🇨🇲 FreelanceCM
    </div>

    <!-- Bouton burger -->
    <div class="burger" @click="toggleMenu">
      <span :class="{ active: isOpen }"></span>
      <span :class="{ active: isOpen }"></span>
      <span :class="{ active: isOpen }"></span>
    </div>
    
    <!-- Liens de navigation -->
    <div class="nav-links" :class="{ open: isOpen }">
      <router-link to="/freelances" class="nav-link">Trouver un freelance</router-link>
      
      <!-- Liens conditionnels selon l'état de connexion -->
      <template v-if="isLoggedIn">
        <router-link to="/profile" class="nav-link">Mon Profil</router-link>
        <button @click="handleLogout" class="nav-link logout-btn">Se déconnecter</button>
      </template>
      <template v-else>
        <router-link to="/inscription" class="nav-link">Créer mon compte</router-link>
        <router-link to="/connexion" class="nav-link">Me connecter</router-link>
      </template>
      
      <router-link to="/language" class="nav-link">FR</router-link>
    </div>
  </section>

  <router-view/>

</template>

<script>
export default {
  name: 'AppHeader',
  data() {
    return {
      isOpen: false,
      isLoggedIn: false
    }
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen
    },
    
    checkAuthStatus() {
      // Vérifier si un utilisateur est connecté dans localStorage
      const user = localStorage.getItem('freelancecm_currentUser')
      this.isLoggedIn = !!user
      console.log('Auth status checked:', this.isLoggedIn) // Pour debug
    },
    
    handleLogout() {
      if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
        localStorage.removeItem('freelancecm_currentUser')
        this.isLoggedIn = false
        this.isOpen = false
        
        // Émettre l'événement pour synchroniser
        this.$root.$emit('auth-change')
        
        // Rediriger vers la page d'accueil si on est sur une page protégée
        if (this.$route.path === '/profile') {
          this.$router.push('/')
        }
      }
    },
    
    // Nouvelle méthode pour écouter les événements
    setupAuthListener() {
      // Écouter les événements d'authentification
      this.$root.$on('auth-change', () => {
        console.log('Auth change event received') // Pour debug
        this.checkAuthStatus()
      })
    }
  },
  mounted() {
    this.checkAuthStatus()
    this.setupAuthListener()
    
    // Écouter les changements de route pour fermer le menu mobile
    this.$router.afterEach(() => {
      this.isOpen = false
    })
  },
  beforeDestroy() {
    // Nettoyer l'écouteur d'événements
    this.$root.$off('auth-change')
  }
}
</script>

<style scoped>
/* Votre CSS existant reste inchangé */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 50px;
  border-bottom: 1px solid #cecdcd;
  font-size: 18px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #1d2d3a;
  color: white;
  position:sticky;
  top:0;
  z-index: 10;
}

.logo {
  font-weight: bold;
  font-size: 1.4rem;
  color: #ffe600;
}

/* Nav Desktop */
.nav-links {
  display: flex;
  gap: 15px;
  align-items: center;
  transition: all 0.3s ease;
}

.nav-link {
  margin-left: 10px;
  padding: 8px 15px;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  border: 1px solid #7a7878;
  color: white;
  transition: all 0.3s;
  text-decoration: none;
  box-shadow: 0px 0px 3px 3px rgb(52, 47, 47) inset;
  background: none;
  font-family: inherit;
}

.nav-link:hover {
  background-color: #232323;
  transform: translateY(-2px);
}

.nav-link.router-link-active {
  background-color: #007a5e;
  border-color: #007a5e;
}

/* Style spécifique pour le bouton de déconnexion */
.logout-btn {
  background-color: #ff4444;
  border-color: #ff4444;
  color: white;
}

.logout-btn:hover {
  background-color: #cc3333;
  border-color: #cc3333;
}

/* Burger Menu */
.burger {
  display: none;
  flex-direction: column;
  cursor: pointer;
  width: 25px;
  height: 20px;
  justify-content: space-between;
}

.burger span {
  background: #ffe600;
  height: 3px;
  width: 100%;
  border-radius: 2px;
  transition: 0.3s;
}

/* Animation du burger */
.burger span.active:nth-child(1) {
  transform: rotate(45deg) translateY(8px);
}
.burger span.active:nth-child(2) {
  opacity: 0;
}
.burger span.active:nth-child(3) {
  transform: rotate(-45deg) translateY(-8px);
}

/* Responsive */
@media (max-width: 768px) {
  .header {
    padding: 20px 25px;
  }

  .burger {
    display: flex;
  }

  .nav-links {
    position: absolute;
    top: 100%;
    left: 0;
    background-color: #1d2d3a;
    flex-direction: column;
    width: 100%;
    text-align: center;
    padding: 15px 0;
    gap: 10px;
    border-top: 1px solid #3a3a3a;
    display: none;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  }

  .nav-links.open {
    display: flex;
  }

  .nav-link {
    width: 80%;
    margin: 5px auto;
    padding: 12px 15px;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 15px 20px;
  }
  
  .logo {
    font-size: 1.2rem;
  }
}
</style>