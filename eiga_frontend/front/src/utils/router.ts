import {createRouter, createWebHistory} from 'vue-router';
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Index from "../components/Index.vue";
import BangumiPageView from "../views/BangumiPageView.vue";
import HomePage from "../views/HomePageView.vue"
import InfoUpdate from "../views/InfoUpdate.vue"
import CharacterPageView from "../views/CharacterPageView.vue"
import SubjectSearch from "../views/SubjectSearch.vue"

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
            path: "/bangumi",
            name: "bangumi",
            component: BangumiPageView,
        },
        {
            path: "/Home",
            name: "homePage",
            component: HomePage
        },
        {
            path: '/bangumi/:bangumiId',
            name: 'bangumi-view',
            component: BangumiPageView,
        },
        {
            path: '/character/:characterId',
            name: 'character-view',
            component: CharacterPageView,
        },
        {
            path: '/subject_search/',
            name: 'bangumi-subject_search',
            component: SubjectSearch,
        },
    ]
})

export default router;