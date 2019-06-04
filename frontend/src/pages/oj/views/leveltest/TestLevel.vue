<template lang='html'>
<div class="test-wrapper">
    <Card class="result" :bordered="false" :padding="50" style="width:800px;" v-if="isSubmit">
      <p slot="title" class="title">진단 결과</p>
      <p class="content">
        중급입니다.
      </p>
      <Button type="primary" @click="this.$router.push('problems')" v-if="problem.ordering === problems.length">
        추천 문제 풀러 가기
        <Icon type="ios-arrow-forward" />
      </Button>
    </Card>
    <Carousel v-model="value">
        <!-- 문제 -->
        <CarouselItem v-for="problem in problems" :key='ordering'>
          <div class="problem-wrapper">
            <Card :bordered="false" :padding="50" style="width:800px;">
              <p slot="title" class="title">{{ problem.difficulty | getDifficulty }} {{problem.ordering}} 번</p>
              <p class="content" v-html="problem.description"></p>
              <hr>
              <div class="radio-wrapper">
                <RadioGroup v-model="answers[problem.ordering - 1]" vertical >
                  <Radio :label="index" v-for="(choice, index) in problem.choices" :key="index" v-if="choice !== ''">
                    <span> {{ choice }}</span>
                  </Radio>
                </RadioGroup>
              </div>
            <div style="text-align:right">
              <Button type="primary" @click="onSubmit" v-if="problem.ordering === problems.length">
              제출
              <Icon type="ios-arrow-forward" />
              </Button>
            </div>    
            </Card>
          </div>
        </CarouselItem>
        <!-- 문제 end -->
    </Carousel>
</div>
</template>
<script>
import api from '@oj/api'

export default {
  props: ['difficulty'],
  data () {
    return {
      value: 0,
      problems: [],
      isSubmit: false,
      result: ''
    }
  },
  filters: {
    getDifficulty (difficulty) {
      if (difficulty === 'low') {
        return '초급'
      } else if (difficulty === 'mid') {
        return '중급'
      } else {
        return '고급'
      }
    }
  },
  computed: {
    answers () {
      const answers = []
      for (let index = 0; index < this.problems.length; index++) {
        answers.push('')
      }
      return answers
    }
  },
  created () {
    api.getLevelTest({difficulty: this.difficulty, limit: 10})
    .then(res => {
      this.problems = res.data.data.results
    })
  },
  methods: {
    onSubmit () {
      if (this.isComplete()) {
        let body = {
          difficulty: this.difficulty,
          answers: this.answers
        }
        api.submitLevelTestAnswers(body).then(res => {
          this.isSubmit = true
          this.result = res
        })
      } else {
        // eslint-disable-next-line no-undef
        alert('문제를 모두 풀어주세요.')
      }
    },
    isComplete () {
      for (let index = 0; index < this.answers.length; index++) {
        const answer = this.answers[index]
        if (answer === '') {
          this.value = index
          return false
        }
      }
      return true
    }
  }

}
</script>
<style >

</style>
