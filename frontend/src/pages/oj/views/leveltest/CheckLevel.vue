<template lang='html'>
<div>
  <div class="tab-wrapper">
    <h2> <img class="selfcheck-img" src="@/assets/selfcheck.png"> Self Check</h2>
    <p class="notice">*진단고사는 Python 3 버전을 기준으로 제작되었습니다.</p>
    <Tabs >

      <TabPane label="초급">
        파이썬의 기초 문법을 알고 간단한 구현 문제를 해결할 수 있다.
        <ul>
          <li> <Icon type="ios-checkmark" /> 변수, 상수, 기초 자료형</li>
          <li> <Icon type="ios-checkmark" /> 입출력 기초</li>
          <li> <Icon type="ios-checkmark" /> 연산</li>
          <li> <Icon type="ios-checkmark" /> 흐름제어</li>
          <li> <Icon type="ios-checkmark" /> 함수 개념 이해</li>
          <li> <Icon type="ios-checkmark" /> 문자열 포매팅</li>
        </ul>
        <router-link to="/test/low" style="display:block;text-align:right;">
          <Button type="primary">
            초급 문제 풀기
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
        <router-link to="/test/mid" style="display:block;text-align:right;">
          <Button type="primary">
            중급 문제 풀기
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
        <router-link to="/test/high" style="display:block;text-align:right;">
          <Button type="primary">
            고급 문제 풀기
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

.tab-wrapper .notice{
  text-align: right;
  font-size: 13px;
  margin-top: 10px;
}

.tab-wrapper ul{
  margin: 20px 0;
  line-height: 2;
  text-align: justify;
}

.selfcheck-img {
  width: 30px;
  vertical-align: middle;
}
</style>
