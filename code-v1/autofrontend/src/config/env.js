/**
 * 配置编译环境和线上环境之间的切换
 *
 * baseUrl: 域名地址
 * routerMode: 路由模式
 * baseImgPath: 图片存放地址
 *
 */
let baseUrl = ''
let routerMode = 'hash'
let baseImgPath = ''

if (process.env.NODE_ENV === 'development') {
  baseUrl = 'http://127.0.0.1:8001'
} else {
  baseUrl = 'http://115.159.211.228:5155'
}

export { baseUrl, routerMode, baseImgPath }
