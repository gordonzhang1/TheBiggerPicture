
import { createRouter, createWebHistory } from "vue-router";
import Mosaic from "../views/Mosaic.vue";
import ItemDetail from "@/components/ItemDetail.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/item/:id', // Dynamic route with item ID
      name: 'item-detail',
      component: ItemDetail, // Replace with your ItemDetail component
      props: true, // Automatically pass the route params as props to the component
    },
    {
      path: '/mosaic',
      name: 'mosaic',
      component: () => import('../views/Mosaic.vue'),
    }
  ],
});

export default router
