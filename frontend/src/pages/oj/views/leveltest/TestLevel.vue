<template lang='html'>
<div class="test-wrapper">
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
      problems: []
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
  created () {
    api.getLevelTest({difficulty: this.difficulty, limit: 10})
    .then(res => {
      this.problems = res.data.data.results
    })
  },
  methods: {
    onSubmit () {
      if (this.isComplete()) {
        this.$router.push('/test/result')
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
.test-wrapper {

}

.test-wrapper .problem-wrapper .title {
    text-align: center;    
    font-size: 20px;
}
p.content {
    margin-left: 25px;
    margin-right: 20px;
    margin-bottom: 20px;
    font-size: 15px
}



</style>
