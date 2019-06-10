<template lang='html'>
<div class="test-wrapper">
    <Card class="result-wrapper" style="width:500px; padding: 20px 50px; margin:auto;" v-if="isSubmit">
      <p slot="title" class="title">진단 결과</p>
      <hr>
      <div class="result">
        <img :src="resultImg" alt="" style="margin-top: 15px;">
        <br>
        {{result.data}}
      </div>
      <div style="text-align:right;">
      <Button type="primary" @click.native="$router.push('/problems')">
        추천 문제 풀러 가기
        <Icon type="ios-arrow-forward" />
      </Button>
      </div>
    </Card>

    <Carousel v-model="value" dots="none" v-if="!isSubmit">
        <!-- 문제 -->
        <CarouselItem v-for="problem in problems" :key='problem.ordering' >
          <div class="problem-wrapper" >
            <Card :bordered="false"  style="width:800px; padding: 20px 50px;">
              <p slot="title" class="title">{{ problem.difficulty | getDifficulty }} {{problem.ordering}} 번</p>
              <p class="content" v-html="problem.description"></p>
              <hr>
              <div class="radio-wrapper">
                <RadioGroup v-model="answers[problem.ordering - 1]" vertical @on-change="radioClick">
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
    },
    resultImg () {
      switch (this.result.data.substr(0, 1)) {
        case '초':
          return require('@/assets/level1.png')
        case '중':
          return require('@/assets/level2.png')
        case '고':
          return require('@/assets/level3.png')

        default:
          break
      }
    }
  },
  created () {
    api.getLevelTest({difficulty: this.difficulty})
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
          this.result = res.data
          console.log(res)
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
    },
    radioClick () {
      // 맨 끝에서 넘어가지 않도록
      if (this.value !== 10) {
        this.value += 1
      }
    }
  }
}
</script>
<style >
.ivu-card {
  border-radius: 15px;
}

.ivu-carousel-arrow {
  top: 5%;
}
.ivu-carousel-arrow.right {
  right: 30px;
}
.ivu-carousel-arrow.left {
  left: 30px;
}

.ivu-card-body .radio-wrapper {
  margin-top: 15px;
}

.result-wrapper {
  margin-bottom: 30px;
}

.result-wrapper .radio-wrapper {
  margin-top: 15px;
}

.result-wrapper .result {
  font-size: 30px;
  text-align: center;
  font-weight: 500;
  margin-bottom: 50px;
  height: 300px;
}

.ivu-radio-group {
  width: 100%;
  
}

.ivu-radio-group-item{
  padding: 0 10px;
}
.ivu-radio-group-item:hover {
  background: rgba(0,0,0,0.1)
}
</style>
