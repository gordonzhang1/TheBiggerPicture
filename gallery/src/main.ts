import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createAuth0 } from '@auth0/auth0-vue';

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.use(
    createAuth0({
      domain: "dev-flupsnk3yrevhily.us.auth0.com",
      clientId: "l9b4yfb1CK9mm9D0Qnf16m8xKystaruJ",
      authorizationParams: {
        redirect_uri: window.location.origin
      }
    })
  );

app.mount('#app')



