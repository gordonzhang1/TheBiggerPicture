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
  if (!user.value || !user.value.email) return;

  const formData = new FormData();

  formData.append('image_name', 'New Mosaic');
  formData.append('user', user.value.email);

  const res = await fetch('http://127.0.0.1:5001/api/create-category', {
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

  const res = await fetch('http://127.0.0.1:5001/api/get-mosaics', {
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
  <nav class="nav">
    <RouterLink to="/dashboard" @click="login">Log in</RouterLink>
    <button @click="logOut">Log Out</button>
    <RouterLink to="/dashboard">DASHBOARD</RouterLink>
    <a @click="createNewMosaic" class="manual-router-link">MOSAIC</a>
    <h1>{{user.email}}</h1>
    
  </nav>
  <RouterView class="router-view" />

</template>

<style scoped>
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
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
</style>