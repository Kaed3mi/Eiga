import {createRouter, createWebHistory} from 'vue-router';
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Index from "../components/Index.vue";
import HomePage from "../views/HomePageView.vue"
import InfoUpdate from "../views/InfoUpdate.vue"
 
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            name: "myLogin",
            component: Login,
        },
        {
            path: "/login",
            name: "Login",
            component: Login,
        },
        {
            path: "/register",
            name: "Register",
            component: Register,
        },
        {
            path: "/update",
            name: "Update",
            component: InfoUpdate,
        },
        {
            path: "/index",
            name: "Index",
            component: Index,
        },
        {
            path: "/Home",
            name: "homePage",
            component: HomePage
        }
    ]
})
 
export default router;