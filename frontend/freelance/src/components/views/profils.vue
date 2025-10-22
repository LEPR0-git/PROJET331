<template>
  <div class="profile-container">
    <!-- Header avec navigation -->
    <div class="profile-header">
      <div class="container">
        <nav class="breadcrumb">
          <router-link to="/" class="back-link">
            <span class="back-arrow">←</span>
            Retour à l'accueil
          </router-link>
        </nav>
        <div class="header-content">
          <h1 class="page-title">
            <span class="avatar-icon">👤</span>
            Mon Profil
          </h1>
          <p class="page-subtitle">Gérez votre identité et vos préférences sur FreelanceCM</p>
        </div>
      </div>
    </div>

    <!-- Contenu principal -->
    <div class="container profile-content">
      <div class="profile-layout">
        
        <!-- Colonne principale - Formulaire -->
        <main class="profile-main">
          <!-- Carte Informations personnelles -->
          <section class="profile-card">
            <div class="card-header">
              <h2>📝 Informations personnelles</h2>
              <div class="edit-toggle" v-if="!isEditing">
                <button class="btn-edit" @click="startEditing">
                  <span class="edit-icon">✏️</span>
                  Modifier
                </button>
              </div>
            </div>

            <div class="avatar-section">
              <div class="avatar-container">
                <div class="avatar" :style="avatarStyle">
                  {{ userInitials }}
                </div>
                <div class="avatar-info">
                  <p class="avatar-name">{{ form.fullName || 'Nom non renseigné' }}</p>
                  <p class="avatar-role">{{ form.profession || 'Métier non spécifié' }}</p>
                </div>
              </div>
              <button class="btn-avatar" @click="editAvatar = true">
                <span class="camera-icon">📷</span>
                Changer la photo
              </button>
            </div>

            <form @submit.prevent="updateProfile" class="profile-form">
              <div class="form-grid">
                <div class="form-group">
                  <label for="fullName" class="form-label">Nom complet *</label>
                  <input
                    type="text"
                    id="fullName"
                    v-model="form.fullName"
                    :disabled="!isEditing"
                    placeholder="Votre nom complet"
                    class="form-input"
                  >
                </div>

                <div class="form-group">
                  <label for="email" class="form-label">Email *</label>
                  <input
                    type="email"
                    id="email"
                    v-model="form.email"
                    :disabled="!isEditing"
                    placeholder="votre@email.com"
                    class="form-input"
                  >
                </div>

                <div class="form-group">
                  <label for="profession" class="form-label">Métier principal</label>
                  <input
                    type="text"
                    id="profession"
                    v-model="form.profession"
                    :disabled="!isEditing"
                    placeholder="Ex: Développeur, Coiffeur, Maçon..."
                    class="form-input"
                  >
                </div>

                <div class="form-group">
                  <label for="city" class="form-label">Ville</label>
                  <select 
                    id="city" 
                    v-model="form.city" 
                    :disabled="!isEditing"
                    class="form-select"
                  >
                    <option value="">Sélectionnez votre ville</option>
                    <option value="douala">Douala</option>
                    <option value="yaounde">Yaoundé</option>
                    <option value="bafoussam">Bafoussam</option>
                    <option value="garoua">Garoua</option>
                    <option value="maroua">Maroua</option>
                    <option value="buea">Buéa</option>
                    <option value="autres">Autre ville</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="phone" class="form-label">Téléphone</label>
                  <input
                    type="tel"
                    id="phone"
                    v-model="form.phone"
                    :disabled="!isEditing"
                    placeholder="6XX XXX XXX"
                    class="form-input"
                  >
                </div>

                <div class="form-group full-width">
                  <label for="description" class="form-label">Description professionnelle</label>
                  <textarea
                    id="description"
                    v-model="form.description"
                    :disabled="!isEditing"
                    placeholder="Décrivez votre métier, vos compétences, votre expérience..."
                    rows="4"
                    class="form-textarea"
                  ></textarea>
                  <div class="char-count" v-if="isEditing">
                    {{ form.description.length }}/500 caractères
                  </div>
                </div>
              </div>

              <!-- Actions du formulaire -->
              <div class="form-actions" v-if="isEditing">
                <button type="submit" class="btn-save" :disabled="saving">
                  <span class="save-icon" v-if="!saving">💾</span>
                  <span class="loading-spinner" v-else>⏳</span>
                  {{ saving ? 'Sauvegarde...' : 'Sauvegarder les modifications' }}
                </button>
                <button type="button" class="btn-cancel" @click="cancelEditing">
                  <span class="cancel-icon">❌</span>
                  Annuler
                </button>
              </div>
            </form>
          </section>

          <!-- Carte Sécurité -->
          <section class="profile-card">
            <h2>🔒 Sécurité du compte</h2>
            <div class="security-actions">
              <button class="btn-security" @click="changePassword = true">
                <span class="security-icon">🔑</span>
                <div class="security-info">
                  <strong>Changer le mot de passe</strong>
                  <span>Mettez à jour votre mot de passe régulièrement</span>
                </div>
              </button>
              <button class="btn-logout" @click="handleLogout">
                <span class="logout-icon">🚪</span>
                <div class="security-info">
                  <strong>Se déconnecter</strong>
                  <span>Quitter votre session en cours</span>
                </div>
              </button>
            </div>
          </section>
        </main>

        <!-- Sidebar -->
        <aside class="profile-sidebar">
          <!-- Statistiques -->
          <section class="sidebar-card">
            <h3>📊 Activité</h3>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">0</div>
                <div class="stat-label">Prestations</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">0</div>
                <div class="stat-label">Avis reçus</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">—</div>
                <div class="stat-label">Note moyenne</div>
              </div>
            </div>
          </section>

          <!-- Actions rapides -->
          <section class="sidebar-card">
            <h3>🚀 Actions rapides</h3>
            <div class="quick-actions">
              <router-link to="/freelances" class="quick-action">
                <span class="action-icon">🔍</span>
                Trouver des prestataires
              </router-link>
              <router-link to="/services" class="quick-action">
                <span class="action-icon">💼</span>
                Publier mes services
              </router-link>
              <button class="quick-action" @click="shareProfile">
                <span class="action-icon">📤</span>
                Partager mon profil
              </button>
            </div>
          </section>

          <!-- Informations compte -->
          <section class="sidebar-card">
            <h3>📅 Informations compte</h3>
            <div class="account-info">
              <div class="info-item">
                <span class="info-label">Membre depuis :</span>
                <span class="info-value">{{ joinDate }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Dernière connexion :</span>
                <span class="info-value">{{ lastLogin }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Profil :</span>
                <span class="info-value">{{ form.profession || 'Non spécifié' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Localisation :</span>
                <span class="info-value">{{ form.city ? getCityName(form.city) : 'Non spécifiée' }}</span>
              </div>
            </div>
          </section>
        </aside>
      </div>
    </div>

    <!-- Modals -->
    <Modal v-if="editAvatar" @close="editAvatar = false">
      <template #header>
        <h3>Changer la photo de profil</h3>
      </template>
      <template #body>
        <p>Cette fonctionnalité sera bientôt disponible !</p>
        <p class="modal-hint">Vous pourrez bientôt uploader votre photo directement depuis votre appareil.</p>
      </template>
      <template #footer>
        <button class="btn-primary" @click="editAvatar = false">Compris</button>
      </template>
    </Modal>

    <Modal v-if="changePassword" @close="changePassword = false">
      <template #header>
        <h3>🔑 Changer le mot de passe</h3>
      </template>
      <template #body>
        <p>La modification du mot de passe sera disponible prochainement.</p>
        <p class="modal-hint">Pour votre sécurité, cette fonctionnalité est en cours de développement.</p>
      </template>
      <template #footer>
        <button class="btn-primary" @click="changePassword = false">Fermer</button>
      </template>
    </Modal>
  </div>
</template>

<script>
export default {
  name: 'ProfilePage',
  data() {
    return {
      user: null,
      form: {
        fullName: '',
        email: '',
        profession: '',
        city: '',
        phone: '',
        description: ''
      },
      originalForm: {},
      isEditing: false,
      saving: false,
      editAvatar: false,
      changePassword: false
    }
  },
  computed: {
    userInitials() {
      if (!this.form.fullName) return '👤'
      return this.form.fullName
        .split(' ')
        .map(name => name[0])
        .join('')
        .toUpperCase()
        .slice(0, 2)
    },
    avatarStyle() {
      return {
        background: 'linear-gradient(135deg, #ffe600, #ffcc00)',
        color: '#1d2d3a'
      }
    },
    joinDate() {
      if (!this.user?.createdAt) return 'Date inconnue'
      return new Date(this.user.createdAt).toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    },
    lastLogin() {
      if (!this.user?.updatedAt) return 'Jamais'
      return new Date(this.user.updatedAt).toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  },
  methods: {
    loadUserData() {
      const userData = localStorage.getItem('freelancecm_currentUser')
      if (!userData) {
        this.$router.push('/connexion')
        return
      }

      this.user = JSON.parse(userData)
      this.initializeForm()
    },
    initializeForm() {
      this.form = {
        fullName: this.user.fullName || '',
        email: this.user.email || '',
        profession: this.user.profession || '',
        city: this.user.city || '',
        phone: this.user.phone || '',
        description: this.user.description || ''
      }
      this.originalForm = { ...this.form }
    },
    startEditing() {
      this.isEditing = true
    },
    cancelEditing() {
      this.form = { ...this.originalForm }
      this.isEditing = false
    },
    async updateProfile() {
      this.saving = true

      try {
        // Validation
        if (!this.form.fullName.trim() || !this.form.email.trim()) {
          alert('❌ Le nom et l\'email sont obligatoires')
          return
        }

        // Mettre à jour les données
        const users = JSON.parse(localStorage.getItem('freelancecm_users') || '[]')
        const userIndex = users.findIndex(u => u.id === this.user.id)
        
        if (userIndex !== -1) {
          users[userIndex] = {
            ...users[userIndex],
            ...this.form,
            updatedAt: new Date().toISOString()
          }
          localStorage.setItem('freelancecm_users', JSON.stringify(users))
        }

        // Mettre à jour l'utilisateur courant
        this.user = {
          ...this.user,
          ...this.form,
          updatedAt: new Date().toISOString()
        }
        localStorage.setItem('freelancecm_currentUser', JSON.stringify(this.user))

        this.originalForm = { ...this.form }
        this.isEditing = false
        
        this.showNotification('✅ Profil mis à jour avec succès !', 'success')
        
      } catch (error) {
        console.error('Error updating profile:', error)
        this.showNotification('❌ Erreur lors de la mise à jour du profil', 'error')
      } finally {
        this.saving = false
      }
    },
    handleLogout() {
      if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
        localStorage.removeItem('freelancecm_currentUser')
        window.location.href = '/'
      }
    },
    shareProfile() {
      const profileUrl = `${window.location.origin}/profile/${this.user.id}`
      if (navigator.share) {
        navigator.share({
          title: `Profil de ${this.form.fullName} - FreelanceCM`,
          text: `Découvrez le profil de ${this.form.fullName} sur FreelanceCM`,
          url: profileUrl
        })
      } else {
        navigator.clipboard.writeText(profileUrl)
        this.showNotification('✅ Lien du profil copié dans le presse-papier !', 'success')
      }
    },
    getCityName(cityKey) {
      const cities = {
        douala: 'Douala',
        yaounde: 'Yaoundé',
        bafoussam: 'Bafoussam',
        garoua: 'Garoua',
        maroua: 'Maroua',
        buea: 'Buéa',
        autres: 'Autre ville'
      }
      return cities[cityKey] || cityKey
    },
    showNotification(message, type = 'info') {
      // Implémentation simple d'une notification
      const notification = document.createElement('div')
      notification.className = `notification notification-${type}`
      notification.textContent = message
      notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        background: ${type === 'success' ? '#007a5e' : '#ff4444'};
        color: white;
        border-radius: 8px;
        z-index: 10000;
        animation: slideIn 0.3s ease;
      `
      document.body.appendChild(notification)
      setTimeout(() => {
        notification.remove()
      }, 3000)
    }
  },
  mounted() {
    this.loadUserData()
  }
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f1f2d 0%, #1d2d3a 100%);
  color: white;
  font-family: "Poppins", sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Header amélioré */
.profile-header {
  background: linear-gradient(135deg, #007a5e 0%, #1d2d3a 100%);
  padding: 30px 0;
  border-bottom: 1px solid #263845;
}

.breadcrumb {
  margin-bottom: 20px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #ffe600;
  text-decoration: none;
  font-size: 0.9rem;
  transition: opacity 0.3s ease;
}

.back-link:hover {
  opacity: 0.8;
}

.back-arrow {
  font-size: 1.1rem;
}

.header-content {
  text-align: center;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: #ffe600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.avatar-icon {
  font-size: 2.2rem;
}

.page-subtitle {
  color: #c8c8c8;
  font-size: 1.1rem;
  line-height: 1.5;
}

/* Layout principal */
.profile-content {
  padding: 40px 0;
}

.profile-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  align-items: start;
}

/* Cartes */
.profile-card, .sidebar-card {
  background: #1d2d3a;
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid #263845;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.profile-card:hover, .sidebar-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
}

.profile-card h2, .sidebar-card h3 {
  color: #ffe600;
  margin-bottom: 25px;
  font-size: 1.3rem;
  font-weight: 600;
}

/* En-tête de carte avec bouton edit */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.btn-edit {
  background: #ffe600;
  color: #1d2d3a;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-edit:hover {
  background: #ffcc00;
  transform: translateY(-1px);
}

/* Section avatar améliorée */
.avatar-section {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 25px;
  border-bottom: 1px solid #263845;
}

.avatar-container {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  justify-content: center;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: bold;
  flex-shrink: 0;
}

.avatar-info {
  text-align: left;
}

.avatar-name {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 5px;
  color: white;
}

.avatar-role {
  color: #c8c8c8;
  font-size: 0.9rem;
}

.btn-avatar {
  background: transparent;
  color: #ffe600;
  border: 2px solid #ffe600;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-avatar:hover {
  background: #ffe600;
  color: #1d2d3a;
}

/* Formulaire amélioré */
.profile-form {
  margin-top: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  display: block;
  color: #ffe600;
  margin-bottom: 8px;
  font-weight: 500;
  font-size: 0.9rem;
}

.form-input, .form-select, .form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #263845;
  border-radius: 8px;
  background: #0f1f2d;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none;
  border-color: #ffe600;
  box-shadow: 0 0 0 3px rgba(255, 230, 0, 0.1);
}

.form-input:disabled, .form-select:disabled, .form-textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: #1a2835;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.char-count {
  text-align: right;
  font-size: 0.8rem;
  color: #8a8a8a;
  margin-top: 5px;
}

/* Actions du formulaire */
.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #263845;
}

.btn-save, .btn-cancel {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-save {
  background: #ffe600;
  color: #1d2d3a;
  flex: 1;
}

.btn-save:hover:not(:disabled) {
  background: #ffcc00;
  transform: translateY(-1px);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: transparent;
  color: #ff6b6b;
  border: 2px solid #ff6b6b;
}

.btn-cancel:hover {
  background: #ff6b6b;
  color: white;
}

/* Section sécurité */
.security-actions {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.btn-security, .btn-logout {
  background: transparent;
  border: 2px solid #263845;
  padding: 15px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 15px;
  text-align: left;
  width: 100%;
}

.btn-security:hover {
  border-color: #ffe600;
  background: rgba(255, 230, 0, 0.1);
}

.btn-logout {
  border-color: #ff4444;
  color: #ff6b6b;
}

.btn-logout:hover {
  background: #ff4444;
  color: white;
}

.security-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.security-info strong {
  font-size: 1rem;
}

.security-info span {
  font-size: 0.8rem;
  color: #8a8a8a;
}

.security-icon, .logout-icon {
  font-size: 1.2rem;
}

/* Sidebar */
.sidebar-card {
  background: #1d2d3a;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.stat-item {
  text-align: center;
  padding: 15px 10px;
  background: #263845;
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ffe600;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.8rem;
  color: #c8c8c8;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quick-action {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 15px;
  background: #263845;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  font-family: inherit;
  font-size: 0.9rem;
}

.quick-action:hover {
  background: #2d4150;
  transform: translateX(5px);
}

.action-icon {
  font-size: 1.1rem;
}

.account-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid #263845;
}

.info-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.info-label {
  color: #c8c8c8;
  font-size: 0.9rem;
}

.info-value {
  color: white;
  font-weight: 500;
  font-size: 0.9rem;
  text-align: right;
}

/* Responsive */
@media (max-width: 968px) {
  .profile-layout {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .avatar-container {
    flex-direction: column;
    text-align: center;
  }
  
  .avatar-info {
    text-align: center;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 15px;
  }
  
  .profile-header {
    padding: 20px 0;
  }
  
  .page-title {
    font-size: 1.8rem;
  }
  
  .profile-card, .sidebar-card {
    padding: 20px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 480px) {
  .card-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
  
  .btn-edit {
    justify-content: center;
  }
  
  .security-actions {
    gap: 10px;
  }
  
  .btn-security, .btn-logout {
    padding: 12px 15px;
  }
}

/* Animations */
@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>