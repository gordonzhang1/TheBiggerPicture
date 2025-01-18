<script>
export default {
  data() {
    return {
      links: ['Home', 'Analytics', 'Settings', 'Profile'],
    };
  },
};
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div class="dashboard">
    <aside class="sidebar">
      <ul>
        <li v-for="link in links" :key="link">{{ link }}</li>
      </ul>
    </aside>
    <header class="header">
      <h1>Dashboard</h1>
    </header>
    <main class="main-content">
      <section>
        <!-- Add charts, tables, etc. -->
        <h2>Welcome to the Dashboard</h2>
      </section>
    </main>
    <footer class="footer">
      <p>© 2025 Your Company</p>
    </footer>
  </div>
</template>

<style scoped>
/* Add custom styling here */
.dashboard {
  display: grid;
  grid-template-areas:
    "sidebar header"
    "sidebar main"
    "sidebar footer";
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  height: 100vh;
}

.sidebar {
  grid-area: sidebar;
  background: #2c3e50;
  color: #ecf0f1;
  padding: 1rem;
}

.header {
  grid-area: header;
  background: #34495e;
  color: white;
  padding: 1rem;
}

.main-content {
  grid-area: main;
  padding: 1rem;
}

.footer {
  grid-area: footer;
  background: #34495e;
  color: white;
  text-align: center;
  padding: 0.5rem;
}
</style>
