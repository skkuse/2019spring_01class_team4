import Vue from 'vue'
import store from '@/store'
import axios from 'axios'

Vue.prototype.$http = axios
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

export default {
  testCrawlerApi (username) {
    return ajax('https://www.acmicpc.net/user/' + username, 'get')
  },
  checkUsernameOrEmail (username, email) {
    return ajax('check_username_or_email', 'post', {
      data: {
        username,
        email
      }
    })
  },
  getProblemList (offset, limit, searchParams) {
    let params = {
      paging: true,
      offset,
      limit
    }
    Object.keys(searchParams).forEach((element) => {
      if (searchParams[element]) {
        params[element] = searchParams[element]
      }
    })
    return ajax('problem', 'get', {
      params: params
    })
  },
  pickone () {
    return ajax('pickone', 'get')
  }
}

/**
 * @param url
 * @param method get|post|put|delete...
 * @param params like queryString. if a url is index?a=1&b=2, params = {a: '1', b: '2'}
 * @param data post data, use for method put|post
 * @returns {Promise}
 */
function ajax (url, method, options) {
  if (options !== undefined) {
    var {params = {}, data = {}} = options
  } else {
    params = data = {}
  }
  return new Promise((resolve, reject) => {
    axios({
      url,
      method,
      params,
      data
    }).then(res => {
      // API正常返回(status=20x), 是否错误通过有无error判断
      if (res.data.error !== null) {
        Vue.prototype.$error(res.data.data)
        reject(res)
        // 若后端返回为登录，则为session失效，应退出当前登录用户
        if (res.data.data.startsWith('Please login')) {
          store.dispatch('changeModalStatus', {'mode': 'login', 'visible': true})
        }
      } else {
        resolve(res)
        // if (method !== 'get') {
        //   Vue.prototype.$success('Succeeded')
        // }
      }
    }, res => {
      // API请求异常，一般为Server error 或 network error
      reject(res)
      Vue.prototype.$error(res.data.data)
    })
  })
}
