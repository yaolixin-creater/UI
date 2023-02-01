import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const login = r => require.ensure([], () => r(require('@/page/login')), 'login')
const menu = r => require.ensure([], () => r(require('@/page/menu')), 'menu')
const home = r => require.ensure([], () => r(require('@/page/home')), 'home')
const backCaseList = r => require.ensure([], () => r(require('@/page/backCaseList')), 'backCaseList')
const backReport = r => require.ensure([], () => r(require('@/page/backReport')), 'backReport')
const backParamAdd = r => require.ensure([], () => r(require('@/page/backParamAdd')), 'backParamAdd')
const backParamList = r => require.ensure([], () => r(require('@/page/backParamList')), 'backParamList')
const backstepmod = r => require.ensure([], () => r(require('@/page/backstepmod')), 'backstepmod')
const groupManagement = r => require.ensure([], () => r(require('@/page/groupManagement')), 'groupManagement')
const envManagement = r => require.ensure([], () => r(require('@/page/envManagement')), 'envManagement')
const help = r => require.ensure([], () => r(require('@/page/help')), 'help')
const routes = [{
  path: '/login',
  component: login
},
{
  path: '/',
  component: login
},
{
  path: '/menu',
  component: menu,
  meta: {
    'title': [],
    requiresAuth: true
  },
  name: '',
  children: [{
    path: '/home',
    component: home,
    meta: {
      'title': [],
      requiresAuth: false
    }
  },
  {
    path: '/backCaseList',
    component: backCaseList,
    meta: {
      'title': ['UI用例列表'],
      requiresAuth: true
    }
  },
  {
    path: '/backReport',
    component: backReport,
    meta: {
      'title': ['UI测试报告'],
      requiresAuth: true
    }
  },
  {
    path: '/backParamAdd',
    component: backParamAdd,
    meta: {
      'title': ['UI参数配置'],
      requiresAuth: true
    }
  },
  {
    path: '/backstepmod',
    component: backstepmod,
    meta: {
      'title': ['UI复用步骤修改'],
      requiresAuth: true
    }
  },
  {
    path: '/backParamList',
    component: backParamList,
    meta: {
      'title': ['UI参数列表'],
      requiresAuth: true
    }
  },
  {
    path: '/groupManagement',
    component: groupManagement,
    meta: {
      'title': ['UI分组管理'],
      requiresAuth: true
    }
  },
  {
    path: '/envManagement',
    component: envManagement,
    meta: {
      'title': ['UI环境管理'],
      requiresAuth: true
    }
  },
  {
    path: '/help',
    component: help,
    meta: {
      'title': ['UI帮助文档'],
      requiresAuth: true
    }
  }
  ]
}
]

export default new Router({
  routes,
  strict: process.env.NODE_ENV !== 'production'
})
