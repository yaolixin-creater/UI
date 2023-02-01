
/**
 *
 */
import { Loading } from 'element-ui'
import {
  backendManageQuerygroup
} from '@/api/getData'

let loadingCount = 0
let loading

export const startLoading = () => {
  loading = Loading.service({
    lock: true,
    text: '亲, 火速加载中......',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  setTimeout(() => {
    loading.close()
  }, 66666)
}

export const endLoading = () => {
  loading.close()
}

export const showLoading = () => {
  if (loadingCount === 0) {
    startLoading()
  }
  loadingCount += 1
}

export const hideLoading = () => {
  if (loadingCount <= 0) {
    return
  }
  loadingCount -= 1
  if (loadingCount === 0) {
    endLoading()
  }
}
export const loadings = () => {
  const loading = this.$loading({
    lock: true,
    text: '火速加载中',
    spinner: 'el-icon-loading',
    background: 'rgba(0, 0, 0, 0.7)',
    fullscreen: false
  })
  setTimeout(() => {
    loading.close()
  }, 8888)
}

export function stepOrder () {
  var step_list = new Array()
  var i = 0, len = 100
  for (; i < len;) {
    var step_item = {desc: `第${i + 1}步`, order: i + 1}
    step_list.push(step_item)
    i++
  }
  console.log(step_list)
  return step_list
}

export const clearToken = () => {
  if (localStorage.autoTokenForVerify) {
    localStorage.autoTokenForVerify = ''
    console.log(`clear SUCCESS...`)
  }
}

export const pickerOptions = {
  shortcuts: [
    {
      text: '今天',
      onClick (picker) {
        const dater = new Date()
        var month = dater.getMonth() + 1
        var date = dater.getDate()
        month = month < 10 ? '0' + month : month
        date = date < 10 ? '0' + date : date
        var start =
                    dater.getFullYear() + '-' + month + '-' + date + ' 00:00:00'
        var end =
                    dater.getFullYear() + '-' + month + '-' + date + ' 23:59:59'
        picker.$emit('pick', [start, end])
      }
    },
    {
      text: '昨天',
      onClick (picker) {
        const dater = new Date()
        var month = dater.getMonth() + 1
        var date = dater.getDate() - 1
        month = month < 10 ? '0' + month : month
        date = date < 10 ? '0' + date : date
        var start =
                    dater.getFullYear() + '-' + month + '-' + date + ' 00:00:00'
        var end =
                    dater.getFullYear() + '-' + month + '-' + date + ' 23:59:59'
        picker.$emit('pick', [start, end])
      }
    },
    {
      text: '最近三天',
      onClick (picker) {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 3)
        picker.$emit('pick', [start, end])
      }
    },
    {
      text: '最近一周',
      onClick (picker) {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
        picker.$emit('pick', [start, end])
      }
    },
    {
      text: '最近一个月',
      onClick (picker) {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
        picker.$emit('pick', [start, end])
      }
    },
    {
      text: '最近三个月',
      onClick (picker) {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
        picker.$emit('pick', [start, end])
      }
    },
    {
      text: '最近半年',
      onClick (picker) {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 180)
        picker.$emit('pick', [start, end])
      }
    },
    {
      text: '最近一年',
      onClick (picker) {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 365)
        picker.$emit('pick', [start, end])
      }
    }
  ]
}
