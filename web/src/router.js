import Login from './view/Login.vue'
import Students from "@/view/Students.vue";
import Teachers from "@/view/Teachers.vue";

const routes = [
    {path:'/', component:Login},
    {path:'/login', component: Login},
    {path:'/students', component: Students},
    {path:'/teachers', component: Teachers},
];
export default routes;
