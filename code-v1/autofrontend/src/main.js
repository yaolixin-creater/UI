// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/iconfont/iconfont.css'
import VueClipboard from 'vue-clipboard2'
import clipboard from 'clipboard'
import 'default-passive-events'

Vue.prototype.clipboard = clipboard
Vue.config.productionTip = false
VueClipboard.config.autoSetContainer = true // add this line

Vue.use(VueClipboard)
Vue.use(ElementUI)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {
    App
  }
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 这里判断用户是否登录，验证本地存储是否有token
    if (!localStorage.autoTokenForVerify) { // 判断当前的token是否存在
      console.log('no token...')
      next({
        path: '/login',
        query: {
          redirect: to.fullPath
        }
      })
    } else {
      next()
      console.log('have token...')
    }
  } else {
    next()
  }
})

export default router
