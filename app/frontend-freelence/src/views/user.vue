<template>
  <div class="users-page">
    <h1>Liste des utilisateurs</h1>

    <!-- Formulaire création utilisateur -->
    <form @submit.prevent="addUser">
      <input v-model="newUser.email" type="email" placeholder="Email" required />
      <input v-model="newUser.password" type="password" placeholder="Mot de passe" required />
      <select v-model="newUser.role">
        <option value="FREELANCE">Freelance</option>
        <option value="CLIENT">Client</option>
        <option value="ADMIN">Admin</option>
      </select>
      <button type="submit">Ajouter</button>
    </form>

    <hr />

    <!-- Liste utilisateurs -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Rôle</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td><input v-model="user.email" /></td>
          <td>
            <select v-model="user.role">
              <option value="FREELANCE">Freelance</option>
              <option value="CLIENT">Client</option>
              <option value="ADMIN">Admin</option>
            </select>
          </td>
          <td>
            <button @click="updateUser(user)">Modifier</button>
            <button @click="deleteUser(user.id)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { getUsers, createUser, updateUser as apiUpdateUser, deleteUser as apiDeleteUser } from '../api';

export default {
  name: 'Users',
  data() {
    return {
      users: [],
      newUser: {
        email: '',
        password: '',
        role: 'FREELANCE'
      }
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const res = await getUsers();
        if (res.data.success) this.users = res.data.data;
      } catch (err) {
        console.error(err);
        alert("Erreur lors du chargement des utilisateurs");
      }
    },
    async addUser() {
      try {
        const res = await createUser(this.newUser);
        if (res.data.success) {
          this.users.push(res.data.data);
          this.newUser.email = '';
          this.newUser.password = '';
        } else alert(res.data.message);
      } catch (err) {
        console.error(err);
        alert("Erreur lors de la création de l'utilisateur");
      }
    },
    async updateUser(user) {
      try {
        const res = await apiUpdateUser(user.id, { email: user.email, role: user.role });
        if (!res.data.success) alert(res.data.message);
      } catch (err) {
        console.error(err);
        alert("Erreur lors de la mise à jour de l'utilisateur");
      }
    },
    async deleteUser(userId) {
      if (!confirm("Voulez-vous vraiment supprimer cet utilisateur ?")) return;
      try {
        const res = await apiDeleteUser(userId);
        if (res.data.success) this.users = this.users.filter(u => u.id !== userId);
        else alert(res.data.message);
      } catch (err) {
        console.error(err);
        alert("Erreur lors de la suppression de l'utilisateur");
      }
    }
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.users-page {
  max-width: 800px;
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
</style>
