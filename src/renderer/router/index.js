import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: require('@/view/home.vue').default
    },
    {
      path: '/file',
      name: 'home',
      component: require('@/view/file.vue').default
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
