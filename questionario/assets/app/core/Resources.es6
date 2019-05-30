window.User = {
  install(Vue, options) {
    const url = '/api/v1/usuarios/'
    Vue.prototype.User = Vue.prototype.Resource(url)
  }
}

window.Questionario = {
  install(Vue, options) {
    const url = '/api/v1/questionarios/'
    Vue.prototype.Questionario = Vue.prototype.Resource(url, {
      submeterQuestionario (questionario) {
        return axios.post(`${url}${questionario.id}/submeter/`, questionario)
      },
      validos () {
        return axios.get(`${url}validos/`)
      }
    })
  }
}

window.RespostaQuestao = {
  install(Vue, options) {
    const url = '/api/v1/respostas/'
    Vue.prototype.RespostaQuestao = Vue.prototype.Resource(url, {
      submeterQuestionario (questionario) {
        return axios.post(`${url}submeter/`, questionario)
      }
    })
  }
}
