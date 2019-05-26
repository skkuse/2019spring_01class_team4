<template lang='html'>
<div class="test-wrapper">
    
    <Carousel v-model="value">
        <!-- 문제 -->
        <CarouselItem>
            <div class="problem-wrapper">
                <Card :bordered="false" :padding="50" style="width:800px;">
                    <p slot="title" class="title">중급 문제 1 번</p>
                    <pre>
다음은 두 수의 공약수 전체를 출력하는 프로그램이다.
div_x=set()
div_y=set()

def getDiv(xx,yy):
    for ii in range(1,xx+1):
        if(xx%ii==0):
            div_x.add(ii)

    for jj in range(1,yy+1):
        if(yy%jj==0):
            div_y.add(jj)
            
    def CommonDiv(divSet1, divSet2):
        divisor=divSet1 & divSet2
        return divisor
    print(CommonDiv(div_x, div_y))

getDiv(2,6)와 CommonDiv(div_x, div_y)를 차례대로 호출했을 때, 결과는?

                    </pre>
                    <hr>
                    <div class="radio-wrapper">
                        <RadioGroup v-model="answers[0]" vertical>
                            <Radio label="1">
                                <span> {1,2,1,2,3,6}, {1,2}</span>
                            </Radio>
                            <Radio label="2">
                                <span>{1,2}, {1,2}</span>
                            </Radio>
                            <Radio label="3">
                                <span>{1,2,1,2,3,6}, NameError</span>
                            </Radio>
                            <Radio label="4">
                                <span>{1,2}, NameError</span>
                            </Radio>
                            <Radio label="5">
                                <span>{1,2,3,6}, NameError</span>
                            </Radio>
                        </RadioGroup>
                    </div>
                </Card>
                
            </div>
        </CarouselItem>
        <!-- 문제 end -->

        <!-- 문제 -->
        <CarouselItem>
            <div class="problem-wrapper">
                <Card :bordered="false" :padding="50" style="width:800px;">
                    <p slot="title" class="title">중급 문제 1 번</p>
                    <pre>
다음은 두 수의 공약수 전체를 출력하는 프로그램이다.
div_x=set()
div_y=set()

def getDiv(xx,yy):
    for ii in range(1,xx+1):
        if(xx%ii==0):
            div_x.add(ii)

    for jj in range(1,yy+1):
        if(yy%jj==0):
            div_y.add(jj)
            
    def CommonDiv(divSet1, divSet2):
        divisor=divSet1 & divSet2
        return divisor
    print(CommonDiv(div_x, div_y))

getDiv(2,6)와 CommonDiv(div_x, div_y)를 차례대로 호출했을 때, 결과는?

                    </pre>
                    <hr>
                    <div class="radio-wrapper">
                        <RadioGroup v-model="answers[0]" vertical>
                            <Radio label="1">
                                <span> {1,2,1,2,3,6}, {1,2}</span>
                            </Radio>
                            <Radio label="2">
                                <span>{1,2}, {1,2}</span>
                            </Radio>
                            <Radio label="3">
                                <span>{1,2,1,2,3,6}, NameError</span>
                            </Radio>
                            <Radio label="4">
                                <span>{1,2}, NameError</span>
                            </Radio>
                            <Radio label="5">
                                <span>{1,2,3,6}, NameError</span>
                            </Radio>
                        </RadioGroup>
                    </div>
                </Card>
                
            </div>
        </CarouselItem>
        <!-- 문제 end -->
    
    </Carousel>
</div>
</template>
<script>
export default {
  data () {
    return {
      value: 0
    }
  },
  computed: {
    answers () {
      const answers = []
      for (let index = 0; index < 5; index++) {
        answers.push('')
      }
      return answers
    }
  }
}
</script>
<style >
.test-wrapper {

}

.test-wrapper .problem-wrapper {

}

.test-wrapper .problem-wrapper .title {
    text-align: center;    
    font-size: 20px;
}



</style>
