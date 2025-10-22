<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <router-link to="/" class="back-home">
          ← Retour à l'accueil
        </router-link>
        <h1>🔐 Connexion</h1>
        <p>Accède à ton espace freelancer</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="form.email"
            placeholder="exemple@email.com"
            required
          >
        </div>

        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            placeholder="Ton mot de passe"
            required
          >
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          <span v-if="loading">Connexion en cours...</span>
          <span v-else>🚀 Se connecter</span>
        </button>

        <div class="auth-footer">
          <p>Pas encore de compte ? <router-link to="/inscription">Inscris-toi ici</router-link></p>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''

      try {
        // Récupérer les utilisateurs depuis localStorage
        const users = JSON.parse(localStorage.getItem('freelancecm_users') || '[]')
        
        // Trouver l'utilisateur
        const user = users.find(u => u.email === this.form.email && u.password === this.form.password)
        
        if (!user) {
          this.error = 'Email ou mot de passe incorrect'
          this.loading = false
          return
        }

        // Mettre à jour la date de dernière connexion
        user.updatedAt = new Date().toISOString()
        localStorage.setItem('freelancecm_users', JSON.stringify(users))
        
        // Stocker l'utilisateur connecté
        localStorage.setItem('freelancecm_currentUser', JSON.stringify(user))
        
        // 🔥 Émettre l'événement pour mettre à jour la navigation
        this.$root.$emit('auth-change')
        
        // Redirection vers la page de profil ou tableau de bord
        this.$router.push('/profile')

         window.location.reload()
        
      } catch (error) {
        this.error = 'Une erreur est survenue lors de la connexion'
        console.error('Login error:', error)
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    // Vérifier si l'utilisateur est déjà connecté
    const currentUser = localStorage.getItem('freelancecm_currentUser')
    if (currentUser) {
      this.$router.push('/profile')
    }
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1d2d3a, #007a5e);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  font-family: "Poppins", sans-serif;
}

.auth-card {
  background: #1d2d3a;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 450px;
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.back-home {
  color: #ffe600;
  text-decoration: none;
  font-size: 0.9rem;
  margin-bottom: 20px;
  display: inline-block;
}

.back-home:hover {
  text-decoration: underline;
}

.auth-header h1 {
  color: #ffe600;
  font-size: 2rem;
  margin-bottom: 10px;
}

.auth-header p {
  color: #c8c8c8;
  font-size: 1rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  color: #ffe600;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input {
  padding: 12px 15px;
  border: 2px solid #263845;
  border-radius: 8px;
  background: #0f1f2d;
  color: white;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #ffe600;
}

.form-group input::placeholder {
  color: #8a8a8a;
}

.btn-primary {
  background-color: #ffe600;
  color: #1d2d3a;
  border: none;
  padding: 15px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 10px;
}

.btn-primary:hover:not(:disabled) {
  background-color: #ffcc00;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  background: #ff4444;
  color: white;
  padding: 12px;
  border-radius: 8px;
  text-align: center;
  font-size: 0.9rem;
}

.auth-footer {
  text-align: center;
  margin-top: 20px;
}

.auth-footer p {
  color: #c8c8c8;
}

.auth-footer a {
  color: #ffe600;
  text-decoration: none;
}

.auth-footer a:hover {
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 480px) {
  .auth-card {
    padding: 30px 20px;
  }
  
  .auth-header h1 {
    font-size: 1.6rem;
  }
}
</style>