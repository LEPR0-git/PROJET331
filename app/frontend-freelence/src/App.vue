<template>
  <div id="app">
    <header>
      <nav>
        <router-link to="/users">Utilisateurs</router-link> |
        <router-link to="/profiles">Profils Freelance</router-link>
      </nav>
    </header>

    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

header nav {
  margin-bottom: 2rem;
}

header nav a {
  text-decoration: none;
  color: #42b983;
  margin-right: 1rem;
}

header nav a.router-link-active {
  font-weight: bold;
  color: #35495e;
}

main {
  min-height: 400px;
}
</style>

<!-- <script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div>
    <a href="https://vite.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld msg="Vite + Vue" />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style> -->
