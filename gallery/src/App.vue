<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import ItemGrid from './components/ItemGrid.vue';

import { useAuth0 } from '@auth0/auth0-vue';

// Using the auth0 hook for authentication

const { loginWithRedirect, user, isAuthenticated } = useAuth0();
const { logout } = useAuth0();

// Login method (directly in the setup)
function login() {
  loginWithRedirect();
}

function logOut(){
  
  logout({ logoutParams: { returnTo: window.location.origin } });
        
}

</script>

<template>
  <nav class="nav">
    <div> 
      <button @click="login">Log in</button>
      <pre>
        <code>{{ user.email }}</code>
      </pre>
    </div>
    <button @click="logOut">Log out</button>

    <RouterLink to="/">DASHBOARD</RouterLink>
    <RouterLink to="/mosaic">MOSAIC</RouterLink>
  </nav>

  <HelloWorld class="hello-world" />

  <div class="item-grid-container">
    <ItemGrid class="item-grid">
      <RouterView class="router-view" />
    </ItemGrid>
  </div>
</template>

<style scoped>
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
}

.item-grid-container {
  padding: 2rem;
}

.nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #4c7467;
  padding: 1rem;
  display: flex;
  gap: 1rem;
  z-index: 1000;
}

.nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.nav a:hover {
  background-color: #34495e;
}

.hello-world {
  display: flex;
  align-items: center;
  padding: 2rem;
  margin-top: 5rem; /* Adjust based on the navbar height */
}

.router-view {
  margin-top: 2rem;
}
</style>
