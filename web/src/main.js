import { createApp } from 'vue'
import ViewUIPlus from 'view-ui-plus'
import App from './App.vue'
import 'view-ui-plus/dist/styles/viewuiplus.css'
import axios from "axios";
// 这个地方是在做一个导包起别名的操作，将我们在router.js中书写的内容导入到main的文件中去
import * as VueRouter from 'vue-router'
import routes from "./router";

// 说明：下面这一坨代码是一个路由（router）的标准写法，需要记住
const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes: routes,
})

const app = createApp(App)
app.config.globalProperties.$axios = axios
// 笔记：在main.js中被use的参数都是可以被直接调用的
app.use(ViewUIPlus).use(router).mount('#app')
