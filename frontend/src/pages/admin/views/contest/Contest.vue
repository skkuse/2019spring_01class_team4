<template>
  <div class="view">
    <Panel :title="title">
      <el-form label-position="top">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item :label="$t('m.ContestTitle')" required>
              <el-input v-model="testproblem.title" :placeholder="$t('m.ContestTitle')"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="$t('m.ContestDescription')" required>
              <Simditor v-model="testproblem.description"></Simditor>
            </el-form-item>
          </el-col>
        
          <el-col :span="8">
            <el-form-item :label="'선택지 만들기'">
              <el-input class="choice" v-model="testproblem.choices[1]" :placeholder="'1번 문항'"></el-input>
              <el-input class="choice" v-model="testproblem.choices[2]" :placeholder="'2번 문항'"></el-input>
              <el-input class="choice" v-model="testproblem.choices[3]" :placeholder="'3번 문항'"></el-input>
              <el-input class="choice" v-model="testproblem.choices[4]" :placeholder="'4번 문항'"></el-input>
              <el-input class="choice" v-model="testproblem.choices[5]" :placeholder="'5번 문항'"></el-input>
            </el-form-item>
          </el-col>

          <el-col :span="8">
            <el-form-item :label="'정답'">
              <el-input-number class="choice" v-model="testproblem.answer" :min="1" :max="5"></el-input-number>  
            </el-form-item>

            <el-form-item :label="'순번'">
              <el-input-number v-model="testproblem.ordering" :min="1" :max="30"></el-input-number>  
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="'난이도'">
               <el-select v-model="testproblem.difficulty" placeholder="Select">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <save @click.native="saveContest"></save>
    </Panel>
  </div>
</template>

<script>
  import api from '../../api.js'
  import Simditor from '../../components/Simditor.vue'

  export default {
    name: 'CreateContest',
    components: {
      Simditor
    },
    data () {
      return {
        title: 'Create Contest',
        disableRuleType: false,
        testproblem: {
          title: '',
          description: '',
          choices: {
            1: '',
            2: '',
            3: '',
            4: '',
            5: ''
          },
          ordering: 1,
          difficulty: ''
        },
        options: [{
          value: 'high',
          label: '고급'
        }, {
          value: 'mid',
          label: '중급'
        }, {
          value: 'low',
          label: '초급'
        }]
      }
    },
    methods: {
      saveContest () {
        console.log('Start Saving!')
        let data = Object.assign({}, this.testproblem)
        console.log(data)
        api.createTestProblem(data).then(res => {
          this.$router.push({name: 'contest-list', query: {refresh: 'true'}})
        }).catch((err) => {
          console.log(err)
        })
      },
      addIPRange () {
        this.contest.allowed_ip_ranges.push({value: ''})
      },
      removeIPRange (range) {
        let index = this.contest.allowed_ip_ranges.indexOf(range)
        if (index !== -1) {
          this.contest.allowed_ip_ranges.splice(index, 1)
        }
      }
    },
    mounted () {
      if (this.$route.name === 'edit-contest') {
        this.title = 'Edit Contest'
        this.disableRuleType = true
        api.getContest(this.$route.params.contestId).then(res => {
          let data = res.data.data
          let ranges = []
          for (let v of data.allowed_ip_ranges) {
            ranges.push({value: v})
          }
          if (ranges.length === 0) {
            ranges.push({value: ''})
          }
          data.allowed_ip_ranges = ranges
          this.contest = data
        }).catch(() => {
        })
      }
    }
  }
</script>
<style>
  .choice {
    margin-bottom: 1em;
  }
</style>
