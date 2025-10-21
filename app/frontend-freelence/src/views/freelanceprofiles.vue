<template>
  <div class="freelance-page">
    <h1>Profils Freelance</h1>

    <!-- Formulaire création profil -->
    <form @submit.prevent="addProfile">
      <input v-model="newProfile.userId" type="number" placeholder="ID Utilisateur" required />
      <input v-model="newProfile.firstName" placeholder="Prénom" required />
      <input v-model="newProfile.lastName" placeholder="Nom" required />
      <input v-model="newProfile.title" placeholder="Titre" />
      <input v-model="newProfile.description" placeholder="Description" />
      <input v-model="newProfile.skills" placeholder="Compétences (séparées par virgule)" />
      <input v-model.number="newProfile.hourlyRate" type="number" placeholder="Taux horaire" />
      <select v-model="newProfile.availability">
        <option value="AVAILABLE">Disponible</option>
        <option value="UNAVAILABLE">Indisponible</option>
        <option value="PART_TIME">Temps partiel</option>
      </select>
      <button type="submit">Ajouter</button>
    </form>

    <hr />

    <!-- Filtres -->
    <div class="filters">
      <input v-model="filterSkills" placeholder="Filtrer par compétences (virgule)" />
      <select v-model="filterAvailability">
        <option value="">Toutes les disponibilités</option>
        <option value="AVAILABLE">Disponible</option>
        <option value="UNAVAILABLE">Indisponible</option>
        <option value="PART_TIME">Temps partiel</option>
      </select>
      <button @click="fetchProfiles">Filtrer</button>
    </div>

    <!-- Liste profils -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Utilisateur ID</th>
          <th>Nom</th>
          <th>Titre</th>
          <th>Compétences</th>
          <th>Taux horaire</th>
          <th>Disponibilité</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="profile in profiles" :key="profile.id">
          <td>{{ profile.id }}</td>
          <td>{{ profile.user_id }}</td>
          <td>
            <input v-model="profile.first_name" />
            <input v-model="profile.last_name" />
          </td>
          <td><input v-model="profile.title" /></td>
          <td><input v-model="profile.skillsString" /></td>
          <td><input v-model.number="profile.hourly_rate" type="number" /></td>
          <td>
            <select v-model="profile.availability">
              <option value="AVAILABLE">Disponible</option>
              <option value="UNAVAILABLE">Indisponible</option>
              <option value="PART_TIME">Temps partiel</option>
            </select>
          </td>
          <td>
            <button @click="updateProfile(profile)">Modifier</button>
            <button @click="deleteProfile(profile.id)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { 
  getProfiles, 
  createProfile, 
  updateProfile as apiUpdateProfile, 
  deleteProfile as apiDeleteProfile 
} from '../api';

export default {
  name: 'FreelanceProfiles',
  data() {
    return {
      profiles: [],
      newProfile: {
        userId: '',
        firstName: '',
        lastName: '',
        title: '',
        description: '',
        skills: '',
        hourlyRate: null,
        availability: 'AVAILABLE'
      },
      filterSkills: '',
      filterAvailability: ''
    };
  },
  methods: {
    async fetchProfiles() {
      try {
        const params = {};
        if (this.filterSkills) params.skills = this.filterSkills;
        if (this.filterAvailability) params.availability = this.filterAvailability;

        const res = await getProfiles(params);
        if (res.data.success) {
          this.profiles = res.data.data.map(p => ({
            ...p,
            skillsString: p.skills.join(', ')
          }));
        }
      } catch (err) {
        console.error(err);
        alert("Erreur lors du chargement des profils");
      }
    },
    async addProfile() {
      try {
        const data = {
          userId: this.newProfile.userId,
          firstName: this.newProfile.firstName,
          lastName: this.newProfile.lastName,
          title: this.newProfile.title,
          description: this.newProfile.description,
          skills: this.newProfile.skills.split(',').map(s => s.trim()).filter(s => s),
          hourlyRate: this.newProfile.hourlyRate,
          availability: this.newProfile.availability
        };
        const res = await createProfile(data);
        if (res.data.success) {
          this.fetchProfiles();
          Object.assign(this.newProfile, { userId:'', firstName:'', lastName:'', title:'', description:'', skills:'', hourlyRate:null, availability:'AVAILABLE' });
        } else {
          alert(res.data.message);
        }
      } catch (err) {
        console.error(err);
        alert("Erreur lors de la création du profil");
      }
    },
    async updateProfile(profile) {
      try {
        const data = {
          firstName: profile.first_name,
          lastName: profile.last_name,
          title: profile.title,
          skills: profile.skillsString.split(',').map(s => s.trim()).filter(s => s),
          hourlyRate: profile.hourly_rate,
          availability: profile.availability
        };
        const res = await apiUpdateProfile(profile.id, data);
        if (!res.data.success) {
          alert(res.data.message);
        }
      } catch (err) {
        console.error(err);
        alert("Erreur lors de la mise à jour du profil");
      }
    },
    async deleteProfile(profileId) {
      if (!confirm("Voulez-vous vraiment supprimer ce profil ?")) return;
      try {
        const res = await apiDeleteProfile(profileId);
        if (res.data.success) {
          this.profiles = this.profiles.filter(p => p.id !== profileId);
        } else {
          alert(res.data.message);
        }
      } catch (err) {
        console.error(err);
        alert("Erreur lors de la suppression du profil");
      }
    }
  },
  mounted() {
    this.fetchProfiles();
  }
};
</script>

<style scoped>
.freelance-page {
  max-width: 900px;
  margin: auto;
  padding: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table th, table td {
  padding: 0.5rem;
  border: 1px solid #ccc;
}

input, select {
  padding: 0.3rem;
  margin-right: 0.3rem;
}

.filters {
  margin-bottom: 1rem;
}
</style>
