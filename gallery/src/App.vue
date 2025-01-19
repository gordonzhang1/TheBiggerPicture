<script setup lang="ts">

import { RouterLink, RouterView, useRouter } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import ItemGrid from './components/ItemGrid.vue';

import { useAuth0 } from '@auth0/auth0-vue';
import { watch } from 'vue';
import { backendData } from './stores/backend-data';

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

const router = useRouter();

async function createNewMosaic() {
  console.log(user.value)

  if (!user.value || !user.value.email) {
    return;
  }

  const formData = new FormData();

  formData.append('image_name', 'New Mosaic');
  formData.append('user', user.value.email);

  const res = await fetch('https://uofthacks-12.onrender.com/api/create-category', {
    method: 'POST',
    body: formData
  });

  const json = await res.json();

  const id = json.id;
  
  router.push(`/mosaic/${id}`);
}

async function fetchData(email: string | undefined) {
  console.log('hey');
  if (!email) {
    return;
  }

  const data = new FormData();

  data.append('user', email);

  const res = await fetch('https://uofthacks-12.onrender.com/api/get-mosaics', {
    method: 'POST',
    body: data
  });

  const json = await res.json();

  backendData.mosaics = json.ids.map((id: number, i: number) => ({
    id,
    image_name: json.image_names[i],
    url: json.urls[i]
  }));
}

watch(() => user.value && user.value.email, fetchData, { immediate: true })

</script>

<template>
  <div class="main-container">
    <!-- Show log in button only if user is not authenticated -->
    <div v-if="!isAuthenticated" class="login-button">
      <div class="greetings">
     <h1>
      <strong>The Bigger Picture.</strong>
     </h1>
      <h3>
        A more meaningful way to share your photos.
      </h3>
     </div>
      <RouterLink to="/dashboard" @click="login">LOGIN</RouterLink>
    </div>

    <nav class="nav">
      <RouterLink to="/dashboard">DASHBOARD</RouterLink>
      <a @click="createNewMosaic" class="manual-router-link">MOSAIC</a>
      <h1>{{ user ? user.email : null }}</h1>
      <a href="#" v-if="isAuthenticated" @click="logOut">Log Out</a>
    </nav>

    <!-- The main router view where your page content will be rendered -->
    <RouterView class="router-view" />
  </div>

</template>

<style scoped>
body {
  width: 100%;
  height: 100%;
  margin: 0;
}

html {
    overflow: scroll;
    overflow-x: hidden;
}
::-webkit-scrollbar {
    width: 0;  /* Remove scrollbar space */
    background: transparent;  /* Optional: just make scrollbar invisible */
}
/* Optional: show position indicator in red */
::-webkit-scrollbar-thumb {
    background: #FF0000;
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
.router-view {
  margin-top: 2rem;
}

.manual-router-link {
  cursor: pointer;
}

.main-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 20px;
  margin-top: 5rem;
}

.nav a, .nav h1 {
  color: white;
}

.login-button {
  display: inline-flex;
  margin-top: 3rem;
  margin-bottom: 20px;
  background-color: #f0f0f0; /* Add some styling to make it visible */
  padding: 10px;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  width: 300px;
  height:100px;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
}

.login-button:hover {
  background-color: #e0e0e0;
  transition: all 0.3s ease;
  scale: 1.05;
} 

.greetings {
  margin-top: 10%;
  display: inline-flex;
  flex-direction: column;
  font-size: 2.5rem;
  font-weight:bold;
  text-align: center;
  color: aliceblue;
  gap: 2rem;
  margin-bottom: 1rem;
}

.greetings h3 {
  font-size: 1.5rem;
}

</style>