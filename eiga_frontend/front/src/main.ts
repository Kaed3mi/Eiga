import { createApp, VueElement } from 'vue'
import './style.css'
import './styles/styles.css'
import App from './App.vue'
import router from './utils/router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App);
router.afterEach((to, from) => {
    if (from.path != '/') {
        if(to.path.split('/')[1] === from.path.split('/')[1]) {
            console.log("active reload")
            window.location.reload()
        }
    }
});
app.use(ElementPlus).use(router).mount('#app')
