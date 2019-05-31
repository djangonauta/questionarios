Vue.component('questionarios', resolve => {
  axios.get('/public/app/core/componentes/questionarios.html').then(response => {
    resolve({
      template: response.data,
      delimiters: ['[[', ']]'],
      data () {
        return {
          questionarios: [],
          questionario: {inicio: new Date(), questoes: []},
          questionarioFields: [
            {key: 'id', label: 'ID'},
            {key: 'titulo', label: 'Título'},
            {key: 'descricao', label: 'Descrição'},
            {key: 'acoes', label: 'Ações'},
          ],

          questao: {tipo_questao: '1', alternativas: []},
          questionario_options: {
            1: 'Texto Livre',
            2: 'Única Escolha',
            3: 'Múltipla Escolha',
            4: 'Avaliação',
          },
          questoesFields: [
            'index',
            {key: 'titulo', label: 'Título'},
            {key: 'descricao', label: 'Descrição'},
            {key: 'tipo_questao', label: 'Tipo Questão'},
            {key: 'acao', label: 'Ações'},
          ],

          alternativa: {tipo_alternativa: '1', alternativas: []},
          subAlternativa: {tipo_alternativa: '1'},
          alternativasFields: [
            'index',
            {key: 'titulo', label: 'Título'},
            {key: 'descricao', label: 'Descrição'},
            {key: 'acao', label: 'Ações'},
          ],
          alternativaOptions: {
            1: 'Padrão',
            2: 'Texto',
            3: 'Múltipla Escolha'
          },
        }
      },
      methods: {
        carregarQuestionarios () {
          this.Questionario.validos().then(response => {
            this.questionarios = response.data
          })
        },  
        adicionarQuestao () {
          this.questionario.questoes.push(this.questao)
          this.questao = {tipo_questao: '1', alternativas: []}
        },
        removerQuestao (index) {
          this.questionario.questoes.splice(index, 1)
        },
        adicionarAlternativa() {
          this.questao.alternativas.push(this.alternativa)
          this.alternativa = {tipo_alternativa: '1', alternativas: []}
        },
        adicionarSubAlternativa () {
          this.alternativa.alternativas.push(this.subAlternativa)
          this.subAlternativa = {tipo_alternativa: '1'}
        },
        removerAlternativa (index) {
          this.questao.alternativas.splice(index, 1)
        },
        removerSubAlternativa (index) {
          this.alternativa.alternativas.splice(index, 1)
        },
        salvarQuestionario () {
          this.Questionario.save(this.questionario).then(response => {
            this.questionario = {inicio: new Date(), questoes: []}
            this.carregarQuestionarios()
          })
        },
        removerQuestionario (questionario) {
          if (confirm('remover?')) {
            this.Questionario.delete(questionario).then(response => {
              return this.carregarQuestionarios()
            })
          }
        }
      },
      mounted () {
        this.carregarQuestionarios()
      }
    })
  })
})
