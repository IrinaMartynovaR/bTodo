import { createApp, Vue } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')

import axios from 'axios'

Vue.prototype.$http = axios;
