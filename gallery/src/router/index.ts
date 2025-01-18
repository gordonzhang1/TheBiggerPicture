 mosaicswitch
import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import Mosaic from "../views/Mosaic.vue";

 main

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
mosaicswitch
      path: "/mosaic",
      name: "mosaic",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: Mosaic,
 main
    },
  ],
});

export default router;
