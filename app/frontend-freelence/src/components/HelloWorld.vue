<!-- 
<template>
  <div>
    <h2>Liste des utilisateurs</h2>
    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.email }} - {{ user.role }}
      </li>
    </ul>
  </div>
</template>

<script>
import api from '../api';

export default {
  data() {
    return {
      users: [],
    };
  },
  async mounted() {
    try {
      const res = await api.get('/users');
      this.users = res.data.data;
    } catch (err) {
      console.error(err);
    }
  },
};
</script>
<template>
  <div>
    <h2>Liste des profils freelances</h2>
    <ul>
      <li v-for="profile in profiles" :key="profile.id">
        {{ profile.first_name }} {{ profile.last_name }} - {{ profile.title || 'N/A' }}
      </li>
    </ul>
  </div>
</template> -->

<!-- <script>
import api from '../api';

export default {
  data() {
    return {
      profiles: [],
    };
  },
  async mounted() {
    try {
      const res = await api.get('/freelance/profiles');
      this.profiles = res.data.data;
    } catch (err) {
      console.error(err);
    }
  },
};
</script> -->


<!-- <script setup>
import { ref }<template>
  <div>
    <h2>Liste des utilisateurs</h2>
    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.email }} - {{ user.role }}
      </li>
    </ul>
  </div>
</template>

<script>
import api from '../api';

export default {
  data() {
    return {
      users: [],
    };
  },
  async mounted() {
    try {
      const res = await api.get('/users');
      this.users = res.data.data;
    } catch (err) {
      console.error(err);
    }
  },
};
</script>

defineProps({
  msg: String,
})

const count = ref(0)
</script>

<template>
  <h1>{{ msg }}</h1>

  <div class="card">
    <button type="button" @click="count++">count is {{ count }}</button>
    <p>
      Edit
      <code>components/HelloWorld.vue</code> to test HMR
    </p>
  </div>

  <p>
    Check out
    <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank"
      >create-vue</a
    >, the official Vue + Vite starter
  </p>
  <p>
    Learn more about IDE Support for Vue in the
    <a
      href="https://vuejs.org/guide/scaling-up/tooling.html#ide-support"
      target="_blank"
      >Vue Docs Scaling up Guide</a
    >.
  </p>
  <p class="read-the-docs">Click on the Vite and Vue logos to learn more</p>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style> -->
