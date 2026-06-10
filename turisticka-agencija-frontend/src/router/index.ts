import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", redirect: "/home" },
  { path: "/home", name: "home", component: {} },
  { path: "/dashboard", name: "dashboard", component: {} },
  { path: "/destinacije", name: "destinacije", component: {} },
  { path: "/klijenti", name: "klijenti", component: {} },
  { path: "/zaposlenici", name: "zaposlenici", component: {} },
  { path: "/rezervacije", name: "rezervacije", component: {} },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;