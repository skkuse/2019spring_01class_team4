<template lang='html'>
<div>
  <div class="tab-wrapper">
    <h2>Self Check!</h2>
    <Tabs >

      <TabPane label="초급">
        파이썬의 기초 문법을 알고 간단한 구현 문제를 해결할 수 있다.
        <ul>
          <li> <Icon type="ios-checkmark" /> 변수, 상수, 기초 자료형</li>
          <li> <Icon type="ios-checkmark" /> 입출력 기초</li>
          <li> <Icon type="ios-checkmark" /> 연산</li>
          <li> <Icon type="ios-checkmark" /> 흐름제어</li>
          <li> <Icon type="ios-checkmark" /> 함수 개념 이해</li>
        </ul>
        <router-link to="testlevel" style="display:block;text-align:right;">
          <Button :size="buttonSize" type="primary">
            문제 풀기
            <Icon type="ios-arrow-forward" />
          </Button>
        </router-link>
      </TabPane>

      <TabPane label="중급">
        자료구조와 기초적인 알고리즘을 활용해 문제를 해결할 수 있다.
        <ul>
          <li> <Icon type="ios-checkmark" /> dictionary / set</li>
          <li> <Icon type="ios-checkmark" /> 함수 사용</li>
          <li> <Icon type="ios-checkmark" /> 고급 자료형 (제네레이터, 이터레이터, map ..)</li>
          <li> <Icon type="ios-checkmark" /> 자료구조의 이해</li>
          <li> <Icon type="ios-checkmark" /> 탐색 알고리즘</li>
          <li> <Icon type="ios-checkmark" /> 정렬 알고리즘</li>
        </ul>
        <router-link to="testlevel" style="display:block;text-align:right;">
          <Button :size="buttonSize" type="primary">
            문제 풀기
            <Icon type="ios-arrow-forward" />
          </Button>
        </router-link>
      </TabPane>

      <TabPane label="고급">
        여러 알고리즘을 사용해 복잡한 문제를 해결할 수 있다.
        <ul>
          <li> <Icon type="ios-checkmark" /> OOP </li>
          <li> <Icon type="ios-checkmark" /> BFS / DFS</li>
          <li> <Icon type="ios-checkmark" /> BackTracking</li>
          <li> <Icon type="ios-checkmark" /> 예외처리 </li>
          <li> <Icon type="ios-checkmark" /> 동적 프로그래밍</li>
          <li> <Icon type="ios-checkmark" /> 정규 표현식</li>
          
        </ul>
        <router-link to="testlevel" style="display:block;text-align:right;">
          <Button :size="buttonSize" type="primary">
            문제 풀기
            <Icon type="ios-arrow-forward" />
          </Button>
        </router-link>
      </TabPane>
      
    </Tabs>
  </div>
</div>
</template>
<script>
export default {

}
</script>
<style>
.tab-wrapper{
  background: #fff;
  padding: 20px;
  text-align: center;
}

.tab-wrapper h2{
  text-align: center;
}

.tab-wrapper ul{
  margin: 20px 0;
  line-height: 2;
  text-align: justify;
}
</style>
