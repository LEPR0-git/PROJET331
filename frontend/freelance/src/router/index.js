
 import { createRouter , createWebHistory } from "vue-router";
import Home from "../components/home.vue";
import inscription from "../components/views/inscription.vue";
import connexion from "../components/views/connexion.vue";
import profils from "../components/views/profils.vue";
 const routes = [
    {
        path:'/',
        name:"home",
        component:Home
    },
    {
      path:'/inscription',
      name:"inscription",
      component:inscription
    },
    {
      path:'/connexion',
      name:"connexion",
      component:connexion
    },
    {
      path:'/profile',
      name:"profils",
      component:profils
    }
 ]

 const router = createRouter({
    history:createWebHistory(),
    routes
 })

 export default router ;