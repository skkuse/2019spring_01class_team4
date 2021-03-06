<template>
  <Row type="flex" :gutter="18">
    <Col :span=19>
    <Panel shadow>
      <div slot="title">Problem List</div>
      <div slot="extra">
        <ul class="filter">
          <li>
            <Dropdown @on-click="filterByDifficulty">
              <span>{{query.difficulty === '' ? 'Difficulty' : query.difficulty}}
                <Icon type="arrow-down-b"></Icon>
              </span>
              <Dropdown-menu slot="list">
                <Dropdown-item name="">All</Dropdown-item>
                <Dropdown-item name="Low">Low</Dropdown-item>
                <Dropdown-item name="Mid">Mid</Dropdown-item>
                <Dropdown-item name="High">High</Dropdown-item>
              </Dropdown-menu>
            </Dropdown>
          </li>
          <li>
            <i-switch size="large" @on-change="handleTagsVisible">
              <span slot="open">Tags</span>
              <span slot="close">Tags</span>
            </i-switch>
          </li>
          <li>
            <Input v-model="query.keyword"
                   @on-enter="filterByKeyword"
                   @on-click="filterByKeyword"
                   placeholder="keyword"
                   icon="ios-search-strong"/>
          </li>
          <li>
            <Button type="info" @click="requestRecoList">
              <Icon type="refresh"></Icon>
              문제추천받기
            </Button>
          </li>
        </ul>
      </div>
      <Table style="width: 100%; font-size: 16px;"
             :columns="problemTableColumns"
             :data="problemList"
             :loading="loadings.table"
             :id='problemList.id'
             disabled-hover></Table>
    </Panel>
    <Pagination :total="total" :page-size="limit" @on-change="pushRouter" :current.sync="query.page"></Pagination>

    </Col>

    <Col :span="5">
    <Panel :padding="10">
      <div slot="title" class="taglist-title">Tags</div>
      <Button v-for="tag in tagList"
              :key="tag.name"
              @click="filterByTag(tag.name)"
              type="ghost"
              :disabled="query.tag === tag.name"
              shape="circle"
              class="tag-btn">{{tag.name}}
      </Button>

      <Button long id="pick-one" @click="pickone">
        <Icon type="shuffle"></Icon>
        Pick one
      </Button>
    </Panel>
    <Spin v-if="loadings.tag" fix size="large"></Spin>
    </Col>
  </Row>
</template>

<script>
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  import utils from '@/utils/utils'
  import { ProblemMixin } from '@oj/components/mixins'
  import Pagination from '@oj/components/Pagination'

  export default {
    name: 'ProblemList',
    mixins: [ProblemMixin],
    components: {
      Pagination
    },
    data () {
      return {
        tagList: [],
        problemTableColumns: [
          {
            title: '출처',
            width: 80,
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'text',
                  size: 'large'
                },
                on: {
                  click: () => {
                    let isEx = params.row.source === '해커랭크' || params.row.source === '백준'
                    let pid = params.row.source === '' ? params.row.pid : params.row._id
                    this.$router.push({name: 'problem-details', params: { problemID: pid, isEx: isEx }})
                    // if (params.row.source === '') {
                    //   this.$router.push({name: 'problem-details', params: {problemID: params.row._id}})
                    // } else {
                    //   this.$router.push({name: 'problem-details-ex', params: {problemID: params.pid}})
                    // }
                  }
                },
                style: {
                  padding: '2px 0'
                }
              }, params.row.source === '' ? 'Qurious' : params.row.source)
            }
          },
          {
            title: 'Title',
            width: 400,
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'text',
                  size: 'large'
                },
                on: {
                  click: () => {
                    let isEx = params.row.source === '해커랭크' || params.row.source === '백준'
                    let pid = isEx ? params.row.pid : params.row._id
                    this.$router.push({name: 'problem-details', params: {problemID: pid, isEx: isEx}})
                    // if (params.row.source === '') {
                    //   this.$router.push({name: 'problem-details', params: {problemID: params.row._id}})
                    // } else {
                    //   this.$router.push({name: 'problem-details-ex', params: {problemID: params.pid}})
                    // }
                  }
                },
                style: {
                  padding: '2px 0',
                  overflowX: 'auto',
                  textAlign: 'left',
                  width: '100%',
                  textDecoration: params.row.isSolved ? 'line-through' : 'none'
                }
              }, params.row.title)
            }
          },
          {
            title: 'Level',
            render: (h, params) => {
              let t = params.row.difficulty
              let color = 'blue'
              if (t === 'Low') color = 'green'
              else if (t === 'High') color = 'yellow'
              return h('Tag', {
                props: {
                  color: color
                }
              }, params.row.difficulty)
            }
          },
          // {
          //   title: 'Total',
          //   key: 'submission_number'
          // },
          {
            title: 'AC Rate',
            render: (h, params) => {
              let isEx = params.row.source === '해커랭크' || params.row.source === '백준'
              if (isEx) {
                return h('span', params.row.acrate)
              } else {
                let ac = this.getACRate(params.row.accepted_number, params.row.submission_number)
                return h('span', ac === '0%' ? '-' : ac)
              }
            }
          }
        ],
        problemList: [],
        limit: 20,
        total: 0,
        loadings: {
          table: true,
          tag: true
        },
        routeName: '',
        query: {
          keyword: '',
          difficulty: '',
          tag: '',
          page: 1
        }
      }
    },
    mounted () {
      this.getProblemList()
      this.getRecoList()
      // // this.init()
    },
    methods: {
      init (simulate = false) {
        this.routeName = this.$route.name
        let query = this.$route.query
        this.query.difficulty = query.difficulty || ''
        this.query.keyword = query.keyword || ''
        this.query.tag = query.tag || ''
        this.query.page = parseInt(query.page) || 1
        if (this.query.page < 1) {
          this.query.page = 1
        }
        if (!simulate) {
          this.getTagList()
        }
        // this.getProblemList()
        // this.getRecoList()
      },
      pushRouter () {
        this.$router.push({
          name: 'problem-list',
          query: utils.filterEmptyValue(this.query)
        })
      },
      getProblemList () {
        let offset = (this.query.page - 1) * this.limit
        this.loadings.table = true
        api.getProblemList(offset, this.limit, this.query).then(res => {
          this.loadings.table = false
          this.total = res.data.data.total
          let results = res.data.data.results
          results.forEach(resData => {
            this.problemList.push(resData)
          })
          if (this.isAuthenticated) {
            this.addStatusColumn(this.problemTableColumns, res.data.data.results)
          }
        }, res => {
          this.loadings.table = false
        })
      },
      getRecoList () {
        api.getRecomendProblemList().then(res => {
          const results = res.data.data.results

          results.forEach(resData => {
            let data = {
              id: resData.id,
              source: resData.problemex.exbank,
              title: resData.problemex.title,
              difficulty: resData.problemex.cate1 + ' ' + resData.problemex.cate2,
              pid: resData.problemex.id,
              acrate: this.getAcRate(resData.problemex.correct_ratio),
              isSolved: resData.is_Solved
            }
            console.log(resData.problemex)
            this.problemList.push(data)
          })
        })
      },
      requestRecommend () {
        api.requestRecommend().then(res => {
          this.$router.go()
        })
      },
      getTagList () {
        api.getProblemTagList().then(res => {
          this.tagList = res.data.data
          this.loadings.tag = false
        }, res => {
          this.loadings.tag = false
        })
      },
      filterByTag (tagName) {
        this.query.tag = tagName
        this.query.page = 1
        this.pushRouter()
      },
      filterByDifficulty (difficulty) {
        this.query.difficulty = difficulty
        this.query.page = 1
        this.pushRouter()
      },
      filterByKeyword () {
        this.query.page = 1
        this.pushRouter()
      },
      handleTagsVisible (value) {
        if (value) {
          this.problemTableColumns.push(
            {
              title: 'Tags',
              align: 'center',
              render: (h, params) => {
                let tags = []
                params.row.tags.forEach(tag => {
                  tags.push(h('Tag', {}, tag))
                })
                return h('div', {
                  style: {
                    margin: '8px 0'
                  }
                }, tags)
              }
            })
        } else {
          this.problemTableColumns.splice(this.problemTableColumns.length - 1, 1)
        }
      },
      onReset () {
        this.$router.push({name: 'problem-list'})
      },
      pickone () {
        api.pickone().then(res => {
          this.$success('Good Luck')
          this.$router.push({name: 'problem-details', params: {problemID: res.data.data}})
        })
      },
      getAcRate (num) {
        return Math.round(num * 100) + '%'
      },
      requestRecoList () {
        api.reqRecomendProblemList().then(res => {
          this.$router.go()
        })
      }
    },
    computed: {
      ...mapGetters(['isAuthenticated'])
    },
    watch: {
      '$route' (newVal, oldVal) {
        if (newVal !== oldVal) {
          this.init(true)
        }
      },
      'isAuthenticated' (newVal) {
        if (newVal === true) {
          this.init()
        }
      }
    }
  }
</script>

<style scoped lang="less">
  .taglist-title {
    margin-left: -10px;
    margin-bottom: -10px;
  }

  .tag-btn {
    margin-right: 5px;
    margin-bottom: 10px;
  }

  #pick-one {
    margin-top: 10px;
  }
</style>
