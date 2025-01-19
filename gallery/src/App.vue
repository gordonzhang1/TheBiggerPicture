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
    <div class="greetings-container" v-if="!isAuthenticated">
      <div class="greetings">
     <h1>
      <strong>The Bigger Picture.</strong>
     </h1>
      <h3>
        A more meaningful way to share your photos.
      </h3>
     </div>
      <RouterLink class="login-button" to="/dashboard" @click="login">Log In</RouterLink>
    </div>

    <nav class="nav">
      <RouterLink to="/dashboard">Dashboard</RouterLink>
      <a @click="createNewMosaic" class="manual-router-link">Create Mosaic</a>
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
  background-color: #dad9d9;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3rem;
  z-index: 1000;
}

.nav a,
.nav h1 {
  font-weight: 500;
  color: rgb(20, 20, 20);
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s ease;
  transition: all 0.3s ease;
  font-size: 1.2rem;

}

.nav a:hover {
  color: #000000;
  transition: all 0.3s ease;
  scale: 1.02;
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
}

.login-button {
  display: inline-flex;
  margin-top: 3rem;
  margin-bottom: 20px;
  background-color: rgb(231, 231, 231);
  padding: 10px;
  border-radius: 50px;
  color: #0c0c0c;
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
  background-color: rgb(190, 190, 190);
  transition: all 0.3s ease;
  scale: 1.05;
  /* glow effect */
  box-shadow: 0 0 30px #f0f0f08c;
  transition: all 0.3s ease;
} 

.greetings-container {
  margin-top: 7rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.greetings {
  margin-top: 14%;
  display: inline-flex;
  flex-direction: column;
  font-size: 2.5rem;
  font-weight:bold;
  text-align: center;
  color: rgb(231, 231, 231);
  gap: 2rem;
  margin-bottom: 1rem;
}

.greetings h3 {
  font-size: 1.5rem;
}

</style>