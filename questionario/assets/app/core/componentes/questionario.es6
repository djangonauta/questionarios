Vue.component('questionario', resolve => {
  axios.get('/public/app/core/componentes/questionario.html').then(response => {
    resolve({
      template: response.data,
      delimiters: ['[[', ']]'],
      data () {
        return {
          questionario: {},
        }
      },
      beforeRouteEnter (to, from, next) {
        next(vm => vm.setQuestionario(to.params.id))
      },
      methods: {
        setQuestionario (id) {
          this.Questionario.get(id).then(response => {
            this.questionario = response.data
            this.questionario.questoes.forEach(q => {
              q.questionarioQuestao = {
                questionario: this.questionario.id,
                questao: q.id
              }
            })
          })
        },
        submeterQuestionario () {
          console.log(this.questionario.questoes.map(q => q.questionarioQuestao))
          // this.QuestionariosQuestoes.submeterQuestionario(this.data).then(() => {
          //   this.$router.push('/cadastrar-questionarios')
          // })
        }
      }
    })
  })
})
