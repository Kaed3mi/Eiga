import { createApp, VueElement } from 'vue'
import './style.css'
import './styles/styles.css'
import App from './App.vue'
import router from './utils/router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css' 
createApp(App).use(ElementPlus).use(router).mount('#app')
