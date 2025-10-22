// main.js
import { createApp } from 'vue'

import './style.css'

import App from './App.vue'

import router from './router'  // Import du router

const app = createApp(App)

app.use(router)  // Utilise le router

app.mount('#app')
