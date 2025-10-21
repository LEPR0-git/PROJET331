import { createRouter, createWebHistory } from 'vue-router';
import Users from './views/user.vue';
import FreelanceProfiles from './views/freelanceprofiles.vue';

const routes = [
  { path: '/', redirect: '/users' },
  { path: '/users', component: Users },
  { path: '/profiles', component: FreelanceProfiles },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
