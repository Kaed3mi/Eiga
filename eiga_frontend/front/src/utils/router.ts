import {createRouter, createWebHistory} from 'vue-router';
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Index from "../components/Index.vue";
import BangumiPageView from "../views/BangumiPageView.vue";
import HomePage from "../views/HomePageView.vue"
import InfoUpdate from "../views/InfoUpdate.vue"
import CharacterPageView from "../views/CharacterPageView.vue"
import SubjectSearch from "../views/SubjectSearch.vue"
import CharacterUpdateView from "../views/CharacterUpdateView.vue"
import BangumiUpdateView from "../views/BangumiUpdateView.vue"
import BangumiCreateView from "../views/BangumiCreateView.vue"
import UserPageView from "../views/UserPageView.vue";
import CharacterCreateView from "../views/CharacterCreateView.vue"
import BangumiRank from "../views/BangumiRank.vue";
import BlogPageView from "../views/BlogPageView.vue";
import BlogCreateView from "../views/BlogCreateView.vue";
import BlogUpdateView from "../views/BlogUpdateView.vue";

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
            path: "/home",
            name: "homePage",
            component: HomePage
        },
        {
            path: '/user/:userId',
            name: 'UserPage',
            component: UserPageView,
        },
        // search
        {
            path: '/subject_search/',
            name: 'bangumi-subject_search',
            component: SubjectSearch,
        },
        // character
        {
            path: '/character/:characterId',
            name: 'character-view',
            component: CharacterPageView,
        },
        {
            path: '/character_update/:characterId',
            name: 'character-update',
            component: CharacterUpdateView,
        },
        {
            path: '/character_create/',
            name: 'character-create',
            component: CharacterCreateView,
        },
        // bangumi
        {
            path: '/bangumi/:bangumiId',
            name: 'bangumi-view',
            component: BangumiPageView,
        },
        {
            path: '/bangumi_update/:bangumiId',
            name: 'bangumi_update-update',
            component: BangumiUpdateView,
        },
        {
            path: '/bangumi_create/',
            name: 'bangumi-create',
            component: BangumiCreateView,
        },
        // rank
        {
            path: '/rank/:page',
            name: 'rank',
            component: BangumiRank
        },
        // blog
        {
            path: '/blog/:blogId',
            name: 'blog-page',
            component: BlogPageView,
        },
        {
            path: '/blog_create',
            name: 'blog-create-page',
            component: BlogCreateView,
        },
        {
            path: '/blog_update/:blogId',
            name: 'blog-update-page',
            component: BlogUpdateView,
        },
    ]
})

export default router;